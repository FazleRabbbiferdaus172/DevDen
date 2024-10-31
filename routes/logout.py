
from fasthtml.core import APIRouter
from utils.redirect_uits import login_redir

logout_router = APIRouter()

@logout_router(path="/logout", methods=['get'])
def logout(sess):
    del sess['auth']
    return login_redir