from fastapi import FastAPI

app = FastAPI(title="Quantum Writer Auth Service", docs_url="/api/docs")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth-service"}

@app.post("/api/v1/login")
async def login(username: str, password: str):
    # Dummy authentication
    if username and password:
        return {"token": "fake-jwt"}
    return {"error": "invalid"}
