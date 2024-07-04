from pylipd.globals.schema import SCHEMA, SYNONYMS
import re
import os

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))
CLASSDIR = os.path.realpath(f"{SCRIPTDIR}/../classes")
if not os.path.exists(CLASSDIR):
    os.makedirs(CLASSDIR)

def get_initdata_item(type, range):
    initdataitem = f"""
                for val in value:"""
    if type == "object" and range is not None:
        if "synonyms" in prop:
            initdataitem += f"""
                    obj = {range}.from_synonym(re.sub("^.*?#", "", val["@id"]))
            """
        else:
            initdataitem += f"""
                    if "@id" in val:
                        obj = {range}.from_data(val["@id"], data)
                    else:
                        obj = val["@value"]
            """
    elif range:
        initdataitem += f"""
                    if "@value" in val:
                        obj = val["@value"]"""
    else:
        initdataitem += f"""
                    obj = val["@id"]"""
    return initdataitem

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
    initdata = set()
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
        pname = pname[0].lower() + pname[1:]

        multiple = prop.get("multiple", False)
        mpname = pname
        if multiple and not re.match(".*data$", pname, re.I):
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
            if not re.match(".*data$", pname, re.I):
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
        
        # Rewriting ranges to python types
        if range == "integer":
            range = "int"
        elif range == "string":
            range = "str"
        elif range == "boolean":
            range = "bool"

        if type == "object":
            imports.add(range)

        initdataitem = get_initdata_item(type, range)
        if multiple:
            initvars.add(f"self.{mpname}: list[{range}] = []")
            mpinitdataitem = f"""
            elif key == "{propid}":
{initdataitem}
                    self.{mpname}.append(obj)"""          
            initdata.add(mpinitdataitem)
            
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
            sinitdataitem = f"""
            elif key == "{propid}":
{initdataitem}                        
                    self.{pname} = obj"""
            initdata.add(sinitdataitem)
                    
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
        for im in imports:
            outf.write(f"from pylipd.classes.{im.lower()} import {im}\n")
        outf.write("\n")
        outf.write(f"class {clsid}:\n")
        outf.write(f"""
    def __init__(self):""")
        for initvar in initvars:
            outf.write(f"""
        {initvar}""")

        outf.write(f"""
        self.misc = {{}}""")

        outf.write("\n")
        outf.write(f"""
    @staticmethod
    def from_data(id, data) -> '{clsid}':
        self = {clsid}()
        mydata = data[id]
        for key in mydata:
            value = mydata[key]
            obj = None
            if key == "type":
                continue""")
        for initvar in initdata:
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