from pylipd.globals.schema import SCHEMA, SYNONYMS
from pylipd.globals.urls import ONTONS, NSURL
from pylipd.globals.blacklist import REVERSE_BLACKLIST

import re
import os

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))
CLASSDIR = os.path.realpath(f"{SCRIPTDIR}/../classes")
if not os.path.exists(CLASSDIR):
    os.makedirs(CLASSDIR)
TEMPLATEDIR = f"{CLASSDIR}/templates"

def get_fromdata_item(ptype, range, is_enum):
    fromdataitem = f"""
                for val in value:"""
    if ptype == "object" and range is not None:
        if is_enum:
            fromdataitem += f"""
                    obj = {range}.from_synonym(re.sub("^.*?#", "", val["@id"]))
            """
        else:
            fromdataitem += f"""
                    if "@id" in val:
                        obj = {range}.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            """
    elif range:
        fromdataitem += f"""
                    if "@value" in val:
                        obj = val["@value"]"""
    else:
        fromdataitem += f"""
                    obj = val["@id"]"""
    return fromdataitem


def get_todata_item(type, range):
    todataitem = ""
    if type == "literal" and range:
        todataitem += f"""
            obj = {{
                "@value": value_obj,
                "@type": "literal",
                "@datatype": "http://www.w3.org/2001/XMLSchema#{range}"
            }}"""
    elif type == "literal":
        todataitem += f"""
            obj = {{
                "@id": value_obj,
                "@type": "uri"
            }}"""
    elif type == "object":
        todataitem += f"""
            if type(value_obj) is str:
                obj = {{
                    "@value": value_obj,
                    "@type": "literal",
                    "@datatype": "http://www.w3.org/2001/XMLSchema#string"
                }}
            else:
                obj = {{
                    "@id": value_obj.id,
                    "@type": "uri"
                }}
                data = value_obj.to_data(data)"""
    return todataitem

def get_tojson_item(type):
    todataitem = ""
    if type == "literal":
        todataitem += f"""
            obj = value_obj"""
    elif type == "object":
        todataitem += f"""
            obj = value_obj.to_json()"""
    return todataitem

def get_fromjson_item(ptype, range, is_enum):
    fromjsonitem = ""
    if ptype == "object" and range is not None:
        if is_enum:
            fromjsonitem += f"""
                    obj = {range}.from_synonym(re.sub("^.*?#", "", value))"""
        else:
            fromjsonitem += f"""
                    obj = {range}.from_json(value)"""
    elif range:
        fromjsonitem += f"""
                    obj = value"""
    else:
        fromjsonitem += f"""
                    obj = value"""
    return fromjsonitem

def get_python_snippet_for_multi_value_property(clsid, pid, propid, pname, ptype, ont_range, python_range, getter, setter, adder, is_enum):
    # Create the python snippet for initialzing property variables
    initvar = f"self.{pname}: list[{python_range}] = []"

    # Create the python function snippet for this property to convert the class to a dictionary (todata)
    todataitem = get_todata_item(ptype, ont_range)
    todata = f"""

        if len(self.{pname}):
            data[self.id][\"{propid}\"] = []
        for value_obj in self.{pname}:{todataitem}
            data[self.id][\"{propid}\"].append(obj)"""

    # Create the python function snippet for this property to convert from data dictionary to a class (fromdata)
    fromdataitem = get_fromdata_item(ptype, python_range, is_enum)
    fromdata = f"""
            elif key == \"{propid}\":{fromdataitem}
                    self.{pname}.append(obj)"""

    # Create the python function snippet for this property to convert the class to json (tojson)
    if pid not in REVERSE_BLACKLIST:
        tojsonitem = get_tojson_item(ptype)
        tojson = f"""

        if len(self.{pname}):
            data[\"{pid}\"] = []
        for value_obj in self.{pname}:{tojsonitem}
            data[\"{pid}\"].append(obj)"""            
    # Create the python function snippet for this property to convert from json dictionary to a class (fromjson)
    fromjsonitem = get_fromjson_item(ptype, python_range, is_enum)
    fromjson = f"""
            elif key == \"{pid}\":
                for value in pvalue:{fromjsonitem}
                    self.{pname}.append(obj)"""
    
    if python_range is None:
        python_range = "object"
    error_msg = "Error: '{" + pname + "}' is not of type " + python_range
    if is_enum:
        error_msg += f"\\nYou can create a new {python_range} object from a string using the following syntax:\\n"
        error_msg += f"- Fetch existing {python_range} by synonym: {python_range}.from_synonym(\\\"{{"+pname+"}\\\")\\n"
        error_msg += f"- Create a new custom {python_range}: {python_range}(\\\"{{"+pname+"}\\\")"
    # Create the python snippet for getter/setter/adders
    fns = f"""
    def {getter}(self) -> list[{python_range}]:
        \"\"\"Get {pname} list.

        Returns
        -------
        list[{python_range}]
            A list of {python_range} objects.
        \"\"\"
        return self.{pname}

    def {setter}(self, {pname}:list[{python_range}]):
        \"\"\"Set the {pname} list.

        Parameters
        ----------
        {pname} : list[{python_range}]
            The list to assign.
        \"\"\"
        assert isinstance({pname}, list), "Error: {pname} is not a list"
        assert all(isinstance(x, {python_range}) for x in {pname}), f"{error_msg}"
        self.{pname} = {pname}

    def {adder}(self, {pname}:{python_range}):
        \"\"\"Add a value to the {pname} list.

        Parameters
        ----------
        {pname} : {python_range}
            The value to append.
        \"\"\"
        assert isinstance({pname}, {python_range}), f"{error_msg}"
        self.{pname}.append({pname})
        """
    return (initvar, todata, fromdata, tojson, fromjson, fns)


def get_python_snippet_for_property(clsid, pid, propid, pname, ptype, ont_range, python_range, getter, setter, is_enum):
    # Create the python snippet for initialzing property variables
    initvar = f"self.{pname}: {python_range} = None"

    # Create the python function snippet for this property to convert the class to a dictionary (todata)
    todataitem = get_todata_item(ptype, ont_range)
    todata = f"""

        if self.{pname}:
            value_obj = self.{pname}{todataitem}
            data[self.id][\"{propid}\"] = [obj]
                """
    # Create the python function snippet for this property to convert from data dictionary to a class (fromdata)
    fromdataitem = get_fromdata_item(ptype, python_range, is_enum)
    fromdata = f"""
            elif key == \"{propid}\":{fromdataitem}                        
                    self.{pname} = obj"""

    # Create the python function snippet for this property to convert the class to json (tojson)
    tojson = ""
    if pid not in REVERSE_BLACKLIST:
        tojsonitem = get_tojson_item(ptype)
        tojson += f"""

        if self.{pname}:
            value_obj = self.{pname}{tojsonitem}
            data[\"{pid}\"] = obj"""

    # Create the python function snippet for this property to convert from json dictionary to a class (fromjson)
    fromjsonitem = get_fromjson_item(ptype, python_range, is_enum)
    fromjson = f"""
            elif key == \"{pid}\":
                    value = pvalue{fromjsonitem}
                    self.{pname} = obj"""
    
    if python_range is None:
        python_range = "object"
            
    error_msg = "Error: '{" + str(pname) + "}' is not of type " + str(python_range)
    if is_enum:
        error_msg += f"\\nYou can create a new {python_range} object from a string using the following syntax:\\n"
        error_msg += f"- Fetch existing {python_range} by synonym: {python_range}.from_synonym(\\\"{{"+pname+"}\\\")\\n"
        error_msg += f"- Create a new custom {python_range}: {python_range}(\\\"{{"+pname+"}\\\")"

    # Create the python snippet for getter/setter/adders
    fns = f"""
    def {getter}(self) -> {python_range}:
        \"\"\"Get {pname}.

        Returns
        -------
        {python_range}
            The current value of {pname}.
        \"\"\"
        return self.{pname}

    def {setter}(self, {pname}:{python_range}):
        \"\"\"Set {pname}.

        Parameters
        ----------
        {pname} : {python_range}
            The value to assign.
        \"\"\"
        assert isinstance({pname}, {python_range}), f"{error_msg}"
        self.{pname} = {pname}
    """
    # Special case for Dataset
    if clsid == "Dataset" and pname == "name":
        fns += f"    self.id = self.ns + '/' + {pname} # This is a hack to set the id of the dataset based on the name\n"

    return (initvar, todata, fromdata, tojson, fromjson, fns)


def generate_enum_classes():
    for sectionid in SYNONYMS:
        for clsid in SYNONYMS[sectionid]:
            done = {}
            synonyms = SYNONYMS[sectionid][clsid]

            fileid = clsid.lower()
            with open(f"{CLASSDIR}/{fileid}.py", "w") as outf:
                outf.write("""
##############################
# Auto-generated. Do not Edit
##############################
""")
                outf.write("from pylipd.globals.synonyms import SYNONYMS\n\n")

                outf.write(f"class {clsid}:\n    \"\"\"Controlled-vocabulary class for `{clsid}` terms.\"\"\"")
                outf.write(f"""
    synonyms = SYNONYMS["{sectionid}"]["{clsid}"]

    def __init__(self, id, label):
        \"\"\"Initialize a {clsid} term.

        Parameters
        ----------
        id : str
            The full URI identifier for this term.
        label : str
            The human-readable label for this term.
        \"\"\"
        self.id = id
        self.label = label
    
    def __eq__(self, value: object) -> bool:
        \"\"\"Check equality based on term ID.

        Parameters
        ----------
        value : object
            The object to compare against.

        Returns
        -------
        bool
            True if the IDs match, False otherwise.
        \"\"\"
        return self.id == value.id
        
    def getLabel(self):
        \"\"\"Return the human-readable label of the term.

        Returns
        -------
        str
            The label for this term.
        \"\"\"
        return self.label

    def getId(self):
        \"\"\"Return the full URI identifier of the term.

        Returns
        -------
        str
            The URI identifier for this term.
        \"\"\"
        return self.id
    
    def to_data(self, data={{}}):
        \"\"\"Serialize this term to JSON-LD format.

        Parameters
        ----------
        data : dict, optional
            Existing data dictionary to extend.

        Returns
        -------
        dict
            The updated data dictionary.
        \"\"\"
        data[self.id] ={{
            "label": [
                {{
                    "@datatype": None,
                    "@type": "literal",
                    "@value": self.label
                }}
            ]
        }}
        return data

    def to_json(self):
        \"\"\"Return the plain-text label (used in lightweight JSON).

        Returns
        -------
        str
            The label for this term.
        \"\"\"
        data = self.label
        return data

    @classmethod
    def from_synonym(cls, synonym):
        \"\"\"Create a {clsid} instance from a synonym string.

        Parameters
        ----------
        synonym : str
            A synonym or alternative name for the term.

        Returns
        -------
        {clsid} or None
            The {clsid} instance if found, None otherwise.
        \"\"\"
        if synonym.lower() in {clsid}.synonyms:
            synobj = {clsid}.synonyms[synonym.lower()]
            return {clsid}(synobj['id'], synobj['label'])
        return None
        
""")
                outf.write(f"class {clsid}Constants:")
                for synonym in synonyms:
                    synobj = synonyms[synonym]
                    synid = re.sub("[^a-zA-Z0-9]", "_", re.sub(".*?#", "", synobj["id"]))
                    if synid in done:
                        continue
                    done[synid] = True
                    outf.write(f"""
    {synid} = {clsid}("{synobj['id']}", "{synobj['label']}")""")

def fetch_extra_template_functions(clsid):
    imports = []
    fns = []

    curfn = ""
    fn_ongoing = False
    tplfilename = f"{TEMPLATEDIR}/{clsid.lower()}.py"
    if os.path.exists(tplfilename):
        with open(tplfilename, "r") as inf:
            for line in inf.readlines():
                #line = line.strip()
                if re.match("^import ", line, re.I) or re.match("^from .+ import ", line, re.I):
                    imports.append(line)
                if re.match("^#.*START TEMPLATE FUNCTION", line, re.I):
                    fn_ongoing = True
                elif re.match("^#.*END TEMPLATE FUNCTION", line, re.I):
                    fn_ongoing = False
                    if curfn:
                        fns.append("\n" + curfn)
                    curfn = ""
                elif fn_ongoing:
                    curfn += "    " + line                
    return (imports, fns)


def generate_class_file(clsid, import_snippets, initvar_snippets, 
                        todata_snippets, fromdata_snippets, 
                        tojson_snippets, fromjson_snippets, 
                        fn_snippets):    

    (ximports, xfn_snippets) = fetch_extra_template_functions(clsid)
    fn_snippets = fn_snippets + xfn_snippets

    filename = f"{CLASSDIR}/{clsid.lower()}.py"
    with open(filename, "w") as outf:
        # Write the header
        outf.write("""
##############################
# Auto-generated. Do not Edit
##############################

""")
        # Write the imports
        outf.write(f"import re\n")
        for im in ximports:
            outf.write(im)
        outf.write("from pylipd.utils import uniqid\n")
        for im in import_snippets:
            outf.write(f"from pylipd.classes.{im.lower()} import {im}\n")
        outf.write("\n")


        # Write the class header
        outf.write(f"class {clsid}:\n    \"\"\"Auto-generated LinkedEarth class representing `{clsid}`.\"\"\"")


        # Write the init function
        outf.write(f"""
    def __init__(self):
        \"\"\"Initialize a new {clsid} instance.\"\"\"
        """)
        for snippet in initvar_snippets:
            outf.write(f"""
        {snippet}""")
        outf.write(f"""
        self.misc = {{}}
        self.ontns = "{ONTONS}"
        self.ns = "{NSURL}"
        self.type = "{ONTONS}{clsid}"
        self.id = self.ns + "/" + uniqid("{clsid}.")""")
        outf.write("\n")


        # Write the from_data function
        outf.write(f"""
    @staticmethod
    def from_data(id, data) -> '{clsid}':
        \"\"\"Instantiate `{clsid}` from an ontology-style data graph.

        Parameters
        ----------
        id : str
            The node identifier for this object.
        data : dict
            Dictionary mapping node ids to their predicate lists.

        Returns
        -------
        {clsid}
            The populated `{clsid}` instance.
        \"\"\"
        self = {clsid}()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]""")
        for snippet in fromdata_snippets:
            outf.write(f"""
        {snippet}""")
        outf.write(f"""
            else:
                for val in value:
                    obj = None
                    if "@id" in val:
                        obj = data[val["@id"]]
                    elif "@value" in val:
                        obj = val["@value"]
                    self.set_non_standard_property(key, obj)
            
        return self""")
        outf.write("\n") 


        # Write the to_data function
        outf.write(f"""
    def to_data(self, data={{}}):
        \"\"\"Serialize the object into a JSON-LD compatible dictionary.

        Parameters
        ----------
        data : dict, optional
            Existing data dictionary to extend.

        Returns
        -------
        dict
            The updated data dictionary.
        \"\"\"
        data[self.id] = {{}}
        data[self.id]["type"] = [
            {{
                "@id": self.type,
                "@type": "uri"
            }}
        ]""")
        for snippet in todata_snippets:
            outf.write(f"""{snippet}""")
        outf.write(f"""
        for key in self.misc:
            value = self.misc[key]
            data[self.id][key] = []
            ptype = None
            tp = type(value).__name__
            if tp == "int":
                ptype = "http://www.w3.org/2001/XMLSchema#integer"
            elif tp == "float" or tp == "double":
                ptype = "http://www.w3.org/2001/XMLSchema#float"
            elif tp == "str":
                if re.match(r"\d{{4}}-\d{{2}}-\d{{2}}( |T)\d{{2}}:\d{{2}}:\d{{2}}", value):
                    ptype = "http://www.w3.org/2001/XMLSchema#datetime"   
                elif re.match(r"\d{{4}}-\d{{2}}-\d{{2}}", value):
                    ptype = "http://www.w3.org/2001/XMLSchema#date"
                else:
                    ptype = "http://www.w3.org/2001/XMLSchema#string"
            elif tp == "bool":
                ptype = "http://www.w3.org/2001/XMLSchema#boolean"

            data[self.id][key].append({{
                "@value": value,
                "@type": "literal",
                "@datatype": ptype
            }})
        
        return data""")
        outf.write("\n") 


        # Write the to_json function
        outf.write(f"""
    def to_json(self):
        \"\"\"Return a lightweight JSON representation (used by LiPD).

        Returns
        -------
        dict
            A dictionary representation of this object.
        \"\"\"
        data = {{
            "@id": self.id
        }}""")
        for snippet in tojson_snippets:
            outf.write(f"""{snippet}""") 
        outf.write("\n") 
        outf.write(f"""
        for key in self.misc:
            value = self.misc[key]
            data[key] = value
                   
        return data""")
        outf.write("\n")


        # Write the from_json function
        outf.write(f"""
    @staticmethod
    def from_json(data) -> '{clsid}':
        \"\"\"Instantiate `{clsid}` from its lightweight JSON representation.

        Parameters
        ----------
        data : dict
            The JSON dictionary to parse.

        Returns
        -------
        {clsid}
            The populated `{clsid}` instance.
        \"\"\"
        self = {clsid}()
        for key in data:
            pvalue = data[key]
            if key == "@id":
                self.id = pvalue""")
        for snippet in fromjson_snippets:
            outf.write(f"""{snippet}""") 
        outf
        outf.write(f"""
            else:
                self.set_non_standard_property(key, pvalue)
                   
        return self""")
        outf.write("\n")        

        # Write the functions to handle non standard properties
        outf.write(f"""
    def set_non_standard_property(self, key, value):
        \"\"\"Store a predicate that is not defined in the ontology schema.

        This is useful for forward-compatibility with new properties that are
        not yet part of the official schema.

        Parameters
        ----------
        key : str
            The property name.
        value : any
            The property value.
        \"\"\"
        if key not in self.misc:
            self.misc[key] = value
    
    def get_non_standard_property(self, key):
        \"\"\"Return a single non-standard property by key.

        Parameters
        ----------
        key : str
            The property name.

        Returns
        -------
        any
            The property value.
        \"\"\"
        return self.misc[key]
                
    def get_all_non_standard_properties(self):
        \"\"\"Return the dictionary of all non-standard properties.

        Returns
        -------
        dict
            Dictionary of all non-standard properties.
        \"\"\"
        return self.misc

    def add_non_standard_property(self, key, value):
        \"\"\"Append a value to a list-valued non-standard property.

        Parameters
        ----------
        key : str
            The property name.
        value : any
            The value to append.
        \"\"\"
        if key not in self.misc:
            self.misc[key] = []
        self.misc[key].append(value)
        """)   

        # Write the getter/setter functions       
        for fn in fn_snippets:
            outf.write(fn)


def generate_lipd_classes():
    # Check all classes in Schema
    for clsid in SCHEMA:
        props = SCHEMA[clsid]    

        import_snippets = set()
        initvar_snippets = set()
        fromdata_snippets = set()
        todata_snippets = set()
        tojson_snippets = set()
        fromjson_snippets = set()
        fn_snippets = set()

        # Check all properties
        for pid in props:
            if pid[0] == "@":
                continue
            prop = props[pid]
            
            propid = pid
            if "name" in prop:
                propid = prop["name"]

            # Create the python property name (pname) from ontology property id (propid)
            pname = propid
            if re.match("^has", propid):
                pname = re.sub("^has", "", propid)
            elif re.match("^is", propid):
                pname = re.sub("^is", "", propid)
            # Fix if property name is "type". Gets mixed up
            if pname.lower() == "type":
                pname = f"{clsid}Type"
            pname = pname[0].lower() + pname[1:]

            # Check if the property is supposed to have multiple values. Rename accordingly
            multiple = prop.get("multiple", False)
            mpname = pname
            if multiple and not re.match(".*(data|by)$", pname, re.I):
                mpname += "s"

            is_enum = ("synonyms" in prop)

            # Create getter/setter/adder function names
            adder = None
            suffix = pname[0].upper() + pname[1:]
            setter = "set" + suffix
            if re.match("^is", propid):
                getter = "is" + suffix
            else:
                getter = "get" + suffix
            if multiple:
                adder = "add" + suffix
                if not re.match(".*(data|by)$", pname, re.I):
                    setter += "s"
                    getter += "s"
            
            # Get the range of the property
            ont_range = "string"
            ptype = "literal"
            if "class_type" in prop:
                ont_range = prop["class_type"]
            elif "type" in prop:
                ont_range = prop["type"]
                if ont_range == "Individual":
                    ont_range = None
            if "class_range" in prop:
                ptype = "object"
                ont_range = prop["class_range"]
            elif "schema" in prop:
                ptype = "object"
                ont_range = prop["schema"]

            python_range = ont_range
            # Rewrite the property range to python types
            if ont_range == "integer":
                python_range = "int"
            elif ont_range == "string":
                python_range = "str"
            elif ont_range == "boolean":
                python_range = "bool"

            # Get python snippets for initialization function, todata function, fromdata from, and the setter/getter functions
            if multiple:
                (initvar, todata, fromdata, tojson, fromjson, fns) = get_python_snippet_for_multi_value_property(clsid, pid, propid, mpname, ptype, 
                                                                                               ont_range, python_range, 
                                                                                               getter, setter, adder, is_enum)  
            else:
                (initvar, todata, fromdata, tojson, fromjson, fns) = get_python_snippet_for_property(clsid, pid, propid, mpname, ptype, 
                                                                                   ont_range, python_range, 
                                                                                   getter, setter, is_enum)
            
            # Collect all snippets
            # Import the range class (in case the range is a class)
            if ptype == "object":
                import_snippets.add(python_range)
            initvar_snippets.add(initvar)
            todata_snippets.add(todata)
            fromdata_snippets.add(fromdata)
            tojson_snippets.add(tojson)
            fromjson_snippets.add(fromjson)
            fn_snippets.add(fns)
        
        # Write outputs
        generate_class_file(clsid, sorted(import_snippets), sorted(initvar_snippets), 
                            sorted(todata_snippets), sorted(fromdata_snippets), 
                            sorted(tojson_snippets), sorted(fromjson_snippets), 
                            sorted(fn_snippets))

if __name__ == "__main__":
    generate_enum_classes()
    generate_lipd_classes()