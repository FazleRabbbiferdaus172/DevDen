from .base_model import BaseModel
from .db import db

class WebsitePage(BaseModel):
    id:int
    name:str
    page_title:str
    node_id:int
    type:str
    page_link:str
    active_status:bool
    db_table_name:str

website_pages = db.create(WebsitePage, foreign_keys=[
                    ("node_id", "node", "id"),
                    ])