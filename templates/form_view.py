from fasthtml.components import *

def template_record_create_form_view(table, table_name=None):
    '''
    <div class="field">
        <label class="label">Name</label>
        <div class="control">
            <input class="input" type="text" placeholder="e.g Alex Smith">
        </div>
    </div>
    '''
    inputs = [
        Div(
            Label(col.name, cls='label is-capitalized'),
            Div(
                Input(id=col.name, placeholder=col.name, type="text")
                ,cls='control'),
            cls='field') 
        for col in table.columns if col.name != 'id']
    frm = Div(Form(*inputs,
        Button('Create', cls='button is-primary'), action=f'/admin/{table_name}/new', method='post', cls='form'))
    
    return frm