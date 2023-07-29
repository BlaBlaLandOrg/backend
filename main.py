from fastapi import FastAPI
from app.routes import router as api_router

def create_application() -> FastAPI:
    application = FastAPI(title="Blablaland")
    application.include_router(api_router)
    return application

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
