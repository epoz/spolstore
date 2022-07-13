# SPOLStore

A Python RDFLib store that stores RDF data on a simple Subject-Predicate-Object-Literal basis, with all literals fulltext indexed using the SQLite FTS5.

## Usage

First install the package, this can be done with:

```shell
pip install spolstore
```

Before you can use it, it needs to be `opened` by specifying where on the filesystem the sqlite database containing the graph is.
To use this as a store in RDFlib, initialize and open a graph:

```python
import rdflib
g = rdflib.Graph("spol")
g.open("/tmp/example.spol")
```

If you do not open a graph first, an exception is thrown when trying to call any methods on it.

Once a graph has been parsed, you can perform fulltext searches using a SPARQL query:

```python
import rdflib
g = rdflib.Graph("spol")
g.open("/tmp/example.spol")
g.parse("http://www.w3.org/People/Berners-Lee/card")
q = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?s ?p
    WHERE {
            ?s ?p "web workshop" .
    }
"""
for r in g.query(q):
    print(r)
```

### Import an ntriples file from disk

You can also load a .nt file from disk using SPOLStore like so:

```shell
python -m spolstore example.nt example.spol
```

The file can be compressed. The script checks for an extension named .gz, and if so, will uncompress the file when reading.
If you know how many triples there are in the file, you can also specify it on the command line to see the progress.

```shell
python -m spolstore --total=6122281 abiggerfile.nt.gz someotherfile.spol
```

See [here for more Usage](docs.md) and querying as a SQL database directly.

## TODO

This is very much the first working version. Consider it a practical prototype. Probably many bugs...

- Handle languages and data types properly for Literals, in stead of the current dumb dumps
