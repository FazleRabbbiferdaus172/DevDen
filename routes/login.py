from fasthtml.common import *
from fasthtml.core import APIRouter

login_router = APIRouter()

# @login_router.get('/dummy')
# def get_dummy():
#     return ("Dummy")

@login_router(path='/dummy', methods=['get'])
def get_dummy():
    return ("Dummy")