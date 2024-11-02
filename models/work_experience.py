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


work_experiences = db.create(WorkExperience,
                           foreign_keys=[("profile_id", "profile", "id")],
                           not_null=['company_name', 'jod_title', 'desciption', 'profile_id'],
                           if_not_exists=True)