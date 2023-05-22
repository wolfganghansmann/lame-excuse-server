# main.py

from fastapi import FastAPI
import random

app = FastAPI()

with open("excuses.txt") as fh:
    excuses = fh.read().split("\n")

@app.get("/")
async def root():
    return {"excuse": excuses[random.randint(0, len(excuses))]}