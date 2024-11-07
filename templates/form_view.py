from collections import namedtuple

from fasthtml.components import *
from utils.table_utils import *


valid_modes = ['create', 'edit', 'read']

def get_form_input(col, mode='create', record=None, required=False, field_type=None):
    value = None
    if record:
        value = record[col.name]
    return Input(id=col.name, value=value, required=required, type="text")

def form_fields(table, table_name=None, mode='create', record=None):
    form_related_fields_dict = get_table_related_fields(table=table)
    field_list = []
    for col in table.columns:
        if col.is_pk:
            continue
        required = False
        if col.notnull:
            required = True
        input = []
        if col.name not in form_related_fields_dict['foreign_keys_column']:
            input = Div(
                    Label(col.name, cls='label is-capitalized'),
                    Div(
                        get_form_input(col=col, mode=mode, required=required, record=record),
                        # Input(id=col.name, placeholder=col.name, required=required, type="text"),
                        cls='control'),
                    cls='field')
        else:
            relational_recs = form_related_fields_dict['foreign_keys_column_records_dict'][col.name]
            input = Div(
                    Label(col.name, cls='label is-capitalized'),
                    Div(
                        Select(
                            *[Option(rec.name, value=rec.id) for rec in relational_recs],
                            required=required, id=col.name)
                        ,cls='select'),
                    cls='field')
        field_list.append(input)
    return field_list

def template_record_create_form_view(table, table_name=None):
    inputs = form_fields(table=table, table_name=table_name, mode='create')
    frm = Div(Form(*inputs,
        Button('Create', cls='button is-primary'), action=f'/admin/{table_name}/new', method='post', cls='form'))
    
    return frm

def template_record_edit_form_view(table, table_name=None, record=None):
    record = record.__dict__
    id = record['id']
    inputs = form_fields(table=table, table_name=table_name, mode='create', record=record)
    frm = Div(Form(*inputs,
        Button('Update', cls='button is-primary'), action=f'/admin/{table_name}/{id}', method='post', cls='form'))
    
    return frm

def template_form_view(table_name=None, mode='create', record_id=None):
    table = get_table_by_name(table_name)
    record = None
    if record_id:
        # TODO: remove this.
        get_one_2_many_values_by_id(table, res_id=record_id)
        record = table[record_id]
    if mode not in valid_modes:
        raise Exception(f"{mode} is not a valid mode. Valid modes are {valid_modes}")
    if mode == "create":
        return template_record_create_form_view(table=table, table_name=table_name)
    elif mode == "edit":
        return template_record_edit_form_view(table, table_name=table_name, record=record)
    elif mode == "read":
        return template_record_edit_form_view(table, table_name=table_name, record=record)
    else:
        raise Exception("No method implmemented for this mode")