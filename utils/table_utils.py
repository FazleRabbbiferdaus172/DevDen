from models.db import db

def get_table_by_name(name):
    return next((table for table in db.tables if table.name == name), None)

def find_all_tables():
    all_tables = db.tables
    return all_tables

def get_foreign_keys_column(table):
    foreign_keys_column = []
    for key in table.foreign_keys:
        foreign_keys_column.append(key.column)
    return foreign_keys_column

def get_foreign_keys_table(table):
    foreign_keys_column_table_dict = {}
    for key in table.foreign_keys:
        foreign_keys_column_table_dict[key.column] = get_table_by_name(key.other_table)
    return foreign_keys_column_table_dict

def get_all_records_of_raltional_field(table, columns=['id', 'name'], id=None):
    foreign_keys_column_records_dict = {}
    foreign_keys_column_table_dict = get_foreign_keys_table(table=table)
    for column, column_table in foreign_keys_column_table_dict.items():
        foreign_keys_column_records_dict[column] = column_table(id)
    return foreign_keys_column_records_dict

def get_table_related_fields(table, columns=['id', 'name'], id=None):
    return {
        'foreign_keys_column': get_foreign_keys_column(table),
        'foreign_keys_column_table_dict': get_foreign_keys_table(table),
        'foreign_keys_column_records_dict': get_all_records_of_raltional_field(table, columns=columns, id=id)
    }