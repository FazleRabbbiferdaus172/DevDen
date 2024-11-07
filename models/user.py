from .base_model import BaseModel
from .db import db

class User(BaseModel):
    id:int
    name:str
    pwd:str

users = db.create(User, not_null=['name', 'pwd'], 
                     if_not_exists=True)

users.create_index(["name"], unique=True, find_unique_name=True)