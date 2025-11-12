from fastapi import FastAPI

app = FastAPI(title="Issue Tracker", version="0.1",)

@app.get("/")
async def root_health():
    return {"status": "I am Root"}


@app.get("/health")
async def health():
    """Health endpoint for the Issue Tracker service."""
    return {"status": "ok"}
