from fasthtml.common import *
import bcrypt
import logging

logger = logging.basicConfig(level=logging.DEBUG, format="{asctime}:{levelname} - {message}", style="{")


db = database('data/den.db')
class User:
    id:int
    name:str
    pwd:str

    def __ft__(self):
        column = Tr(
            *[Td(i, cls="has-text-centered") for i in self.__dict__.values()]
        )
        return column

class Project:
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

@app.get('/login')
def login():
    frm = Div(Form(Input(id='name', placeholder='Name', required=True),
        Input(id='pwd', type='password', placeholder='Password', required=True),
        Button('login'), action='/login', method='post'))
    
    return main_template(frm)

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
    u = users(where=f"name='{login.name}'", limit=1)
    # if not compare_digest(u.pwd.encode("utf-8"), login.pwd.encode("utf-8"))
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

@app.get("/admin")
def admin_home(auth):
    return main_template(H1("Hello admin"))


def template_list_view(table):
    num_of_cols = len(users.columns)
    title_col = Div(
            *[Div(i.name ,cls='column has-text-centered is-capitalized') for i in users.columns],
            cls='columns'
        )
    print(num_of_cols)
    data_col = users()
    return Div(title_col, *data_col, cls='block')

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