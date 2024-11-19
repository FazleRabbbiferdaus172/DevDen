from .base_model import BaseModel
from .db import db

class WebsitePage(BaseModel):
    id:int
    name:str
    page_title:str
    node_id:int
    type:str
    db_table_name:str

website_pages = db.create(WebsitePage, foreign_keys=[
                    ("node_id", "node", "id"),
                    ],
                     if_not_exists=True)