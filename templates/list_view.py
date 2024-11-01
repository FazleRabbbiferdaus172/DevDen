from fasthtml.components import *

def template_list_view(table, table_name=None, row_clickable=True):
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