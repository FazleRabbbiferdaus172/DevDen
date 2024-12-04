from fasthtml.core import APIRouter
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

@public_routes(path='/home/no/no', methods=['get'])
def Home(auth,session):
    try:
        return main_public_template()
    except NotFoundError:
        return main_public_template((
            H1("No Data")
        ))

@public_routes(path='/home/no', methods=['get'])
def Home(auth,session):
    try:
        return main_public_template()
    except NotFoundError:
        return main_public_template((
            H1("No Data")
        ))
    
@public_routes(path='/home', methods=['get'])
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
    # if page_name == 'project':
    #     return generate_page(page_name, fragment_num=fragment_num)
    # elif page_name == 'about':
    #     return generate_about_section_public()
    # elif page_name == 'contact':
    #     return generate_how_to_reach_public()