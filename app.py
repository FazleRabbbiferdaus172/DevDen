from fasthtml.common import *

db = database('data/den.db')
class User:
    id:int
    name:str
    pwd:str

    def __ft__(self):
        return Li(Span(self.id),Span('-'),Span(self.name), id=f'user-{self.id}')

class Project:
    name:str
    des:str
    link:str
    type:str

users = db.create(User)
projects = db.create(Project)

login_redir = RedirectResponse('/login', status_code=303)

def before(req, sess):
    auth = req.scope['auth'] =  sess.get('auth', None)
    if not auth:
        return login_redir
    # projects.xtra(name=auth)

def _not_found(req, exc):
    return (Title('Opppsss!'), Div('Page not found.'))

bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.js', r'.*\.css', '/login'])
css = Style(':root {--pico-font-size:90%,--pico-font-family: Pacifico, cursive;}')
hdrs=(picolink, css)
app,rt = fast_app(before=bware, live=True,
                  exception_handlers={404: _not_found},
                  hdrs=hdrs)

def main_template(*args):
    web_client = (Title("Den"), Main(
     args,
     cls="container"   
    ))
    return web_client

@app.get('/login')
def login():
    frm = Form(Input(id='name', placeholder='Name'),
        Input(id='pwd', type='password', placeholder='Password'),
        Button('login'), action='/login', method='post')
    
    return main_template(frm)

@dataclass
class Login: name:str; pwd:str

@app.post('/login')
def post(login:Login , sess):
    u = users(where=f"name='{login.name}'", limit=1)
    if u and u[0].name == login.name:
        sess['auth'] = u[0].name
    else:
        u = users.insert(login)
        return RedirectResponse('/login', status_code=303)
    print(users())
    return RedirectResponse('/', status_code=303)

@app.get('/')
def Home(auth,session):
    try: 
        print(users())
        ul = (Ul(*users()))
        return main_template(ul)
    except NotFoundError:
        return main_template((
            H1("No Data")
        ))

serve()