import copy
import re
import uuid

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
    """
    Generate a truly unique identifier using UUID4.
    
    Parameters:
    -----------
    prefix : str
        Optional prefix to prepend to the UUID
    more_entropy : bool
        If True, generates a longer UUID with additional entropy
        
    Returns:
    --------
    str
        A unique identifier string
    """
    if more_entropy:
        # Generate two UUIDs for extra entropy and combine them
        uuid1 = str(uuid.uuid4()).replace('-', '')
        uuid2 = str(uuid.uuid4()).replace('-', '')[:8]  # Take first 8 chars of second UUID
        the_uniqid = uuid1 + uuid2
    else:
        # Standard UUID4 without hyphens
        the_uniqid = str(uuid.uuid4()).replace('-', '')
    
    # Add prefix if provided
    return (prefix if prefix else '') + the_uniqid

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
