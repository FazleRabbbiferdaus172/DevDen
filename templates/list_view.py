from fasthtml.components import *
from utils.table_utils import get_foreign_keys_table

def list_view_cell(column_name, cell_value, list_related_table_dict):
    if column_name not in list_related_table_dict.keys():
        return Td(cell_value, cls="has-text-centered")
    else:
        if cell_value:
            try:
                relational_column_cell_value = list_related_table_dict[column_name](f'id = {cell_value}')[0].name
            except Exception as e:
                print(e)
                relational_column_cell_value = list_related_table_dict[column_name](f'id = {cell_value}')[0].id
        else:
            relational_column_cell_value = ""
        return Td(relational_column_cell_value, cls="has-text-centered")

def list_view_row(record, list_related_table_dict):
    return Tr(
            *[list_view_cell(column_name, cell_value, list_related_table_dict) for column_name, cell_value in record.__dict__.items()], 
            Td(A("Edit", href=f"/admin/{record.table_name}/{record.id}"))
        )

def list_view_rows(table, list_related_table_dict):
    records =  table()
    return [list_view_row(record=record, list_related_table_dict=list_related_table_dict) for record in records]

def template_list_view(table, table_name=None, row_clickable=True):
    thead = Thead(Tr(
            *[Th(i.name, cls="has-text-centered is-capitalized") for i in table.columns],
            Th(" ", cls="has-text-centered is-capitalized")
        ))
    list_related_table_dict = get_foreign_keys_table(table)
    table_rows = list_view_rows(table, list_related_table_dict)
    tbody = Tbody(*table_rows, 
                  Tr(
                      Td(
                          A('Add New', href=f"/admin/{table_name}/new",cls="has-text-centered"),
                          colspan=len(table.columns)
                          )
                      )
                  )
    tfooter = Tfoot()
    return Div(Table(thead, tbody, tfooter, cls="table is-striped is-hoverable table is-fullwidth"), cls='table-container')