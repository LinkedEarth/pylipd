import re
import time
import math
import random

def ucfirst(s):
    return s[0].upper() + s[1:]

def lcfirst(s):
    return s[0].lower() + s[1:]

def camelCase(id) :
    term = ""
    for subid in re.split(r"\s+", id): 
        term += ucfirst(subid)
    return term

def unCamelCase(id) :
    regex = r"(?<=[a-z])(?=[A-Z]) | (?<=[A-Z])(?=[A-Z][a-z])"
    a = re.split(regex, id)
    return " ".join(a).lower()

def fromCamelCase(str) :
    return ucfirst(str)
    #return ucfirst(str.replace(r"([^A-Z])([A-Z])"", "$1_$2", str))

def escape( str ):
    str = str.replace("&", "&amp;")
    str = str.replace("<", "&lt;")
    str = str.replace(">", "&gt;")
    str = str.replace("\"", "\\\"")
    str = str.replace("\n", " ")
    str = str.replace("\r", " ")
    str = re.sub(r"\\$", "", str)
    return str

def sanitizeId(id):
    return re.sub(r"[^a-zA-Z0-9\-_\.]", "_", id)

def uniqid(prefix='', more_entropy=False):
    m = time.time()
    sec = math.floor(m)
    usec = math.floor(1000000 * (m - sec))
    if more_entropy:
        lcg = random.random()
        the_uniqid = "%08x%05x%.8F" % (sec, usec, lcg * 10)
    else:
        the_uniqid = '%8x%05x' % (sec, usec)

    the_uniqid = (prefix if prefix else '') + the_uniqid
    return the_uniqid