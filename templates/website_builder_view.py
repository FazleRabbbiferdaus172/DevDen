from fasthtml.components import *

def tool_bar_section():
    div_list = [Div(f"{i}", cls='cell has-background-light tool-bar-item',  style="height: 100%;") for i in range(12)]
    grid_div = Div(*div_list, cls='grid', style="height: 60%;")
    return Div(grid_div, cls="fixed-grid has-2-cols column is-1", id="tool-bar",style="height: 100%;")

def website_preview():
    pass

def website_builder_section():
    div_list = [Div(f"{i}", cls='cell has-background-primary',  style="height: 100%;", hx_get="/grid/blocks",
    hx_trigger="click", hx_target="this", hx_swap="textConten") for i in range(12)]
    grid_div = Div(*div_list, cls='grid', style="height: 100%;")
    return Div(grid_div, cls="fixed-grid has-3-cols column", style="height: 100%;")

def website_builder_view():
    tool_bar = tool_bar_section()
    builder_section = website_builder_section()
    return Div(tool_bar, builder_section, cls="columns")