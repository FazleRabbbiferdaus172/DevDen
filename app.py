from fasthtml.common import *
import bcrypt
import logging

from models.db import db
from models.user import users
from models.project import projects
from models.profile import profiles
from models.work_experience import work_experiences
from models.social_media_link import social_media_lniks

from routes.login import get_dummy_routes

logger = logging.basicConfig(level=logging.DEBUG, format="{asctime}:{levelname} - {message}", style="{")

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(user, password: str) -> bool:
    return bcrypt.checkpw(password, user.pwd.encode('utf-8'))

login_redir = RedirectResponse('/login', status_code=303)

def before(req, sess):
    auth = req.scope['auth'] =  sess.get('auth', None)
    if not auth:
        return login_redir
    # projects.xtra(name=auth)

def _not_found(req, exc):
    return (Title('Opppsss!'), Div('Page not found.'))

def main_template(*args, **kwargs):
    nav = Nav(
        Div(Span(kwargs.get('page_title', 'Den'), cls='is-size-3 has-text-centered has-text-justified is-uppercase'), cls="navbar-brand px-2"),
        Div(
            *(A(menu, cls='navbar-item px-1') for menu in kwargs.get('menus', ['Home'])),
            cls='navbar-start'),
        Div(
                Div(
                        Div(
                                A('Login', href='/login'),
                                A('Logout', href='/logout'),
                                A('Signup', href='/signup'),
                            cls='buttons'),
                        cls='navbar-item'
                    ),
                 cls='navbar-end'
            ),
        cls='navbar has-shadow is-fixed-top'
    )
    header = Header(nav)
    main = Main(args, cls='container')
    footer = Footer('Footer', cls='navbar is-fixed-bottom',)
    body = Body(  header,
                Div(main,
                  style='padding-bottom: var(--bulma-navbar-height);'
                ),
                footer,
                cls='has-navbar-fixed-top has-navbar-fixed-bottom')
    web_client = (Title("Den"), 
                    body
                  )
    return web_client

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

def generate_about_section_public():
    return [Span("About Me -", cls='title is-capitalized is-5'),
                        Span("From Dhaka, Bangladesh -", cls='custom-block has-text-weight-semibold'),
                        Span("Currently working at Brain Station 23 Plc. -", cls='custom-block has-text-weight-semibold'),
                        Span("Enjoys building things and swimming -", cls='custom-block has-text-weight-semibold')]

def generate_how_to_reach_public():
        return [Span("Contact Me -", cls='title is-capitalized is-5'),
                        Span(Span("fazle.ferdaus1416@gmail.com "), Span(I(cls="fas fa-envelope")), Span(" -"), cls='custom-block has-text-weight-semibold'),
                        Span(Span("+880 1968628234 "), Span(I(cls="fas fa-phone")), Span(" -"),cls='custom-block has-text-weight-semibold'),
                        Span(Span("House#34, Road#7, Block#E, Mirpur-12, Dhaka, Bangladesh "), Span(I(cls="fas fa-map-pin")), Span(" -"), cls='custom-block has-text-weight-semibold')]

def main_public_template(*args, **kwargs):
    icon_list = Div(
        A(I(cls="fab fa-github fa-2x block link"), cls="link", href="https://github.com/FazleRabbbiferdaus172"),
        A(I(cls="fab fa-linkedin-in fa-2x block link"),  cls="link", href="https://www.linkedin.com/in/fazle-rabbi-ferdaus-113255185/"),
        A(I(cls="fab fa-facebook fa-2x block link"), cls="link", href="https://www.facebook.com/FazleRabbiFerdaus/"),
        cls="public-links"
    )
    nav = Nav(
        A(Span('Home', cls='is-size-5 has-text-left'), cls="side-nav selected", hx_get=f'about/page',
          hx_trigger='click',hx_target='#main-content-right',hx_swap='innerHtml'),
        Span(Span('Projects', cls='is-size-5 has-text-left'), cls="side-nav", hx_get=f'project/page?idx={1}',
          hx_trigger='click',hx_target='#main-content-right',hx_swap='innerHtml'),
        A(Span('How to reach me', cls='is-size-5 has-text-left'),  cls="side-nav", hx_get=f'contact/page',
          hx_trigger='click',hx_target='#main-content-right',hx_swap='innerHtml'),
        cls="block pt-5 pl-5 public-nav",
    )
    header = Header(H1('Fazle Rabbi Ferdaus',cls='title is-1'), H2('Software Enginner', cls='subtitle is-4'), nav, cls='block public-header public-section-left')
    about_me_section = generate_about_section_public()
    # projects = generate_infnite_scroll_list_public('project')
    main = Main(
                Div(
                    Div(
                        *about_me_section,
                        # *projects,
                        id="main-content-right"
                    ),
                cls='block content is-normal is-pullued-bottom-right public-section-right')
                )
    footer = Footer(icon_list, cls="public-footer")
    body = (Title("Ferdaus's Den"),Body(Div(header, main, cls="public"), footer)
    )
    return body

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

def template_list_view(table, table_name=None):
    thead = Thead(Tr(
            *[Th(i.name, cls="has-text-centered is-capitalized") for i in table.columns]
        ))
    tr_list =  table()
    tbody = Tbody(*tr_list, 
                  Tr(
                      Td(
                          A('Add New', href=f"/admin/{table_name}/new",cls="has-text-centered"),
                          colspan=len(table.columns)
                          )
                      )
                  )
    tfooter = Tfoot()
    return Div(Table(thead, tbody, tfooter, cls="table is-striped is-hoverable table is-fullwidth"), cls='table-container')

def template_record_create_form_view(table, table_name=None):
    '''
    <div class="field">
        <label class="label">Name</label>
        <div class="control">
            <input class="input" type="text" placeholder="e.g Alex Smith">
        </div>
    </div>
    '''
    inputs = [
        Div(
            Label(col.name, cls='label is-capitalized'),
            Div(
                Input(id=col.name, placeholder=col.name, type="text")
                ,cls='control'),
            cls='field') 
        for col in table.columns if col.name != 'id']
    frm = Div(Form(*inputs,
        Button('Create', cls='button is-primary'), action=f'/admin/{table_name}/new', method='post', cls='form'))
    
    return main_template(frm)

bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.js', r'.*\.css', r'/public/*', '/signup','/login', '/', '/project/page/', '/page/'])
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


# app.router.add_route(path='/login', endpoint=login, methods=['get'], name='signup', include_in_schema=True)
get_dummy_routes()

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

@app.post('/login')
def post(login:Login , sess):
    # important: if the first argument is 'req' it holds the request informations
    u = users(where=f"name='{login.name}'", limit=1)
    if u and check_password(u[0], login.pwd.encode("utf-8")):
        sess['auth'] = u[0].id
    else:
        return RedirectResponse('/login', status_code=303)
    print(users())
    return RedirectResponse('/admin', status_code=303)

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
