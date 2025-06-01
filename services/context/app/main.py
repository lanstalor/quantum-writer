from fastapi import FastAPI

app = FastAPI(title="Quantum Writer Context Service", docs_url="/api/docs")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "context-service"}

@app.post("/api/v1/optimize")
async def optimize(text: str):
    # Return the same text for now
    return {"optimized": text}
