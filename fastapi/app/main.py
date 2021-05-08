from typing import Optional

from fastapi import FastAPI, HTTPException


app = FastAPI()

@app.get("/extract_stuff")
def todo():
    return {"TODO": "TODO"}