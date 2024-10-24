from .base_model import BaseModel

class User(BaseModel):
    id:int
    name:str
    pwd:str