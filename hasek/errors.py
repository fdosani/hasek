class HasekError(Exception):
    """
    Baseclass for all Hasek errors.
    """


class ConfigurationError(HasekError):
    """
    For use with configuration file handling.
    """


class FileNotFound(HasekError):
    """
    Raised when file does not exist.
    """


class ConfigNotFound(ConfigurationError, FileNotFound):
    """
    Raised when the specified configuration file does not exist.
    """


class KeyNotFound(ConfigurationError, FileNotFound):
    """
    Raised when the specified configuration file does not exist.
    """


class ConfigReadOnly(ConfigurationError):
    """
    Raised when a write is attempted on a configuration file was opened
    in read mode.
    """


class InvalidCredentialsError(ConfigurationError):
    """
    Raised when connection credentials are incorrect.
    """


class ConnectionLock(ConfigurationError):
    """
    Raised when connection is locked by invalid attempts and the
    'protect' feature is being used.
    """

    def __init__(self, dsn):
        super(ConnectionLock, self).__init__(
            (
                "Connection {0} is currently locked. please update "
                "credentials and run:\n\thasek config --unlock {0}"
            ).format(dsn)
        )
