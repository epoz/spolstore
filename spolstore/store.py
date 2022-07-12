from typing import Tuple, Optional
from rdflib.term import Node, Literal, URIRef
from rdflib.graph import Graph
from rdflib.store import VALID_STORE, Store
import apsw

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS spo(s INTEGER, p INTEGER, o INTEGER);
CREATE INDEX IF NOT EXISTS spo_s ON spo(s);
CREATE INDEX IF NOT EXISTS spo_p ON spo(p);
CREATE INDEX IF NOT EXISTS spo_o ON spo(o);
CREATE TABLE IF NOT EXISTS iris(iri);
CREATE UNIQUE INDEX IF NOT EXISTS iris_u ON iris(iri);
CREATE VIRTUAL TABLE IF NOT EXISTS literals USING fts5(s UNINDEXED, p UNINDEXED, o);
"""


class StoreNotOpened(Exception):
    ...


def is_opened(func):
    def wrapd(*args, **kwargs):
        if args[0]._storepath is None:
            raise StoreNotOpened()
        return func(*args, **kwargs)

    return wrapd


class SpolStore(Store):
    context_aware = False

    def __init__(self):
        self._storepath = None

    def init_db(self):
        self._db = apsw.Connection(self._storepath)
        self._db.cursor().execute(DB_SCHEMA)

    def open(self, configuration, create: bool = False):
        self._storepath = configuration
        self.init_db()
        return VALID_STORE

    def iiri(self, rowid):
        c = self._db.cursor()
        for rowid in c.execute("SELECT iri FROM iris WHERE rowid = ?", (rowid,)):
            return URIRef(rowid[0])

    def irii(self, iri, insert_if_not_found=True):
        "Return the integer rowid for the given iri, and insert if it does not exist"
        iri = str(iri)
        c = self._db.cursor()
        for rowid in c.execute("SELECT rowid FROM iris WHERE iri = ?", (iri,)):
            return rowid[0]
        else:
            if insert_if_not_found:
                c.execute("INSERT INTO iris VALUES (?)", (iri,))
                return self._db.last_insert_rowid()
        return 0

    @is_opened
    def add(
        self,
        triple: Tuple[Node, Node, Node],
        context: Optional["Graph"],
        quoted: bool = False,
    ):
        s, p, o = triple
        ss = self.irii(s)
        pp = self.irii(p)
        if isinstance(o, Literal):
            self._db.cursor().execute(
                "INSERT INTO literals VALUES (?, ?, ?)", (ss, pp, str(o))
            )
        else:
            oo = self.irii(o)
            self._db.cursor().execute(
                "INSERT OR IGNORE INTO spo VALUES (?, ?, ?)", (ss, pp, oo)
            )

    @is_opened
    def triples(
        self,
        triple_pattern: Tuple[Optional["Node"], Optional["Node"], Optional["Node"]],
        context=None,
    ):
        s, p, o = triple_pattern
        c = self._db.cursor()
        vars = []
        stmt = []
        if isinstance(s, URIRef):
            stmt.append("s = ?")
            vars.append(self.irii(s, insert_if_not_found=False))
        if isinstance(p, URIRef):
            stmt.append("p = ?")
            vars.append(self.irii(p, insert_if_not_found=False))
        if isinstance(o, URIRef):
            stmt.append("o = ?")
            vars.append(self.irii(o, insert_if_not_found=False))
        if isinstance(o, Literal):
            stmt.append("o MATCH ?")
            vars.append(str(o))
        else:
            # If the o is not a Literal, it is either None or a iri, so query
            sql = "SELECT s, p, o FROM spo"
            if stmt:
                sql = sql + " WHERE " + " AND ".join(stmt)
            for row_s, row_p, row_o in c.execute(sql, vars):
                yield (self.iiri(row_s), self.iiri(row_p), self.iiri(row_o)), None

        sql = "SELECT s, p, o FROM literals"
        if stmt:
            sql = sql + " WHERE " + " AND ".join(stmt)
        for row_s, row_p, row_o in c.execute(sql, vars):
            yield (self.iiri(row_s), self.iiri(row_p), Literal(row_o)), None

    def __len__(self, context=None):
        c = self._db.cursor()
        spo = c.execute("SELECT COUNT(*) FROM spo").fetchone()[0]
        spl = c.execute("SELECT COUNT(*) FROM literals").fetchone()[0]
        return spo + spl
