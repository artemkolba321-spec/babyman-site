from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import requests_collection
from bson import ObjectId

app = FastAPI()

class SudoRequestModel(BaseModel):
    user: str
    command: str

@app.post("/sudo_request")
async def create_request(req: SudoRequestModel):
    result = await requests_collection.insert_one(req.dict())
    return {"id": str(result.inserted_id)}

@app.get("/requests")
async def get_requests():
    docs = await requests_collection.find().to_list(100)
    for d in docs:
        d["id"] = str(d["_id"])
        del d["_id"]
    return docs

@app.post("/approve/{request_id}")
async def approve_request(request_id: str):
    result = await requests_collection.update_one(
        {"_id": ObjectId(request_id)}, {"$set": {"status": "approved"}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Request not found")
    return {"status": "approved"}