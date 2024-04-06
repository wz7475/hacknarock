from fastapi import FastAPI
import app.models as models
from app.database import engine
from app.router import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
