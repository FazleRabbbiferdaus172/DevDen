from fasthtml.components import *

def tool_bar_section():
    pass

def website_preview():
    pass

def website_builder_section():
    pass

def website_builder_view():
    div_list = [Div(f"{i}", cls='cell has-background-primary',  style="height: 100%;") for i in range(12)]
    grid_div = Div(*div_list, cls='grid', style="height: 100%;")
    return Div(grid_div, cls="fixed-grid has-3-cols", style="height: 100%;")