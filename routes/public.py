from fasthtml.core import APIRouter, HttpHeader
from fasthtml.common import NotFoundError
from fasthtml.components import *

from templates.main_public_template import main_public_template, generate_page, generate_how_to_reach_public, generate_about_section_public, generate_project_public


public_routes = APIRouter()

@public_routes(path='/', methods=['get'])
def Home(auth,session):
    try:
        return main_public_template()
    except NotFoundError:
        return main_public_template((
            H1("No Data")
        ))

@public_routes(path='/page/{page_name}/', methods=['get'])
def page(page_name: str, fragment_num:int|None = 0):
    return generate_page(page_name, fragment_num=fragment_num)


@public_routes(path='/grid/blocks', methods=['get'])
def grid_blocks(req):
    x_localstorage_data = req.headers["x_localstorage_data"]
    return x_localstorage_data