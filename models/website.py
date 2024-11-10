from .base_model import BaseModel
from .db import db


class Node(BaseModel):
    id:int
    name:str
    type:str
    content:str
    link_path:str
    table_name:str
    table_column:str
    table_row:str
    node_id:int

nodes = db.create(Node, foreign_keys=[("node_id", "node", "id")], 
                     not_null=['type'], 
                     if_not_exists=True)


class Website(BaseModel):
    id:int
    user_id:int
    header_title_id:int
    header_sub_title_id:int


websites = db.create(Website, foreign_keys=[
                    ("header_title_id", "node", "id"),
                    ("header_sub_title_id", "node", "id"),
                    ("user_id", "user", "id")
                    ], 
                     not_null=['user_id'], 
                     if_not_exists=True)


possible_types = ['static', 'link', 'node', 'dynamic']


    