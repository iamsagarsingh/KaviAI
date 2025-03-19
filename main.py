from fastapi import FastAPI, Depends
from scheduler import start_scheduler
from sqlalchemy.orm import Session
from models import Kavita
from starlette import status
import models
from database import engine,sessionLocal
from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

app = FastAPI()
start_scheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Allows all origins; replace with specific origins for security
    allow_credentials=True,
    allow_methods=["*"],    # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)

class DataRequest(BaseModel):
    kavitaText:str = Field(min_length=3)

@app.get('/',status_code=status.HTTP_200_OK)
async def get_all(db:db_dependency):
    return db.query(Kavita).all()

@app.post('/postData/',status_code=status.HTTP_201_CREATED)
async def post_data(db:db_dependency,dataRequest:DataRequest):
    dateofcreated = getDatetime()
    kavita_model = Kavita(**dataRequest.model_dump(),DoP=dateofcreated)
    db.add(kavita_model)
    db.commit()
    
def getDatetime():
    date = datetime.now()
    return date.strftime("%Y-%m-%d %H:%M:%S")