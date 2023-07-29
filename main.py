from fastapi import FastAPI
from app.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from app.database.controller import SessionLocal, engine
from app.database.models import Base

# Create all the tables in the database according to the models
Base.metadata.create_all(bind=engine)

def create_application() -> FastAPI:
    application = FastAPI(title="Blablaland")
    application.include_router(api_router)
    return application

app = create_application()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
