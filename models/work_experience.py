from .base_model import BaseModel
from .db import db

class WorkExperience(BaseModel):
    id:int
    company_name:str
    jod_title:str
    date_from:str
    date_to:str
    desciption:str
    sequence:str
    profile_id:int


work_experiences = db.create(WorkExperience)