import unittest
from rdflib import Graph, URIRef
import spolstore


class StoreTestCase(unittest.TestCase):
    def test_foaf(self):
        g = Graph("spol")
        g.open(":memory:")
        g.parse("http://www.w3.org/People/Berners-Lee/card")
        q = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        
            SELECT ?s ?p ?o
            WHERE {
                    ?s ?p "web workshop" .
                    ?s ?p ?o .
            }
        """
        result = [r for r in g.query(q)]
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0][0], URIRef("http://wiki.ontoworld.org/index.php/_IRW2006")
        )
