from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core import settings
from ypy_websocket import WebsocketServer
from ypy_websocket.ystore import MemoryYStore

ystore = MemoryYStore()
ws_server = WebsocketServer(ystore=ystore)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="Quantum Writer WebSocket Service", version="2.0.0", docs_url="/api/docs", redoc_url="/api/redoc", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.SERVICE_NAME}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await ws_server.serve(websocket, room_id)

