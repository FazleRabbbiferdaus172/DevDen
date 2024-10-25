from .base_model import BaseModel
from .db import db

class Project(BaseModel):
    id:int
    name:str
    des:str
    link:str
    type:str
    profile_id:int


class ProjectImage(BaseModel):
    id: int
    project_id: int
    image_data: bytes

projects = db.create(Project)
project_images = db.create(ProjectImage)