from .base_model import BaseModel
from .db import db

# TODO: need a column name active and also a constraint that only one record sould have active true

class Website(BaseModel):
    id:int
    name:str
    website_title:str
    user_id:int
    header_node_root_id:int
    main_node_root_id:int
    footer_node_root_id:int
    page_id:int

websites = db.create(Website, foreign_keys=[
                    ("header_node_root_id", "node", "id"),
                    ("main_node_root_id", "node", "id"),
                    ("footer_node_root_id", "node", "id"),
                    ("user_id", "user", "id"),
                    ("page_id", "website_page", "id")
                    ], 
                     not_null=['user_id'], 
                     if_not_exists=True, transform=True)
