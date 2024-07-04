from pylipd.globals.schema import SCHEMA, SYNONYMS
from pylipd.globals.urls import ONTONS, NSURL
import re
import os

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))
CLASSDIR = os.path.realpath(f"{SCRIPTDIR}/../classes")
# CLASSDIR = "classes"

if not os.path.exists(CLASSDIR):
    os.makedirs(CLASSDIR)

def get_fromdata_item(type, range):
    fromdataitem = f"""
                for val in value:"""
    if type == "object" and range is not None:
        if "synonyms" in prop:
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
            obj = {{
                "@id": value_obj.id,
                "@type": "uri"
            }}
            data = value_obj.to_data(data)
            """
    return todataitem


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

            outf.write(f"class {clsid}:")
            outf.write(f"""
    synonyms = SYNONYMS["{sectionid}"]["{clsid}"]

    def __init__(self, id, label):
        self.id = id
        self.label = label
    
    def __eq__(self, value: object) -> bool:
            self.id == value.id
        
    def getLabel(self):
        return self.label

    def getId(self):
        return self.id
    
    def to_data(self, data={{}}):
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
    
    @classmethod
    def from_synonym(cls, synonym):
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

for clsid in SCHEMA:
    props = SCHEMA[clsid]    

    imports = set()
    initvars = set()
    fromdata = set()
    todata = set()
    fns = set()

    iffed = False
    for pid in props:
        if pid[0] == "@":
            continue
        prop = props[pid]
        
        propid = pid
        if "name" in prop:
            propid = prop["name"]

        pname = propid
        if re.match("^has", propid):
            pname = re.sub("^has", "", propid)
        elif re.match("^is", propid):
            pname = re.sub("^is", "", propid)
        
        # Fix if property name is "type". Gets mixed up
        if pname.lower() == "type":
            pname = f"{clsid}Type"

        pname = pname[0].lower() + pname[1:]

        multiple = prop.get("multiple", False)
        mpname = pname
        if multiple and not re.match(".*(data|by)$", pname, re.I):
            mpname += "s"

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
        
        range = "string"        
        type = "literal"
        if "class_type" in prop:
            range = prop["class_type"]
        elif "type" in prop:
            range = prop["type"]
            if range == "Individual":
                range = None
        if "class_range" in prop:
            type = "object"
            range = prop["class_range"]
        elif "schema" in prop:
            type = "object"
            range = prop["schema"]
        
        todataitem = get_todata_item(type, range)

        # Rewriting ranges to python types
        if range == "integer":
            range = "int"
        elif range == "string":
            range = "str"
        elif range == "boolean":
            range = "bool"

        if type == "object":
            imports.add(range)

        fromdataitem = get_fromdata_item(type, range)

        if multiple:
            initvars.add(f"self.{mpname}: list[{range}] = []")
            mptodataitem = f"""
        if len(self.{mpname}):
            data[self.id]["{propid}"] = []
        for value_obj in self.{mpname}:{todataitem}
            data[self.id]["{propid}"].append(obj)"""
            todata.add(mptodataitem)

            mpfromdataitem = f"""
            elif key == "{propid}":
{fromdataitem}
                    self.{mpname}.append(obj)"""
            fromdata.add(mpfromdataitem)

            fns.add(f"""
    def {getter}(self) -> list[{range}]:
        return self.{mpname}

    def {setter}(self, {mpname}:list[{range}]):
        self.{mpname} = {mpname}

    def {adder}(self, {pname}:{range}):
        self.{mpname}.append({pname})
        """)
            
        else:
            initvars.add(f"self.{pname}: {range} = None") 
            sfromdataitem = f"""
            elif key == "{propid}":
{fromdataitem}                        
                    self.{pname} = obj"""
            fromdata.add(sfromdataitem)

            stodataitem = f"""
        if self.{pname}:
            value_obj = self.{pname}{todataitem}
            data[self.id]["{propid}"] = [obj]
            """
            todata.add(stodataitem)

            fns.add(f"""
    def {getter}(self) -> {range}:
        return self.{pname}

    def {setter}(self, {pname}:{range}):
        self.{pname} = {pname}
""")         
    fileid = clsid.lower()
    with open(f"{CLASSDIR}/{fileid}.py", "w") as outf:
        outf.write("""
##############################
# Auto-generated. Do not Edit
##############################

""")
        outf.write(f"import re\n")
        outf.write("from pylipd.utils import uniqid\n")

        for im in imports:
            outf.write(f"from pylipd.classes.{im.lower()} import {im}\n")
        outf.write("\n")
        outf.write(f"class {clsid}:\n")
        outf.write(f"""
    def __init__(self):""")
        for initvar in initvars:
            outf.write(f"""
        {initvar}""")

        # namespace is hardcoded (from class generation)
        # type is hardcoded (from class generation) : ontns + class
        # id is generated initially (ns + class + "." + uuid)
        # id can be overridden in from_data

        outf.write(f"""
        self.misc = {{}}
        self.ontns = "{ONTONS}"
        self.ns = "{NSURL}"
        self.type = "{ONTONS}{clsid}"
        self.id = self.ns + "/" + uniqid("{clsid}")""")

        outf.write("\n")
        outf.write(f"""
    @staticmethod
    def from_data(id, data) -> '{clsid}':
        self = {clsid}()
        self.id = id
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                for val in value:
                    self.type = val["@id"]""")
        for initvar in fromdata:
            outf.write(f"""
        {initvar}""")
        outf.write(f"""
            else:
                for val in value:
                    obj = None
                    if "@id" in val:
                        obj = mydata[val["@id"]]
                    elif "@value" in val:
                        obj = val["@value"]
                    self.set_non_standard_property(key, obj)
        
        return self""")
        outf.write("\n") 
        
        outf.write(f"""
    def to_data(self, data={{}}):
        data[self.id] = {{}}
        data[self.id]["type"] = [
            {{
                "@id": self.type,
                "@type": "uri"
            }}
        ]
""")

        for tovar in todata:
            outf.write(f"""
        {tovar}""")        
        outf.write(f"""

        for key in self.misc:
            value = self.misc[key]
            data[self.id][key] = []
            ptype = None
            tp = type(value).__name__
            if tp == "int":
                ptype = "http://www.w3.org/2001/XMLSchema#integer"
            elif tp == "float":
                ptype = "http://www.w3.org/2001/XMLSchema#float"
            elif tp == "str":
                if re.match("\d{{4}}-\d{{2}}-\d{{2}}", value):
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
        outf.write(f"""
    def set_non_standard_property(self, key, value):
        if key not in self.misc:
            self.misc[key] = value
    
    def get_non_standard_property(self, key):
        return self.misc[key]
                   
    def get_all_non_standard_properties(self):
        return self.misc

    def add_non_standard_property(self, key, value):
        if key not in self.misc:
            self.misc[key] = []
        self.misc[key].append(value)
        """)          
        for fn in fns:
            outf.write(fn)