from collections import defaultdict

from fasthtml import components as ftc
from fasthtml.components import *
from templates.infinite_scroll_view import generate_infnite_scroll_list_public
from utils.table_utils import *

def generate_about_section_public():
    return [Span("About Me -", cls='title is-capitalized is-5'),
            Span("From Dhaka, Bangladesh -",
                 cls='custom-block has-text-weight-semibold'),
            Span("Currently working at Brain Station 23 Plc. -",
                 cls='custom-block has-text-weight-semibold'),
            Span("Enjoys building things and swimming -", cls='custom-block has-text-weight-semibold')]

def generate_project_public(table_name='project', part_num=0):
    return generate_infnite_scroll_list_public('project', part_num)

def generate_how_to_reach_public():
    return [Span("Contact Me -", cls='title is-capitalized is-5'),
            Span(Span("fazle.ferdaus1416@gmail.com "), Span(I(cls="fas fa-envelope")),
                 Span(" -"), cls='custom-block has-text-weight-semibold'),
            Span(Span("+880 1968628234 "), Span(I(cls="fas fa-phone")),
                 Span(" -"), cls='custom-block has-text-weight-semibold'),
            Span(Span("House#34, Road#7, Block#E, Mirpur-12, Dhaka, Bangladesh "), Span(I(cls="fas fa-map-pin")), Span(" -"), cls='custom-block has-text-weight-semibold')]

def generate_header_title():
    title = H1('Fazle Rabbi Ferdaus', cls='title is-1')     
    return title

def generate_header_subtitle():
    subtitle = H2('Software Enginner', cls='subtitle is-4')
    return subtitle

def generate_header_nav():
    nav = Nav(
        A(Span('Home', cls='is-size-5 has-text-left'), cls="side-nav selected", hx_get=f'about/page/',
          hx_trigger='click', hx_target='#main-content-right', hx_swap='innerHtml'),
        A(Span('Projects', cls='is-size-5 has-text-left'), cls="side-nav", hx_get=f'project/page/?idx={1}',
             hx_trigger='click', hx_target='#main-content-right', hx_swap='innerHtml'),
        A(Span('How to reach me', cls='is-size-5 has-text-left'),  cls="side-nav", hx_get=f'contact/page/',
          hx_trigger='click', hx_target='#main-content-right', hx_swap='innerHtml'),
        cls="block pt-5 pl-5 public-nav",
    )
    return nav

def generate_public_header(header_root_node, node_table, attribute_table):
    header = get_element_from_root(header_root_node, node_table, attribute_table)
    # header = Header(
    #     generate_header_title(), 
    #     generate_header_subtitle(), 
    #     generate_header_nav(), 
    #     cls='block public-header public-section-left')
    return header

def get_element_from_root(node, node_table, attribute_table):
    element = get_element_from_node_dfs(node.__dict__, node_table, attribute_table)
    return element

def get_element_from_node_dfs(node, node_table, attrubute_table):
    attribute_record = attrubute_table(f"node_id = {node['id']}")
    if attribute_record:
        attribute_record = attribute_record[0].__dict__
    child_nodes = list(node_table.rows_where(f'parent_node_id = {node["id"]}'))
    if not child_nodes:
        element = node['tag']
        if hasattr(ftc, node['tag']):
            if node['type'] == 'record':
                query_string = f"id = {node['db_table_row']}"
                content_table_row = get_table_by_name(node['db_table_name'])(query_string)[0].__dict__
                content = content_table_row[node['db_table_column']]
            elif node['type'] == 'static':
                content = node['content']
            else:
                content = 'N/A'
            if attribute_record:
                element = getattr(ftc, node['tag'])(content, **{'cls':attribute_record['attr_vals']})
            else:
                element = getattr(ftc, node['tag'])(content, **{'cls':attribute_record['attr_vals']})
        return element
    child_args = []
    for child_node in child_nodes:
        child_arg = get_element_from_node_dfs(child_node, node_table, attrubute_table)
        child_args.append(child_arg)
    if hasattr(ftc, node['tag'].capitalize()):
        element = getattr(ftc, node['tag'])(*child_args ,node['content'], **{'cls':attribute_record['attr_vals']})
    return element

def generate_default_public_main_content():
    return generate_about_section_public()

def generate_public_main():
    default_main_content = generate_default_public_main_content()
    main = Main(
        Div(
            Div(
                *default_main_content,
                id="main-content-right"
            ),
            cls='block content is-normal is-pullued-bottom-right public-section-right')
    )
    return main

def generate_public_footer_content():
    icon_list = Div(
        A(I(cls="fab fa-github fa-2x block link"), cls="link",
          href="https://github.com/FazleRabbbiferdaus172"),
        A(I(cls="fab fa-linkedin-in fa-2x block link"),  cls="link",
          href="https://www.linkedin.com/in/fazle-rabbi-ferdaus-113255185/"),
        A(I(cls="fab fa-facebook fa-2x block link"), cls="link",
          href="https://www.facebook.com/FazleRabbiFerdaus/"),
        cls="public-links"
    )
    return icon_list

def generate_public_footer():
    footer_content = generate_public_footer_content()
    footer = Footer(footer_content, cls="public-footer")
    return footer

def main_public_template(*args, **kwargs):
    website = get_table_by_name('website')
    record = website[1]
    node = get_table_by_name('node')
    attribute = get_table_by_name('attribute')
    header = generate_public_header(node[record.header_node_root_id],
                                    node, attribute_table=attribute)
    main = generate_public_main()
    footer = generate_public_footer()
    body = (Title("Ferdaus's Den"), Body(Div(header, main, cls="public"), footer)
            )
    return body
