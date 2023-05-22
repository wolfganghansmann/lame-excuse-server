# main.py

from fastapi import FastAPI, Response
import random

app = FastAPI()

with open("excuses.txt") as fh:
    excuses = fh.read().split("\n")

@app.get("/")
async def root(output="json"):
    excuse = excuses[random.randint(0, len(excuses) - 1)]
    if output == "json":
        return {"excuse": excuse}
    else:
    	return Response(content=f"""
<html>
  <body>
  <h1>Excuse of the day:</h1>
    <p>
      <b>{excuse}</b>
    </p>
  </body>
</html>
""", media_type="text/html")
