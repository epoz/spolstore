import rdflib
from starlette.responses import PlainTextResponse, HTMLResponse
from starlette.exceptions import HTTPException
from starlette.applications import Starlette
from .store import SpolStore
from starlette.routing import Route
from rich import print
import os, sys
import apsw

DEBUG = os.environ.get("DEBUG") != None

DB = None
SPOLDBPATH = os.environ.get("SPOLDBPATH")
if SPOLDBPATH:
    print(f"[green]OK:[/green]    serving [blue]{SPOLDBPATH}")
    DB = apsw.Connection(SPOLDBPATH)
    c = DB.cursor()
    c.execute("PRAGMA journal_mode=wal")

SPARQL_ENDPOINT = os.environ.get("SPARQL_ENDPOINT", "/sparql")


async def irii(request):
    if DB is None:
        raise HTTPException(500, detail="A SPOLDBPATH is not configured")
    if "irii" not in request.query_params:
        raise HTTPException(404, detail="An irii parameter is not included")
    c = DB.cursor()
    row = c.execute(
        "SELECT rowid FROM iris WHERE iri = ?", (request.query_params["irii"],)
    ).fetchone()
    if row is None:
        c.execute("INSERT INTO iris VALUES (?)", (request.query_params["irii"],))
        rowid = DB.last_insert_rowid()
    else:
        rowid = row[0]

    return PlainTextResponse(str(rowid))


async def sparql(request):
    if DB is None:
        raise HTTPException(500, detail="A SPOLDBPATH is not configured")
    query = request.query_params.get("query")
    if request.method == "POST":
        form = await request.form()
        query = form.get("query")
    if not query:
        resp = """<!DOCTYPE html>
<html lang="en">
  <head>
<link href="https://unpkg.com/@triply/yasgui/build/yasgui.min.css" rel="stylesheet" type="text/css" />
<script src="https://unpkg.com/@triply/yasgui/build/yasgui.min.js"></script>
<style>
  .yasgui .autocompleteWrapper {
    display: none !important;
  }
</style>  
  </head>
  <body>
  <div id="yasgui"></div>
  <script>
    const yasgui = new Yasgui(document.getElementById("yasgui"), {
        requestConfig: { endpoint: '{{SPARQL_ENDPOINT}}' },
        copyEndpointOnNewTab: false,
    });
  </script>  
  </body>
</html>
"""
        resp = resp.replace("{{SPARQL_ENDPOINT}}", SPARQL_ENDPOINT)
        return HTMLResponse(resp)
    G = rdflib.Graph("spol")
    G.open(SPOLDBPATH)
    result = G.query(query)
    return PlainTextResponse(
        result.serialize(format="json"), headers={"Access-Control-Allow-Origin": "*"}
    )


server = Starlette(
    debug=DEBUG,
    routes=[Route("/", irii), Route("/sparql", sparql, methods=["GET", "POST"])],
)
