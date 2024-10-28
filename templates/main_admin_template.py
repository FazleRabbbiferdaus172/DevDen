from fasthtml.components import *

def main_template(*args, **kwargs):
    nav = Nav(
        Div(Span(kwargs.get('page_title', 'Den'), cls='is-size-3 has-text-centered has-text-justified is-uppercase'), cls="navbar-brand px-2"),
        Div(
            *(A(menu, cls='navbar-item px-1') for menu in kwargs.get('menus', ['Home'])),
            cls='navbar-start'),
        Div(
                Div(
                        Div(
                                A('Login', href='/login'),
                                A('Logout', href='/logout'),
                                A('Signup', href='/signup'),
                            cls='buttons'),
                        cls='navbar-item'
                    ),
                 cls='navbar-end'
            ),
        cls='navbar has-shadow is-fixed-top'
    )
    header = Header(nav)
    main = Main(args, cls='container')
    footer = Footer('Footer', cls='navbar is-fixed-bottom',)
    body = Body(  header,
                Div(main,
                  style='padding-bottom: var(--bulma-navbar-height);'
                ),
                footer,
                cls='has-navbar-fixed-top has-navbar-fixed-bottom')
    web_client = (Title("Den"), 
                    body
                  )
    return web_client