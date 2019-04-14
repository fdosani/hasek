from ._compat import *
from .config import Config


class Secret(object):
    """
    An object for reading and modifying encrypted values stored in the
    hasek configuration files.  This provides and easier-to-use abstraction for
    handling sensitive information than using the :class:`hasek.config.Config`
    class directly.

    :param str conf: A path to the configuration file to open.
        Defaults to ~/.hasekrc
    :param str mode: Defaults to 'r' for read-only. If not changed,
        configuration will not be writeable while open.
    :param str key_file: A path to the key file to open.
        Defaults to ~/.hasekpg
    """

    def __init__(self, conf=None, mode="r", key_file=None):
        self.config = Config(conf, mode, key_file)

    def get(self, key):
        """
        Retrieve the decrypted value of a key in a hasek
        configuration file.
        :param str key: The key used to lookup the encrypted value
        """
        if not key.startswith("secure.") and not key.startswith("connections."):
            key = "secure.{0}".format(key)
        value = self.config.get_value(key)
        if not isinstance(value, basestring):
            value = None
        return value

    def set(self, key, value):
        """
        Set a decrypted value by key in a hasek configuration file.
        
        :param str key: The key used to lookup the encrypted value
        :param value: Value to set at the given key, can be any value that is
            YAML serializeable.
        """
        if not key.startswith("secure."):
            key = "secure.{0}".format(key)
        self.config.set_value(key, value)
        self.config.write()

    def __call__(self, key):
        keys = [x.strip() for x in key.split(",")]
        if len(keys) == 1:
            return self.get(keys[0])
        return [self.get(k) for k in keys]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        pass
