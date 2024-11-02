from .base_model import BaseModel
from .db import db


class Project(BaseModel):
    id: int
    name: str
    des: str
    link: str
    type: str
    profile_id: int


class ProjectImage(BaseModel):
    id: int
    project_id: int
    image_data: bytes


projects = db.create(Project, foreign_keys=[("profile_id", "profile", "id")],
                     not_null=['profile_id', 'name', 'type', 'des'],
                     if_not_exists=True)
project_images = db.create(ProjectImage,
                           foreign_keys=[("project_id", "project", "id")],
                           not_null=['project_id'],
                           if_not_exists=True
                           )
