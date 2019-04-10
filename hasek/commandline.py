import json
import sys

from ._compat import *
from .config import Config, message_write_default
from .encrypt import create_key_file
from .io import file_exists, home_file
from .logging import colors, log, setup_logging
from .parser import Argument, Command
from .utils import prompt_bool

setup_logging()


class ConfigCommand(Command):
    name = "config"
    description = "hasek configuration"
    usage = "hasek config <options>"
    help = "View/Edit hasek configuration"

    arguments = [
        Argument(
            "-n",
            "--no-newline",
            action="store_true",
            help="Do not output a newline with value from --get",
        ),
        Argument(
            "-d",
            "--decrypt",
            action="store_true",
            help="Decrypt the contents of the settings when using --list",
        ),
        Argument(
            "--init",
            action="store_true",
            help="Initialize a new configuration file at [--config]",
            group="mutual",
        ),
        Argument(
            "--get",
            metavar="key",
            help="Retrieve the key at the given path, separating nested keys with '.'",
            group="mutual",
        ),
        Argument(
            "-l",
            "--list",
            action="store_true",
            help="Show the contents of the configuration file",
            group="mutual",
        ),
        Argument(
            "--set",
            nargs=2,
            metavar=("key", "value"),
            help="Set the key to the given value",
            group="mutual",
        ),
        Argument("--unset", metavar="key", help="Unset the given key", group="mutual"),
        Argument(
            "--unlock",
            metavar="dsn",
            help="Unlock the connection with the given DSN",
            group="mutual",
        ),
    ]

    def run(self, args):
        if args.conf is None:
            args.conf = home_file(".hasekrc")
        if args.key is None:
            args.key = home_file(".hasekpg")
        if args.init:
            if file_exists(args.conf):
                if not prompt_bool(
                    (
                        "Configuration file '{}' found, would you like to overwrite "
                        "it with defaults?"
                    ).format(args.conf),
                    default=False,
                ):
                    return
            result = Config.write_default(args.conf)
            if result:
                log.write(colors.green(result))
                log.write(message_write_default.format(args.conf))
            else:
                log.write(colors.fail("Was not successful"))
            create_key_file(args.key)
            log.write("Key file '{}' created successfully.".format(args.key))
        elif args.get is not None:
            key = args.get
            with Config(conf=args.conf, key_file=args.key) as c:
                value = c.get_value(key)
            if value == -1:
                log.write("{}: not set".format(key))
            else:
                if not isinstance(value, str):
                    value = json.dumps(value, indent=4, sort_keys=True)
                if not args.no_newline:
                    value = "{}:\n{}\n".format(key, value)
                log.write(value)
        elif args.list:
            with Config(conf=args.conf, key_file=args.key) as c:
                log.write(c.list_value(args.decrypt))
        elif args.set is not None:
            key, value = args.set
            with Config(conf=args.conf, mode="w", key_file=args.key) as c:
                c.set_value(key, value)
                c.write()
        elif args.unset is not None:
            with Config(conf=args.conf, mode="w", key_file=args.key) as c:
                c.unset_value(args.unset)
                c.write()
        elif args.unlock is not None:
            Config.unlock_connection(args.conf, args.unlock, args.key)


class SecretCommand(Command):
    name = "secret"
    description = "hasek encrypted storage"
    usage = "hasek secret <key>"
    help = "Retrieve encrypted settings"

    arguments = [Argument("key_value"), Argument("-n", default=False)]

    def run(self, args):
        with Config(conf=args.conf, key_file=args.key) as c:
            if not args.key_value.startswith(
                "secure."
            ) and not args.key_value.startswith("connections."):
                key = "secure.{}".format(args.key_value)
            else:
                key = args.key_value
            value = c.get_value(key)
            if isinstance(value, basestring):
                sys.stdout.write(value)
                if args.n:
                    sys.stdout.write("\n")
            else:
                sys.stderr.write("Key '{}' not found\n".format(key))
                sys.exit(1)
