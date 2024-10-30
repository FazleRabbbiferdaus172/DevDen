from fasthtml.common import *
from fasthtml.core import APIRouter
from templates.main_admin_template import main_template
from models.user import users
from utils.password_utils import *

signup_router = APIRouter()

@signup_router(path='/signup', methods=['get'])
def signup():
    frm = Div(Form(Input(id='name', placeholder='Name', required=True),
        Input(id='pwd', type='password', placeholder='Password', required=True),
        Button('Signup'), action='/signup', method='post'))
    
    return main_template(frm)

@dataclass
class Signup: name:str; pwd:str

@signup_router(path='/signup', methods=['post'])
def signup(signup:Signup , sess):
    signup.pwd = hash_password(signup.pwd)
    u = users.insert(signup)
    return RedirectResponse('/login', status_code=303)