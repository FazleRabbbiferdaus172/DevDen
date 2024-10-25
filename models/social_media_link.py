from .base_model import BaseModel
from .db import db

class SocialMediaLnik(BaseModel):
    id:int
    platform_name:str
    link:str
    profile_id:int
    Platform_image_data: bytes

social_media_lniks = db.create(SocialMediaLnik)