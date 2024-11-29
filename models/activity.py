from .base_model import BaseModel
from .db import db


class Activity(BaseModel):
    id:int
    type:str
    content:str