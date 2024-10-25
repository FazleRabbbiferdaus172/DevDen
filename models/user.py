from .base_model import BaseModel
from .db import db

class User(BaseModel):
    id:int
    name:str
    pwd:str

users = db.create(User)