from fasthtml.components import *

def generate_how_to_reach_public():
        return [Span("Contact Me -", cls='title is-capitalized is-5'),
                        Span(Span("fazle.ferdaus1416@gmail.com "), Span(I(cls="fas fa-envelope")), Span(" -"), cls='custom-block has-text-weight-semibold'),
                        Span(Span("+880 1968628234 "), Span(I(cls="fas fa-phone")), Span(" -"),cls='custom-block has-text-weight-semibold'),
                        Span(Span("House#34, Road#7, Block#E, Mirpur-12, Dhaka, Bangladesh "), Span(I(cls="fas fa-map-pin")), Span(" -"), cls='custom-block has-text-weight-semibold')]

def generate_about_section_public():
    return [Span("About Me -", cls='title is-capitalized is-5'),
                        Span("From Dhaka, Bangladesh -", cls='custom-block has-text-weight-semibold'),
                        Span("Currently working at Brain Station 23 Plc. -", cls='custom-block has-text-weight-semibold'),
                        Span("Enjoys building things and swimming -", cls='custom-block has-text-weight-semibold')]

def main_public_template(*args, **kwargs):
    icon_list = Div(
        A(I(cls="fab fa-github fa-2x block link"), cls="link", href="https://github.com/FazleRabbbiferdaus172"),
        A(I(cls="fab fa-linkedin-in fa-2x block link"),  cls="link", href="https://www.linkedin.com/in/fazle-rabbi-ferdaus-113255185/"),
        A(I(cls="fab fa-facebook fa-2x block link"), cls="link", href="https://www.facebook.com/FazleRabbiFerdaus/"),
        cls="public-links"
    )
    nav = Nav(
        A(Span('Home', cls='is-size-5 has-text-left'), cls="side-nav selected", hx_get=f'about/page',
          hx_trigger='click',hx_target='#main-content-right',hx_swap='innerHtml'),
        Span(Span('Projects', cls='is-size-5 has-text-left'), cls="side-nav", hx_get=f'project/page?idx={1}',
          hx_trigger='click',hx_target='#main-content-right',hx_swap='innerHtml'),
        A(Span('How to reach me', cls='is-size-5 has-text-left'),  cls="side-nav", hx_get=f'contact/page',
          hx_trigger='click',hx_target='#main-content-right',hx_swap='innerHtml'),
        cls="block pt-5 pl-5 public-nav",
    )
    header = Header(H1('Fazle Rabbi Ferdaus',cls='title is-1'), H2('Software Enginner', cls='subtitle is-4'), nav, cls='block public-header public-section-left')
    about_me_section = generate_about_section_public()
    # projects = generate_infnite_scroll_list_public('project')
    main = Main(
                Div(
                    Div(
                        *about_me_section,
                        # *projects,
                        id="main-content-right"
                    ),
                cls='block content is-normal is-pullued-bottom-right public-section-right')
                )
    footer = Footer(icon_list, cls="public-footer")
    body = (Title("Ferdaus's Den"),Body(Div(header, main, cls="public"), footer)
    )
    return body
