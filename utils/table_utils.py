from models.db import db

def get_table_by_name(name):
    return next((table for table in db.tables if table.name == name), None)

def find_all_tables():
    all_tables = db.tables
    return all_tables