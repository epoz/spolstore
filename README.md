# SPOLStore

A Python RDFLib store that stores RDF data on a simple Subject-Predicate-Object-Literal basis, with all literals fulltext indexed using the SQLite FTS5.

## Usage

To use this as a store in RDFlib, initialize and open a graph:

```python
import rdflib
g = rdflib.Graph(store="spol")
```

Before you can use it, it needs to be `opened` by specifying where on the filesystem the sqlite database containing the graph is.

```python
import rdflib
g = rdflib.Graph(store="spol")
g.open("/tmp/mygraph.spol")
```

If you do not open a graph first, an exception is thrown when trying to call any methods on it.

Once a graph has been parsed, you can perform fulltext searches using a SPARQL query:

```python
import rdflib
g = rdflib.Graph(store="spol")
g.open("/tmp/mygraph.spol")
g.parse("http://www.w3.org/People/Berners-Lee/card")
q = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?s ?p ?o
    WHERE {
            ?s ?p "web workshop" .
            ?s ?p ?o .
    }
"""
for r in g.query(q):
    print(r)
```
