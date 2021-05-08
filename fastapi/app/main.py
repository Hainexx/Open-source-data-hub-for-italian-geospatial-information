from typing import Optional

from fastapi import FastAPI, HTTPException


app = FastAPI()

@app.get("/test")
def todo(name: str):
    query='''
        SELECT id FROM tb_nations WHERE name = %s
    '''
    return {'id': db.query_execute(Query(query, (name,)), fetch=True, aslist=True)[0]}