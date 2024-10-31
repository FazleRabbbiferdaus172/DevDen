from fasthtml.components import *

def _not_found(req, exc):
    return (Title('Opppsss!'), Div('Page not found.'))