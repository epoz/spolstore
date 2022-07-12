import unittest
from rdflib import RDF, Graph, Namespace, Literal
import spolstore

EX = Namespace("http://example.com/")


class StoreTestCase(unittest.TestCase):
    def test_store_without_open(self):
        g = Graph("spol")
        with self.assertRaises(spolstore.StoreNotOpened) as context:
            g.add((EX.foo, RDF.type, EX.Entity))

    def test_store_with_open(self):
        g = Graph("spol")
        g.open(":memory:")
        g.add((EX.foo, RDF.type, EX.Entity))

    def test_store_len(self):
        g = self.create_and_fill_graph()
        self.assertEqual(len(g), 3)

    def test_store_match_simple(self):
        g = self.create_and_fill_graph()

    def test_store_iterator_all(self):
        g = self.create_and_fill_graph()
        triples = [t for t in g.triples((None, None, None))]
        self.assertEqual(len(triples), 3)

    def test_store_iterator_literals(self):
        g = self.create_and_fill_graph()
        triples = [t for t in g.triples((None, None, Literal("boinga")))]
        self.assertEqual(len(triples), 2)

    def test_store_iterator_subject(self):
        g = self.create_and_fill_graph()
        triples = [t for t in g.triples((EX.foo, None, None))]
        self.assertEqual(len(triples), 2)

    def test_store_iterator_predicate(self):
        g = self.create_and_fill_graph()
        triples = [t for t in g.triples((None, EX.pred2, None))]
        self.assertEqual(len(triples), 1)

    def create_and_fill_graph(self):
        g = Graph("spol")
        g.open(":memory:")
        g.add((EX.foo, EX.pred1, Literal("oinga boinga")))
        g.add((EX.zom, EX.pred2, Literal("boinga La Ti Do")))
        g.add((EX.foo, EX.pred3, EX.bar))
        return g
