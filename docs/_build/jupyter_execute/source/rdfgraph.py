#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pylipd.utils.rdf_graph import RDFGraph

# Load RDF file into graph
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"])
(result, result_df) = rdf.query("SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10")
print(result_df)


# In[2]:


from pylipd.utils.rdf_graph import RDFGraph

# Fetch RDF graph data for given id(s)
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
rdf.get("http://example.org/graph")


# In[3]:


from pylipd.utils.rdf_graph import RDFGraph

# Fetch RDF Graph Data
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
print(rdf.get_all_graph_ids())


# In[4]:


from pylipd.utils.rdf_graph import RDFGraph

# Load RDF file into graph
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"])
(result, result_df) = rdf.query("SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10")
print(result_df)


# In[5]:


from pylipd.utils.rdf_graph import RDFGraph

# Pop RDF graph data for given id(s)
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
popped = rdf.pop("http://example.org/graph")


# In[6]:


from pylipd.utils.rdf_graph import RDFGraph

rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"])
query = """PREFIX le: <http://linked.earth/ontology#>
        select ?s ?p ?o where {
            ?s ?p ?o
        } LIMIT 10 """
result, result_df = rdf.query(query)
print(result_df)


# In[7]:


from pylipd.utils.rdf_graph import RDFGraph

# Remove RDF graph data for given id(s)
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
rdf.remove("http://example.org/graph")


# In[8]:


from pylipd.utils.rdf_graph import RDFGraph

# Fetch RDF data
rdf = RDFGraph()
rdf.load(["../examples/rdf/graph.ttl"], graphid="http://example.org/graph")
nquads = rdf.serialize()
print(nquads[:10000])
print("...")


# In[9]:


from pylipd.utils.rdf_graph import RDFGraph

# Fetch LiPD data from remote RDF Graph
rdf = RDFGraph()
rdf.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
(result, result_df) = rdf.query("SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10")

