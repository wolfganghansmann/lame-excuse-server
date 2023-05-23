import random
import os
from fastapi import FastAPI, Response

app = FastAPI()

with open("excuses.txt") as fh:
    excuses = fh.read().split("\n")

@app.get("/")
async def root(output="json"):

    excuse = excuses[random.randint(0, len(excuses) - 1)]
    hostname = os.getenv("HOSTNAME")

    if output == "json":
        return {"excuse": excuse, "served_by": hostname}
    else:
    	return Response(content=f"""
<html>
  <body>
  <h1>Excuse of the day:</h1>
    <p>
      <b>{excuse}</b>
    </p>
    <p>
    Excuse happily served by pod <code>{hostname}</code>.
    </p>
  </body>
</html>
""", media_type="text/html")
