from fasthtml.components import *
from fasthtml.core import APIRouter
from fasthtml.common import NotFoundError

from utils.table_utils import *
from templates.main_admin_template import main_template
from templates.grid_view import generate_tables_view_grid
from templates.list_view import template_list_view
from templates.form_view import template_form_view
from templates.website_builder_view import website_builder_view
from utils.redirect_uits import RedirectResponse

admin_routes = APIRouter()

@admin_routes(path="/admin/build/website", methods=['get'])
def admin_build_website(auth):
    website_builder = website_builder_view()
    return website_builder

# @app.get("/admin")
@admin_routes(path="/admin", methods=['get'])
def admin_home(auth):
    tables = find_all_tables()
    tables_grid = generate_tables_view_grid(tables)
    return main_template(tables_grid)

# @app.get("/")
@admin_routes(path="/admin/{table_name}", methods=['get'])
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
    except:
        return main_template((
            H1("No Data")
        ))
    
# @app.get("/admin/{table_name}/new")
@admin_routes(path="/admin/{table_name}/new", methods=['get'])
def table_record_create_form(table_name: str):
    form_view = template_form_view(table_name=table_name, mode='create')
    return main_template(form_view)

@admin_routes(path="/admin/{table_name}/{id}", methods=['get'])
def table_record_create_form(table_name: str, id: int):
    form_view = template_form_view(table_name=table_name, mode='edit', record_id=id)
    return main_template(form_view)

@admin_routes(path="/admin/{table_name}/new", methods=['post'])
def table_record_create_form(table_name: str, data: dict):
    table = get_table_by_name(table_name)
    table.insert(data)
    return RedirectResponse(f'/admin/{table_name}', status_code=303)

@admin_routes(path="/admin/{table_name}/{id}", methods=['post'])
def table_record_create_form(table_name: str, data: dict, id: int):
    table = get_table_by_name(table_name)
    table.update(updates=data, pk_values=id)
    return RedirectResponse(f'/admin/{table_name}', status_code=303)