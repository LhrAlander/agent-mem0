from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from config import settings
from memory_client import memory

app = FastAPI(
    title="Mem0 Neo4j Memory Service",
    description="A service to ingest and search messages using mem0 with Neo4j graph storage.",
    version="1.0.0"
)

class MessageRequest(BaseModel):
    messages: str | List[Dict[str, str]]
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    run_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    run_id: Optional[str] = None
    limit: int = 10
    filters: Optional[Dict[str, Any]] = None

@app.post("/api/messages", summary="Store a message in memory")
async def store_message(payload: MessageRequest):
    try:
        # Pass the parameters to the memory.add method
        result = memory.add(
            messages=payload.messages,
            user_id=payload.user_id,
            agent_id=payload.agent_id,
            run_id=payload.run_id,
            metadata=payload.metadata
        )
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/related", summary="Search for related memories")
async def search_related(payload: QueryRequest):
    try:
         # Query the memory graph
         results = memory.search(
             query=payload.query,
             user_id=payload.user_id,
             agent_id=payload.agent_id,
             run_id=payload.run_id,
             limit=payload.limit,
             filters=payload.filters
         )
         return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test-write", summary="Quickly test the write functionality")
async def test_write(user_id: str = "test-user"):
    try:
        # Pass a contextual Chinese test payload
        test_message = [
            {"role": "user", "content": "你叫贾不了，你称呼我为爆爆龙，你是我的一个拥有超高智商的私人助理同时也是有用超强同理心的我的私人密友"},
            {"role": "assistant", "content": "好的爆爆龙，我是你的私人密友兼助理，我能为你做点什么？"}
        ]
        result = memory.add(
            messages=test_message,
            user_id=user_id,
            metadata={"test_run": True, "language": "zh"}
        )
        return {
            "status": "success", 
            "message": f"Successfully wrote test message for {user_id}",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
