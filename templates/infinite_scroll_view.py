from utils.table_utils import *
from fasthtml.components import *

def generate_infnite_scroll_list_public(table_name, part_num=0):
    table = get_table_by_name(table_name)
    projects = table()
    list_projects = []
    if part_num == 0:
        list_projects.append(
                    Div(Span("Projects" + " -", cls="title is-4 custom-block is-capitalized"),
                    cls='block') 
                )
    for i, t in enumerate(projects):
        if i < len(projects) - 1:
            list_projects.append(
                Div(Span(t.name + " -", cls="title is-5 custom-block is-capitalized"), 
                Span(t.des, cls="custom-block is-capitalized"),
                Span(t.link, cls="custom-block"),
                cls='block') 
            )
        elif i == len(projects) - 1:
            list_projects.append(
                Div(Span(t.name + " -", cls="title is-5 custom-block is-capitalized"), 
                Span(t.des, cls="custom-block is-capitalized"),
                Span(t.link, cls="custom-block"),
                cls='block',
                hx_get=f'{table_name}/page/?idx={part_num + 1}',
                hx_trigger='intersect threshold:0.5 root:.is-pullued-bottom-right once',
                hx_swap='afterend'
                )
            )
    return list_projects
