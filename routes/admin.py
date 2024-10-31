from fasthtml.common import *
from fasthtml.core import APIRouter
from templates.main_admin_template import main_template

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