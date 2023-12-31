
from controllers import candidate_rest_controller, user_rest_controller, company_rest_controller,\
project_rest_controller,test_rest_controller, initial_data, interview_rest_controller
import asyncio
from controllers import health_rest_controller 
from fastapi import FastAPI
from daos.db_model.db_model import Base

from daos.db_model.database import engine

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]

Base.metadata.create_all(bind=engine)
initial_data.initialize_technologies()
initial_data.initialize_abilities()


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
app.include_router(company_rest_controller.router)
app.include_router(project_rest_controller.router)
app.include_router(test_rest_controller.router)
app.include_router(interview_rest_controller.router)


