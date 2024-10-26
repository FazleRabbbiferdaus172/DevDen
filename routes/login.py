from fasthtml.components import Div

def get_dummy_routes():
    from app import app
    
    @app.get('/dummy')
    def dummy():
        return Div("Hello dummy")
    