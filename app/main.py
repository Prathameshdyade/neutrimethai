from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.database import Base, engine

app = FastAPI(title="NutriMithai API")


@app.on_event("startup")
def on_startup():
	# Ensure all DB tables for SQLAlchemy models are created
	Base.metadata.create_all(bind=engine)


app.include_router(api_router, prefix="/api/v1")
