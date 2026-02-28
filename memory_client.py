import os
import openai.resources.chat
import openai.resources.embeddings
from mem0 import Memory
from config import settings

# Set OpenAI base url directly to the environment so underneath OpenAI client picks it up
if settings.OPENAI_BASE_URL:
    os.environ["OPENAI_BASE_URL"] = settings.OPENAI_BASE_URL

# Configure Mem0 with Neo4j as the graph memory provider
config = {
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": settings.NEO4J_URI,
            "username": settings.NEO4J_USERNAME,
            "password": settings.NEO4J_PASSWORD
        },
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": settings.LLM_MODEL,
            "api_key": settings.OPENAI_API_KEY,
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": settings.EMBEDDING_MODEL,
            "api_key": settings.OPENAI_API_KEY,
            "embedding_dims": settings.EMBEDDING_DIMS,
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "mem0",
            "path": "./qdrant_db",
            "embedding_model_dims": settings.EMBEDDING_DIMS,
        }
    }
}

memory = Memory.from_config(config_dict=config)
