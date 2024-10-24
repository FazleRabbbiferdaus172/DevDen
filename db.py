from fastlite import *

from models.base_model import BaseModel
from models.user import User
from models.project import Project


db = database('data/den.db')

users = db.create(User)
projects = db.create(Project)