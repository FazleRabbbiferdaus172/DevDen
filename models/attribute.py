from .base_model import BaseModel
from .db import db

class Attribute(BaseModel):
    id:int
    name:str
    attr_type:str
    attr_vals:str
    node_id:int

attributes = db.create(Attribute, foreign_keys=[("node_id", "node", "id")], 
                     not_null=['node_id'], 
                     if_not_exists=True,transform=True)
