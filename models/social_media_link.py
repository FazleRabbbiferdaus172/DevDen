from .base_model import BaseModel
from .db import db

class SocialMediaLink(BaseModel):
    id:int
    platform_name:str
    link:str
    profile_id:int
    Platform_image_data: bytes

social_media_links = db.create(SocialMediaLink,
                           foreign_keys=[("profile_id", "profile", "id")],
                           not_null=['profile_id', 'platform_name', 'link'],
                           if_not_exists=True)