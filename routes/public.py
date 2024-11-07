from fasthtml.core import APIRouter
from fasthtml.common import NotFoundError
from fasthtml.components import *

from templates.main_public_template import main_public_template, generate_how_to_reach_public, generate_about_section_public, generate_project_public


public_routes = APIRouter()

# @app.get('/')
@public_routes(path='/', methods=['get'])
def Home(auth,session):
    try:
        return main_public_template()
    except NotFoundError:
        return main_public_template((
            H1("No Data")
        ))

# @app.get("")
@public_routes(path='/project/page/', methods=['get'])
def project(idx:int|None = 0):
    return generate_project_public('project', idx)

# @app.get("/about/page/")
@public_routes(path='/about/page/', methods=['get'])
def about(idx:int|None = 0):
    return generate_about_section_public()

# @app.get("/contact/page/")
@public_routes(path='/contact/page/', methods=['get'])
def contact(idx:int|None = 0):
    return generate_how_to_reach_public()

