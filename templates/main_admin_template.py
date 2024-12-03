from fasthtml.components import *

# TODO: NAV css needs to be considered as if the browser is reduced then the nav bar eat up some page and does not push down the main div.

def main_template(*args, **kwargs):
    nav = Nav(
        Div(Span(kwargs.get('page_title', 'Den'), cls='is-size-3 has-text-centered has-text-justified is-uppercase'), cls="navbar-brand px-2"),
        Div(
            *(A(menu, href=m_link ,cls='navbar-item px-1') for menu,m_link in kwargs.get('menus', [('Home', '/admin')])),
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
    return Main(args, cls='container')
    # return Div("hi")