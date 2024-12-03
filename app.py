from fasthtml.common import fast_app, serve
import logging

from models.db import db
from models.user import users
from models.profile import profiles
from models.project import projects
from models.work_experience import work_experiences
from models.social_media_link import social_media_links
from models.node import nodes
from models.attribute import attributes
from models.website_page import website_pages
from models.website import websites

from utils.password_utils import *
from utils.table_utils import *

from beforeware.auth import auth_bware

from routes.login import login_router
from routes.logout import logout_router
from routes.signup import signup_router
from routes.admin import admin_routes
from routes.public import public_routes

from templates.main_admin_template import main_template

from templates.list_view import template_list_view
from templates.form_view import template_record_create_form_view
from templates.not_found_template import _not_found
from templates.infinite_scroll_view import *

logger = logging.basicConfig(level=logging.DEBUG, format="{asctime}:{levelname} - {message}", style="{")

css = Style(':root {--pico-font-size:90%,--pico-font-family: Pacifico, cursive;}')
hdrs=(
    # Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css', type='text/css'),
    Link(rel='stylesheet', href='./scripts/css/script.css', type='text/css'),
    Script(src='./scripts/js/main.js', defer=True),
    Script(src="https://kit.fontawesome.com/7dfe397011.js", crossorigin="anonymous")
)
app,rt = fast_app(
                  pico=False,
                  before=auth_bware, live=False,
                  exception_handlers={404: _not_found},
                  hdrs=hdrs,
                  htmlkw={'class': 'theme-dark'})

login_router.to_app(app)
signup_router.to_app(app)
logout_router.to_app(app)
admin_routes.to_app(app)
public_routes.to_app(app)

if __name__ == '__main__':
    serve()
