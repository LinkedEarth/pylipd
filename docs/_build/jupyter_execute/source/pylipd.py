#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pylipd.lipd import LiPD

lipd = LiPD()
lipd.load(["https://lipdverse.org/data/LCf20b99dfe8d78840ca60dfb1f832b9ec/1_0_1//Nunalleq.Ledger.2018.lpd"])

ts_list = lipd.get_timeseries(lipd.get_all_dataset_names())

for dsname, tsos in ts_list.items():
    for tso in tsos:
        if 'paleoData_variableName' in tso:
            print(dsname+': '+tso['paleoData_variableName']+': '+tso['archiveType'])


# In[2]:


from pylipd.lipd import LiPD

# Load a local file
lipd = LiPD()
lipd.load([
    "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
])
dsname = lipd.get_all_dataset_names()[0]
lipd.create_lipd(dsname, "test.lpd")


# In[3]:


from pylipd.utils.dataset import load_dir

lipd = load_dir()
Lfiltered = lipd.filter_by_archive_type('marine')
Lfiltered.get_all_dataset_names()


# In[4]:


from pylipd.utils.dataset import load_dir

lipd = load_dir()
Lfiltered = lipd.filter_by_geo_bbox(0,25,50,50)
Lfiltered.get_all_dataset_names()


# In[5]:


from pylipd.lipd import LiPD

# Load LiPD files from a local directory
lipd = LiPD()
lipd.load([
    "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
    "../examples/data/MD98_2181.Stott.2007.lpd"
])

all_datasets = lipd.get_all_dataset_names()
print("Loaded datasets: " + str(all_datasets))
ds = lipd.get(all_datasets[0])
print("Got dataset: " + str(ds.get_all_dataset_names()))


# In[6]:


from pylipd.lipd import LiPD

# Load Local files
lipd = LiPD()
lipd.load([
    "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
    "../examples/data/MD98_2181.Stott.2007.lpd"
])
print(lipd.get_all_archiveTypes())


# In[7]:


from pylipd.lipd import LiPD

# Load local files
lipd = LiPD()
lipd.load([
    "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
    "../examples/data/MD98_2181.Stott.2007.lpd"
])
print(lipd.get_all_dataset_ids())


# In[8]:


from pylipd.lipd import LiPD

# Load local files
lipd = LiPD()
lipd.load([
    "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
    "../examples/data/MD98_2181.Stott.2007.lpd"
])
print(lipd.get_all_dataset_names())


# In[9]:


from pylipd.lipd import LiPD

lipd = LiPD()
lipd.load([
    "../examples/data/ODP846.Lawrence.2006.lpd"
])

df = lipd.get_all_variables()
print(df)


# In[10]:


from pylipd.lipd import LiPD

# Fetch LiPD data from remote RDF Graph
lipd = LiPD()
lipd.load([
    "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
    "../examples/data/MD98_2181.Stott.2007.lpd"
])
print(lipd.get_bibtex(save=False))


# In[11]:


from pylipd.lipd import LiPD

lipd = LiPD()
lipd.load([
    "../examples/data/ODP846.Lawrence.2006.lpd"
])
all_datasets = lipd.get_all_dataset_names()
print("Loaded datasets: " + str(all_datasets))

ens_df = lipd.get_ensemble_tables(
    ensembleVarName="age",
    ensembleDepthVarName="depth"
)
print(ens_df)


# In[12]:


from pylipd.lipd import LiPD

# Load a local LiPD file
lipd = LiPD()
lipd.load([
    "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
])
lipd_json = lipd.get_lipd(lipd.get_all_dataset_names()[0])
print(lipd_json)


# In[13]:


from pylipd.lipd import LiPD

# Fetch LiPD data from remote RDF Graph
lipd_remote = LiPD()
lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
ts_list = lipd_remote.get_timeseries(["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001", "MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012"])
for dsname, tsos in ts_list.items():
    for tso in tsos:
        if 'paleoData_variableName' in tso:
            print(dsname+': '+tso['paleoData_variableName']+': '+tso['archiveType'])


# In[14]:


from pylipd.lipd import LiPD

lipd = LiPD()
lipd.load([
    "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
    "../examples/data/MD98_2181.Stott.2007.lpd",
    "../examples/data/Ant-WAIS-Divide.Severinghaus.2012.lpd",
    "https://lipdverse.org/data/LCf20b99dfe8d78840ca60dfb1f832b9ec/1_0_1/Nunalleq.Ledger.2018.lpd"
])

print(lipd.get_all_dataset_names())


# In[15]:


from pylipd.lipd import LiPD

lipd = LiPD()
lipd.load_from_dir("../examples/data")

print(lipd.get_all_dataset_names())


# In[16]:


from pylipd.lipd import LiPD

# Fetch LiPD data from remote RDF Graph
lipd_remote = LiPD()
lipd_remote.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
lipd_remote.load_remote_datasets(["Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001", "MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012"])
print(lipd_remote.get_all_dataset_names())


# In[17]:


from pylipd.lipd import LiPD

# Load local files
lipd = LiPD()
lipd.load([
    "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
    "../examples/data/MD98_2181.Stott.2007.lpd"
])
all_datasets = lipd.get_all_dataset_names()
print("Loaded datasets: " + str(all_datasets))
popped = lipd.pop(all_datasets[0])
print("Loaded datasets after pop: " + str(lipd.get_all_dataset_names()))
print("Popped dataset: " + str(popped.get_all_dataset_names()))


# In[18]:


from pylipd.lipd import LiPD

# Load local files
lipd = LiPD()
lipd.load([
    "../examples/data/Ocn-MadangLagoonPapuaNewGuinea.Kuhnert.2001.lpd",
    "../examples/data/MD98_2181.Stott.2007.lpd"
])
all_datasets = lipd.get_all_dataset_names()
print("Loaded datasets: " + str(all_datasets))
lipd.remove(all_datasets[0])
print("Loaded datasets after remove: " + str(lipd.get_all_dataset_names()))


# In[19]:


from pylipd.lipd import LiPD

lipd = LiPD()
lipd.load([
    "../examples/data/ODP846.Lawrence.2006.lpd"
])

S = lipd.to_lipd_series()


# In[20]:


from pylipd.utils.rdf_graph import RDFGraph

# Load RDF file into graph
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"])
(result, result_df) = rdf.query("SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10")
print(result_df)


# In[21]:


from pylipd.utils.rdf_graph import RDFGraph

# Fetch RDF graph data for given id(s)
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
rdf.get("http://example.org/graph")


# In[22]:


from pylipd.utils.rdf_graph import RDFGraph

# Fetch RDF Graph Data
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
print(rdf.get_all_graph_ids())


# In[23]:


from pylipd.utils.rdf_graph import RDFGraph

# Load RDF file into graph
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"])
(result, result_df) = rdf.query("SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10")
print(result_df)


# In[24]:


from pylipd.utils.rdf_graph import RDFGraph

# Pop RDF graph data for given id(s)
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
popped = rdf.pop("http://example.org/graph")


# In[25]:


from pylipd.utils.rdf_graph import RDFGraph

rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"])
query = """PREFIX le: <http://linked.earth/ontology#>
        select ?s ?p ?o where {
            ?s ?p ?o
        } LIMIT 10 """
result, result_df = rdf.query(query)
print(result_df)


# In[26]:


from pylipd.utils.rdf_graph import RDFGraph

# Remove RDF graph data for given id(s)
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
rdf.remove("http://example.org/graph")


# In[27]:


from pylipd.utils.rdf_graph import RDFGraph

# Fetch RDF data
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
nquads = rdf.serialize()
print(nquads[:10000])
print("...")


# In[28]:


from pylipd.utils.rdf_graph import RDFGraph

# Fetch LiPD data from remote RDF Graph
rdf = RDFGraph()
rdf.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
(result, result_df) = rdf.query("SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10")

