from controllers import candidate_rest_controller, user_rest_controller

from controllers import health_rest_controller 
from fastapi import FastAPI
from daos.db_model.db_model import Base

from daos.db_model.database import engine

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidate_rest_controller.router)
app.include_router(user_rest_controller.router)
app.include_router(health_rest_controller.router)