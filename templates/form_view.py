from fasthtml.components import *
from utils.table_utils import *

def template_record_create_form_view(table, table_name=None):
    '''
    <div class="field">
        <label class="label">Name</label>
        <div class="control">
            <input class="input" type="text" placeholder="e.g Alex Smith">
        </div>
    </div>
    '''
    inputs = []
    foreign_keys_column = []
    foreign_keys_column_table_dict = {}
    for key in table.foreign_keys:
        foreign_keys_column.append(key.column)
        foreign_keys_column_table_dict[key.column] = get_table_by_name(key.other_table)

    for col in table.columns:
        if col.is_pk:
            continue
        required = False
        if col.notnull:
            required = True
        input = []
        if col.name not in foreign_keys_column:
            input = Div(
                    Label(col.name, cls='label is-capitalized'),
                    Div(
                        Input(id=col.name, placeholder=col.name, required=required, type="text")
                        ,cls='control'),
                    cls='field')
        else:
            relational_recs = foreign_keys_column_table_dict[col.name]()
            input = Div(
                    Label(col.name, cls='label is-capitalized'),
                    Div(
                        Select(
                            *[Option(rec.name, value=rec.id) for rec in relational_recs],
                            required=required, id=col.name)
                        ,cls='select'),
                    cls='field')
        inputs.append(input)
    frm = Div(Form(*inputs,
        Button('Create', cls='button is-primary'), action=f'/admin/{table_name}/new', method='post', cls='form'))
    
    return frm

def template_record_edit_form_view(table, table_name=None, record=None):
    '''
    <div class="field">
        <label class="label">Name</label>
        <div class="control">
            <input class="input" type="text" placeholder="e.g Alex Smith">
        </div>
    </div>
    '''
    record = record.__dict__
    inputs = []
    foreign_keys_column = []
    foreign_keys_column_table_dict = {}
    for key in table.foreign_keys:
        foreign_keys_column.append(key.column)
        foreign_keys_column_table_dict[key.column] = get_table_by_name(key.other_table)

    for col in table.columns:
        if col.is_pk:
            continue
        required = False
        if col.notnull:
            required = True
        input = []
        if col.name not in foreign_keys_column:
            input = Div(
                    Label(col.name, cls='label is-capitalized'),
                    Div(
                        Input(id=col.name, value=record[col.name], required=required, type="text")
                        ,cls='control'),
                    cls='field')
        else:
            relational_recs = foreign_keys_column_table_dict[col.name]()
            input = Div(
                    Label(col.name, cls='label is-capitalized'),
                    Div(
                        Select(
                            *[Option(rec.name, value=rec.id) for rec in relational_recs],
                            required=required, id=col.name, value=record[col.name])
                        ,cls='select'),
                    cls='field')
        inputs.append(input)
    frm = Div(Form(*inputs,
        Button('Update', cls='button is-primary'), action=f'/admin/{table_name}/{id}', method='post', cls='form'))
    
    return frm