from .base_model import BaseModel
from .db import db

class Profile(BaseModel):
    id:int
    name:str
    title:str
    bio:str
    address:str
    phone_no:str
    user_id:int


profiles = db.create(Profile, foreign_keys=[("user_id", "user", "id")], 
                     not_null=['user_id', 'name', 'title', 'bio', 'phone_no'], 
                     if_not_exists=True)
