import copy
import re
import time
import math
import random

from pandas import DataFrame
from rdflib.plugins.sparql.processor import SPARQLResult

import zlib, json, base64

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
    # str = str.replace("&", "&amp;")
    # str = str.replace("<", "&lt;")
    # str = str.replace(">", "&gt;")
    # str = str.replace("\"", "\\\"")
    # str = str.replace("'", "\\'")
    # str = str.replace("\n", " ")
    # str = str.replace("\r", " ")
    # str = re.sub(r"\\$", "", str)
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

def zip_string(string):
    return base64.b64encode(
        zlib.compress(string.encode('utf-8'))
    ).decode('ascii')

def unzip_string(string):
    try:
        return  zlib.decompress(base64.b64decode(string))
    except:
        raise RuntimeError("Could not decode/unzip the contents")

def expand_schema(schema) :
    xschema = {}
    for key,props in schema.items() :
        # Add core schema too
        xschema[key] = copy.copy(props)
        for lipdkey,pdetails in props.items() :
            if not type(pdetails) is dict:
                continue
            
            if (("alternates" in pdetails)) :
                for altkey in pdetails["alternates"]: 
                    xschema[key][altkey] = pdetails
    xschema["__expanded"] = True
    return xschema


def sparql_results_to_df(results: SPARQLResult) -> DataFrame:
    """
    Export results from an rdflib SPARQL query into a `pandas.DataFrame`,
    using Python types. See https://github.com/RDFLib/rdflib/issues/1179.
    """
    return DataFrame(
        data=([None if x is None else x.toPython() for x in row] for row in results),
        columns=[str(x) for x in results.vars],
    )
