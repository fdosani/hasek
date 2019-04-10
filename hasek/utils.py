import functools
import getpass
import sys
import time
import warnings

from .logging import log

__all__ = [
    "disable_warnings",
    "get_version_info",
    "import_string",
    "pipeline",
    "prompt",
    "prompt_bool",
    "readable_time",
    "register_graceful_shutdown_signal",
    "show_warning",
    "suppress_context",
    "timer",
]


def disable_warnings(category=UserWarning):
    warnings.simplefilter("ignore", category)


def get_version_info():
    from hasek._version import __version__

    return __version__


def import_string(import_name):
    import_name = str(import_name)
    if not import_name.startswith("hasek."):
        import_name = "hasek.{}".format(import_name)
    try:
        return __import__(import_name)
    except ImportError:
        try:
            module_name, obj_name = import_name.rsplit(".", 1)
        except AttributeError as error:
            raise ImportError(error)
        try:
            module = __import__(module_name, None, None, [obj_name])
        except ImportError:
            module = import_string(module_name)
        try:
            return getattr(module, obj_name)
        except AttributeError as error:
            raise ImportError(error)


def pipeline(funcs):
    def _pipeline(x):
        return reduce(lambda a, f: f(a), funcs, x)

    return _pipeline


def prompt(message, default=None, password=False):
    while True:
        if password:
            user_input = getpass.getpass(message)
        else:
            user_input = input(message)
        if user_input:
            return user_input
        if default is not None:
            return default


def prompt_bool(message, default=False):
    yes_choices = ("y", "yes")
    no_choices = ("n", "no")

    if default:
        message = "{} [Y/n]: ".format(message)
        default_str = "Y"
    else:
        message = "{} [y/N]: ".format(message)
        default_str = "N"
    while True:
        user_input = prompt(message, default=default_str)
        if user_input.lower() in yes_choices:
            return True
        elif user_input.lower() in no_choices:
            return False
        else:
            return default


def readable_time(t):
    if t > 300:
        return "{}m".format(t // 60)
    else:
        return "{:.3f}s".format(t)


def register_shutdown_signal():
    """
    Registers a simple shutdown handler using C signals.
    """
    from ._teradata import register_shutdown_signal as _register

    _register()


def register_graceful_shutdown_signal():
    """
    Registers graceful shutdown handler using C signals. The first
    SIGINT will attempt to close the Teradata connections before
    exiting, and the second will shutdown whether the connections
    have been closed or not.
    """
    from ._teradata import register_graceful_shutdown_signal as _register

    _register()


def show_warning(message, category):
    def send_warnings_to_log(message, category, filename, lineno, file=None, line=None):
        log.write("{}:{}: {}: {}".format(filename, lineno, category.__name__, message))

    warnings.showwarning = send_warnings_to_log
    warnings.warn(message, category)


def suppress_context(exc):
    """
    Used to suppress the error context for Python 3 errors when this is
    an undesired behavior. To ensure capability with Python 2, this
    must be used in place of `raise Exception from None`
    """
    exc.__context__ = None
    exc.__cause__ = None
    return exc


def timer(f):
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        start = time.time()
        result = f(*args, **kwds)
        elapsed = time.time() - start
        sys.stderr.write("{} took {:.4f}s to finish\n".format(f.__name__, elapsed))
        return result

    return wrapper
