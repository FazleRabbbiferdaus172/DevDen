from fasthtml.common import *
import bcrypt
import logging

from models.db import db
from models.user import users
from models.project import projects
from models.profile import profiles
from models.work_experience import work_experiences
from models.social_media_link import social_media_lniks
from utils.password_utils import *

from routes.login import login_router

from templates.main_admin_template import main_template
from templates.main_public_template import main_public_template, generate_how_to_reach_public, generate_about_section_public
from templates.list_view import template_list_view
from templates.form_view import template_record_create_form_view

logger = logging.basicConfig(level=logging.DEBUG, format="{asctime}:{levelname} - {message}", style="{")

login_redir = RedirectResponse('/login', status_code=303)

def before(req, sess):
    auth = req.scope['auth'] =  sess.get('auth', None)
    if not auth:
        return login_redir
    # projects.xtra(name=auth)

def _not_found(req, exc):
    return (Title('Opppsss!'), Div('Page not found.'))

def generate_infnite_scroll_list_public(table_name, part_num=0):
    table = get_table_by_name(table_name)
    projects = table()
    list_projects = []
    if part_num == 0:
        list_projects.append(
                    Div(Span("Projects" + " -", cls="title is-4 custom-block is-capitalized"),
                    cls='block') 
                )
    for i, t in enumerate(projects):
        if i < len(projects) - 1:
            list_projects.append(
                Div(Span(t.name + " -", cls="title is-5 custom-block is-capitalized"), 
                Span(t.des, cls="custom-block is-capitalized"),
                Span(t.link, cls="custom-block"),
                cls='block') 
            )
        elif i == len(projects) - 1:
            list_projects.append(
                Div(Span(t.name + " -", cls="title is-5 custom-block is-capitalized"), 
                Span(t.des, cls="custom-block is-capitalized"),
                Span(t.link, cls="custom-block"),
                cls='block',
                get=f'page?idx={part_num + 1}',
                hx_trigger='intersect threshold:0.5 root:.is-pullued-bottom-right once',
                hx_swap='afterend'
                )
            )
    return list_projects

def find_all_tables():
    all_tables = db.tables
    return all_tables

def get_table_by_name(name):
    return next((table for table in db.tables if table.name == name), None)

def generate_tables_view_cells(tables):
    return [Div(A(t.name, href=f"/admin/{t.name}"), cls="cell is-capitalized has-text-centered") for t in tables]

def generate_tables_view_grid(tables):
    cells = generate_tables_view_cells(tables)
    return Div(Div(*cells, cls="grid"),cls="fixed-grid has-2cols")

bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.js', r'.*\.css', r'/public/*', '/signup','/login', '/', '/project/page/', '/contact/page/', '/about/page/'])
css = Style(':root {--pico-font-size:90%,--pico-font-family: Pacifico, cursive;}')
hdrs=(
    Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css', type='text/css'),
    Link(rel='stylesheet', href='./scripts/css/script.css', type='text/css'),
    Script(src='./scripts/js/main.js', defer=True),
    Script(src="https://kit.fontawesome.com/7dfe397011.js", crossorigin="anonymous")
)
app,rt = fast_app(
                  pico=False,
                  before=bware, live=False,
                  exception_handlers={404: _not_found},
                  hdrs=hdrs,
                  htmlkw={'class': 'theme-dark'})

login_router.to_app(app)

# app.router.add_route(path='/login', endpoint=login, methods=['get'], name='signup', include_in_schema=True)
# get_dummy_routes()

@app.get('/signup')
def signup():
    frm = Div(Form(Input(id='name', placeholder='Name', required=True),
        Input(id='pwd', type='password', placeholder='Password', required=True),
        Button('Signup'), action='/signup', method='post'))
    
    return main_template(frm)

@dataclass
class Login: name:str; pwd:str

@app.post('/signup')
def signup(signup:Login , sess):
    signup.pwd = hash_password(signup.pwd)
    u = users.insert(signup)
    return RedirectResponse('/login', status_code=303)

@app.get("/logout")
def logout(sess):
    del sess['auth']
    return login_redir

@app.get("/admin")
def admin_home(auth):
    tables = find_all_tables()
    tables_grid = generate_tables_view_grid(tables)
    return main_template(tables_grid)

@app.get("/admin/{table_name}")
def table_list_views(table_name: str):
    # Todo: if no table was found raise error
    try:
        table = get_table_by_name(table_name)
        list_view = template_list_view(table=table, table_name=table_name)
        return main_template(list_view)
    except NotFoundError:
        return main_template((
            H1("No Data")
        ))
    
@app.get("/admin/{table_name}/new")
def table_record_create_form(table_name: str):
    # Todo: if no table was found raise error
    table = get_table_by_name(table_name)
    crate_form_view = template_record_create_form_view(table=table, table_name=table_name)
    return main_template(crate_form_view)

@app.post("/admin/{table_name}/new")
def table_record_create_form(table_name: str, data: dict):
    table = get_table_by_name(table_name)
    u = table.insert(data)
    return RedirectResponse(f'/admin/{table_name}', status_code=303)

@app.get('/')
def Home(auth,session):
    try:
        return main_public_template()
    except NotFoundError:
        return main_public_template((
            H1("No Data")
        ))

@app.get("/project/page/")
def project(idx:int|None = 0):
    return generate_infnite_scroll_list_public('project', idx)

@app.get("/about/page/")
def about(idx:int|None = 0):
    return generate_about_section_public()

@app.get("/contact/page/")
def contact(idx:int|None = 0):
    return generate_how_to_reach_public()

# Todo: auto list view of all tables in a db with predefined coulmns implementatoin

@rt("/page/", name="page")
def get(idx:int|None = 0):
    return generate_infnite_scroll_list_public('project', idx)


if __name__ == '__main__':
    serve()
