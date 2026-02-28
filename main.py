from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import traceback
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
        print(f"\n[ERROR] /api/messages/related failed.")
        print(f"[PAYLOAD] query: '{payload.query}', user_id: {payload.user_id}, agent_id: {payload.agent_id}")
        print(f"[TRACEBACK] \n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Search related failed: {str(e)}\nMake sure all required Mem0 models (LLM/embedding) are configured and Qdrant/Neo4j can be reached.")

@app.get("/api/test-write", summary="Quickly test the write functionality")
async def test_write(user_id: str = "test-user"):
    try:
        # Pass a contextual Chinese test payload
        test_message = [
            {"role": "user", "content": "助理的名字是贾不了，用户的昵称是爆爆龙，助理是用户的私人助理和密友"},
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
