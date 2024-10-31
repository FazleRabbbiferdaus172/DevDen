from fasthtml.components import *

def generate_tables_view_cells(tables):
    return [Div(A(t.name, href=f"/admin/{t.name}"), cls="cell is-capitalized has-text-centered") for t in tables]

def generate_tables_view_grid(tables):
    cells = generate_tables_view_cells(tables)
    return Div(Div(*cells, cls="grid"),cls="fixed-grid has-2cols")