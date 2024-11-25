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

def generate_public_header(header_root_node, node_table, attribute_table):
    header = get_element_from_root(header_root_node, node_table, attribute_table)
    return header

def get_element_from_root(node, node_table, attribute_table):
    element = get_element_from_node_dfs(node.__dict__, node_table, attribute_table)
    return element

def get_attribute(node, attrubute_table):
    attribute_records_dict = {}
    attribute_records = attrubute_table(f"node_id = {node['id']}")
    if attribute_records:
        for record in attribute_records:
            # record = record.__dict__
            if record.attr_type not in attribute_records_dict:
                attribute_records_dict[record.attr_type] = record.attr_vals
            else:
                attribute_records_dict[record.attr_type] +=  " " + record.attr_vals
    return attribute_records_dict

def get_tag(node):
    if hasattr(ftc, node['tag'].capitalize()):
        return getattr(ftc, node['tag'])
    else:
        raise Exception("Tag not found!!!!!!!!")

def generate_record_element(node, attribute, tag, child_args):
    query_string = f"id = {node['db_table_row']}"
    content_table_row = get_table_by_name(node['db_table_name'])(query_string)[0].__dict__
    content = [content_table_row[node['db_table_column']]] + child_args
    return tag(*content, **attribute)

def generate_staic_element(node, attribute, tag, child_args):
    content = [node['content']] + child_args
    return tag(*content, **attribute)

def generate_link_element(node, attribute, tag, child_args):
    # TODO: REMOVE this, no need of this as links href or htmx things could be handled by attribute
    content = []
    if node['content']:
        content.append(node['content'])
    content += child_args
    link = node['link_path']
    return tag(*content, **attribute)

def generate_element_by_type(node, attribute, tag, child_args=[]):
    if node['type'] == 'record':
        return generate_record_element(node, attribute, tag, child_args)
    elif node['type'] == 'static':
        return generate_staic_element(node, attribute, tag, child_args)
    elif node['type'] == 'link':
        return generate_link_element(node, attribute, tag, child_args)
    else:
        return generate_staic_element(node, attribute, tag, child_args)

def generate_leaf_element(node, attribute, tag):
    element = generate_element_by_type(node, attribute, tag)
    return element

def generate_parent_element(node, child_args, attribute, tag):
    return generate_element_by_type(node, attribute, tag, child_args)

def generate_node_element(node,  attribute, is_leaf=True, child_args=[]):
    tag = get_tag(node=node)
    element = tag()
    if not is_leaf:
        element = generate_parent_element(node=node, child_args=child_args, attribute=attribute, tag=tag)
    else:
        element = generate_leaf_element(node=node, attribute=attribute, tag=tag)
    return element

def get_element_from_node_dfs(node, node_table, attrubute_table):
    attribute_record = get_attribute(node, attrubute_table)

    child_nodes = list(node_table.rows_where(f'parent_node_id = {node["id"]}'))
    if not child_nodes:
        element = generate_node_element(node=node, attribute=attribute_record)
        return element
    child_args = []
    for child_node in child_nodes:
        child_arg = get_element_from_node_dfs(child_node, node_table, attrubute_table)
        child_args.append(child_arg)
    element = generate_node_element(node=node, attribute=attribute_record, is_leaf=False, child_args=child_args)
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

def generate_public_footer(header_root_node, node_table, attribute_table):
    footer = get_element_from_root(header_root_node, node_table, attribute_table)
    return footer

def generate_page(page_name, **kwargs):
    website_page = get_table_by_name('website_page')
    page = website_page[1]
    node = get_table_by_name('node')
    attribute = get_table_by_name('attribute')
    if page.type == 'static':
        return get_element_from_root(node[page.node_id], node, attribute)
    else:
        fragment_num = kwargs.get('fragment_num', 0)
        return generate_infnite_scroll_list_public(page.db_table_name, fragment_num)

def main_public_template(*args, **kwargs):
    website = get_table_by_name('website')
    record = website[1]
    node = get_table_by_name('node')
    attribute = get_table_by_name('attribute')
    header = Div('header')
    footer = Div('footer')
    if record.header_node_root_id:
        header = generate_public_header(node[record.header_node_root_id],
                                        node, attribute_table=attribute)
    main = generate_public_main()
    if record.footer_node_root_id:
        footer = generate_public_footer(node[record.footer_node_root_id],
                                        node, attribute_table=attribute)
    body = (Title("Ferdaus's Den"), Body(Div(header, main, cls="public"), footer)
            )
    return body
