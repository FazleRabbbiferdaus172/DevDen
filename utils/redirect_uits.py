from fasthtml.starlette import RedirectResponse

login_redir = RedirectResponse('/login', status_code=303)
