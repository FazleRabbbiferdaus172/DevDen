from fasthtml.common import Beforeware
from utils.redirect_uits import login_redir

def before(req, sess):
    auth = req.scope['auth'] =  sess.get('auth', None)
    if not auth:
        return login_redir
    
auth_bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.js', r'.*\.css', r'/public/*', '/signup','/login', '/', '/project/page/', '/contact/page/', '/about/page/'])