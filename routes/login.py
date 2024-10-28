from fasthtml.common import *
from fasthtml.core import APIRouter
from templates.main_admin_template import main_template
from models.user import users
from utils.password_utils import *

login_router = APIRouter()

@login_router(path='/login', methods=['get'])
def login():
    frm = Div(Form(Input(id='name', placeholder='Name', required=True),
        Input(id='pwd', type='password', placeholder='Password', required=True),
        Button('login'), action='/login', method='post'))
    
    return main_template(frm)

@dataclass
class Login: name:str; pwd:str

@login_router(path='/login', methods=['post'])
def post(login:Login , sess):
    # important: if the first argument is 'req' it holds the request informations
    u = users(where=f"name='{login.name}'", limit=1)
    if u and check_password(u[0], login.pwd.encode("utf-8")):
        sess['auth'] = u[0].id
    else:
        return RedirectResponse('/login', status_code=303)
    # print(users())
    return RedirectResponse('/admin', status_code=303)