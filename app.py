from fasthtml.common import *
import bcrypt
import logging

logger = logging.basicConfig(level=logging.DEBUG, format="{asctime}:{levelname} - {message}", style="{")


db = database('data/den.db')

class BaseForTable:
    
    def __ft__(self):
        column = Tr(
            *[Td(i, cls="has-text-centered") for i in self.__dict__.values()]
        )
        return column

class User(BaseForTable):
    id:int
    name:str
    pwd:str

class Project(BaseForTable):
    id:int
    name:str
    des:str
    link:str
    type:str

users = db.create(User)
projects = db.create(Project)

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

def find_all_tables():
    all_tables = db.tables
    return all_tables

def get_table_by_name(name):
    return next((table for table in db.tables if table.name == name), None)

def generate_tables_view_cells(tables):
    logging.debug(type(tables))
    return [Div(t.name, cls="cell is-capitalized has-text-centered") for t in tables]

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

bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.js', r'.*\.css', r'/public/*', '/signup','/login', '/'])
css = Style(':root {--pico-font-size:90%,--pico-font-family: Pacifico, cursive;}')
hdrs=(
    Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css', type='text/css'),
    Style("html { height: 100%; margin: 0; overflow: auto} body { height: 100%; margin: 0;}")
)
app,rt = fast_app(
                  pico=False,
                  before=bware, live=True,
                  exception_handlers={404: _not_found},
                  hdrs=hdrs)

@app.get('/login')
def login():
    frm = Div(Form(Input(id='name', placeholder='Name', required=True),
        Input(id='pwd', type='password', placeholder='Password', required=True),
        Button('login'), action='/login', method='post'))
    
    return main_template(frm)

# app.router.add_route(path='/login', endpoint=login, methods=['get'], name='signup', include_in_schema=True)

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
        sess['auth'] = u[0].name
    else:
        return RedirectResponse('/login', status_code=303)
    print(users())
    return RedirectResponse('/admin', status_code=303)

@app.get("/logout")
def logout(sess):
    del sess['auth']
    return login_redir

def find_all_tables():
    all_tables = db.tables
    return all_tables

def generate_tables_view_cells(tables):
    logging.debug(type(tables))
    return [Div(t.name, cls="cell is-capitalized has-text-centered") for t in tables]

def generate_tables_view_grid(tables):
    cells = generate_tables_view_cells(tables)
    return Div(Div(*cells, cls="grid"),cls="fixed-grid has-2cols")

@app.get("/admin")
def admin_home(auth):
    tables = find_all_tables()
    tables_grid = generate_tables_view_grid(tables)
    return main_template(tables_grid)

@app.get("/admin/{table_name}")
def table_list_views(table_name: str):
    try:
        table = next((table for table in db.tables if table.name == table_name), None)
        list_view = template_list_view(table=table)
        return main_template(list_view)
    except NotFoundError:
        return main_template((
            H1("No Data")
        ))


def template_list_view(table):
    thead = Thead(Tr(
            *[Th(i.name, cls="has-text-centered is-capitalized") for i in table.columns]
        ))
    tr_list =  table()
    tbody = Tbody(*tr_list)
    tfooter = Tfoot()
    return Div(Table(thead, tbody, tfooter, cls="table is-striped is-hoverable table is-fullwidth"), cls='table-container')

@app.get('/')
def Home(auth,session):
    try:
        list_view = template_list_view(users)
        return main_template(list_view)
    except NotFoundError:
        return main_template((
            H1("No Data")
        ))

# Todo: auto list view of all tables in a db with predefined coulmns implementatoin

serve()