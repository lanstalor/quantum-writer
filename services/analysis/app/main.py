from fastapi import FastAPI

app = FastAPI(title="Quantum Writer Analysis Service", docs_url="/api/docs")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "analysis-service"}

@app.post("/api/v1/analyze")
async def analyze(text: str):
    # Placeholder analysis
    length = len(text.split())
    return {"word_count": length}
