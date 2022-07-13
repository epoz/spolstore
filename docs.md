# More Usage

## Querying the database directly

For applications that need to do bulk data reconciliation, it is useful to query the SPOLstore database directly,
and not do access via a HTTP or SPARQL interface.

The database schema for a SPOLStore is conceptually very simple:

```sql
CREATE TABLE IF NOT EXISTS spo(s INTEGER, p INTEGER, o INTEGER);
CREATE TABLE IF NOT EXISTS iris(iri);
CREATE VIRTUAL TABLE IF NOT EXISTS literals USING fts5(s UNINDEXED, p UNINDEXED, o);
```

And there are some simple indices defined:

```sql
CREATE UNIQUE INDEX IF NOT EXISTS iris_u ON iris(iri);
CREATE INDEX IF NOT EXISTS spo_s ON spo(s);
CREATE INDEX IF NOT EXISTS spo_p ON spo(p);
CREATE INDEX IF NOT EXISTS spo_o ON spo(o);
```

So, given an index database, for example the FOAF entries from earlier in this readme, the database can be queried:

```python
import sqlite3
db = sqlite3.connect("/tmp/example.spol")
db.execute("select iris.iri, literals.o from iris inner join literals on iris.rowid = literals.s where o match 'Lee'")

http://www.w3.org/People/Berners-Lee/card|Tim Berners-Lee's FOAF file
https://timbl.com/timbl/Public/friends.ttl|Tim Berners-Lee's editable profile
https://www.w3.org/People/Berners-Lee/card#i|Tim Berners-Lee
https://www.w3.org/People/Berners-Lee/card#i|https://www.w3.org/People/Berners-Lee/card#i
https://www.w3.org/People/Berners-Lee/card#i|Tim Berners-Lee
https://www.w3.org/People/Berners-Lee/card#i|Berners-Lee
https://www.w3.org/People/Berners-Lee/card#i|Timothy Berners-Lee
```
