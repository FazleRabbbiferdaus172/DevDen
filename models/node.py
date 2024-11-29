from .base_model import BaseModel
from .db import db

possible_types = ['static', 'link', 'node', 'dynamic']

# TODO: add another field priority/sequence that will determine which record renders first?
# TODO: Remove the link_path field?
class Node(BaseModel):
    id:int
    name:str
    tag:str
    type:str
    content:str
    link_path:str
    db_table_name:str
    db_table_column:str
    db_table_row:str
    parent_node_id:int

nodes = db.create(Node, foreign_keys=[("parent_node_id", "node", "id")], 
                     not_null=['type'], 
                     if_not_exists=True)