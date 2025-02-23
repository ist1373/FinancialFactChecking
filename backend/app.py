from fastapi import FastAPI
import logging
from src.api.v1.auth import router as auth_router
from src.api.v1.document import router as document_router
from fastapi import FastAPI
from src.db.base import Base, engine



logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(document_router, prefix="/api/v1", tags=["document"])


if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)