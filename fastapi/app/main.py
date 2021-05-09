from typing import Optional
import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from app.postgresql_utils import PostgreSQLManager, Query

app = FastAPI()
db = PostgreSQLManager()

@app.get("/download_csv")
async def get_csv(name: str):
    query='''
        SELECT id, name as city_name, geometry FROM vw_buildings_footprints WHERE name = %s
        '''

    df = db.query_execute(Query(query, (name,)), fetch=True, asdataframe=True)
    stream = io.StringIO()
    df.to_csv(stream, index = False)

    response = StreamingResponse(iter([stream.getvalue()]),media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response

#35.198.107.181/test?name=test