identity = lambda x: x
default_encoding = "UTF-8"
basestring = (str, bytes)
xrange = range
iterbytes = identity


def ensure_bytes(s):
    if type(s) == str:
        return bytes(s, default_encoding)
    elif type(s) == float:
        return ensure_bytes(str(s))
    elif type(s) == int:
        return ensure_bytes(str(s))
    else:
        return bytes(s)


def ensure_str(s):
    if type(s) == bytes:
        return s.decode(default_encoding)
    elif type(s) == str:
        return s
    else:
        return s


def escape_string(s):
    if isinstance(s, str):
        s = s.encode("unicode_escape").decode(default_encoding)
    elif isinstance(s, bytes):
        s = s.encode("unicode_escape")
    return s


def unescape_string(s):
    if isinstance(s, str):
        s = s.encode(default_encoding).decode("unicode_escape")
    elif isinstance(s, bytes):
        s = s.decode("unicode_escape")
    return s
