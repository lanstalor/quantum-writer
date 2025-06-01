from fastapi import FastAPI, WebSocket

app = FastAPI(title="Quantum Writer WebSocket Service", docs_url="/api/docs")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "websocket-service"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(data)
    except Exception:
        await ws.close()
