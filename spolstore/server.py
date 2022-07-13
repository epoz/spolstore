import aiosqlite
import rdflib
from starlette.responses import PlainTextResponse, HTMLResponse
from starlette.exceptions import HTTPException
from starlette.applications import Starlette
from .store import SpolStore
from starlette.routing import Route
from rich import print
import os, sys
import apsw

DEBUG = os.environ.get("SPOLDBPATH") != None

SPOLDBPATH = os.environ.get("SPOLDBPATH")
if not SPOLDBPATH:
    print(
        "[red]Error: [default]There is no [green]SPOLDBPATH[/green] environment variable defined."
    )
    sys.exit(1)
else:
    print(f"[green]OK:[/green]    serving [blue]{SPOLDBPATH}")
DB = apsw.Connection(SPOLDBPATH)


async def irii(request):
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
        requestConfig: { endpoint: "/sparql" },
        copyEndpointOnNewTab: false,
    });
  </script>  
  </body>
</html>
"""
        return HTMLResponse(resp)
    G = rdflib.Graph("spol")
    G.open(SPOLDBPATH)
    result = G.query(query)
    return PlainTextResponse(result.serialize(format="json"))


server = Starlette(
    debug=DEBUG,
    routes=[Route("/", irii), Route("/sparql", sparql, methods=["GET", "POST"])],
)
