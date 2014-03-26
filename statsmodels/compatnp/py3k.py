"""
Python 3 compatibility tools.

"""

import functools
import itertools
import sys

PY3 = (sys.version_info[0] >= 3)
PY3_2 = sys.version_info[:2] == (3, 2)

try:
    import __builtin__ as builtins
    # not writeable when instantiated with string, doesn't handle unicode well
    from cStringIO import StringIO as cStringIO
    # always writeable
    from StringIO import StringIO

    BytesIO = StringIO
    import cPickle
    import urllib2
    import urlparse
except ImportError:
    import builtins
    from io import StringIO, BytesIO

    cStringIO = StringIO
    import pickle as cPickle
    import urllib.request
    import urllib.parse
    from urllib.request import HTTPError, urlretrieve

if PY3:
    import io
    string_types = basestring
    bytes = bytes
    str = str
    asunicode = str

    def asbytes(s):
        if isinstance(s, bytes):
            return s
        return s.encode('latin1')

    def asstr(s):
        if isinstance(s, str):
            return s
        return s.decode('latin1')

    def asstr2(s):  #added JP, not in numpy version
        if isinstance(s, str):
            return s
        elif isinstance(s, bytes):
            return s.decode('latin1')
        else:
            return str(s)

    def isfileobj(f):
        return isinstance(f, io.FileIO)

    def open_latin1(filename, mode='r'):
        return open(filename, mode=mode, encoding='iso-8859-1')

    strchar = 'U'

    # have to explicitly put builtins into the namespace
    range = range
    map = map
    zip = zip
    filter = filter
    reduce = functools.reduce
    long = int
    unichr = chr

    # list-producing versions of the major Python iterating functions
    def lrange(*args, **kwargs):
        return list(range(*args, **kwargs))

    def lzip(*args, **kwargs):
        return list(zip(*args, **kwargs))

    def lmap(*args, **kwargs):
        return list(map(*args, **kwargs))

    def lfilter(*args, **kwargs):
        return list(filter(*args, **kwargs))

    urlopen = urllib.request.urlopen
    urljoin = urllib.parse.urljoin
    urlretrieve = urllib.request.urlretrieve
    string_types = str

else:
    bytes = str
    str = str
    asbytes = str
    asstr = str
    asstr2 = str
    strchar = 'S'

    def isfileobj(f):
        return isinstance(f, file)

    def asunicode(s):
        if isinstance(s, str):
            return s
        return s.decode('ascii')

    def open_latin1(filename, mode='r'):
        return open(filename, mode=mode)

    # import iterator versions of these functions
    range = xrange
    zip = itertools.izip
    filter = itertools.ifilter
    map = itertools.imap
    reduce = reduce
    long = long
    unichr = unichr

    # Python 2-builtin ranges produce lists
    lrange = builtins.range
    lzip = builtins.zip
    lmap = builtins.map
    lfilter = builtins.filter

    urlopen = urllib2.urlopen
    urljoin = urlparse.urljoin
    HTTPError = urllib2.HTTPError
    string_types = basestring


def getexception():
    return sys.exc_info()[1]


def asbytes_nested(x):
    if hasattr(x, '__iter__') and not isinstance(x, (bytes, str)):
        return [asbytes_nested(y) for y in x]
    else:
        return asbytes(x)


def asunicode_nested(x):
    if hasattr(x, '__iter__') and not isinstance(x, (bytes, str)):
        return [asunicode_nested(y) for y in x]
    else:
        return asunicode(x)


try:
    advance_iterator = next
except NameError:
    def advance_iterator(it):
        return it.next()
next = advance_iterator


try:
    callable = callable
except NameError:
    def callable(obj):
        return any("__call__" in klass.__dict__ for klass in type(obj).__mro__)