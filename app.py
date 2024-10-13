from fasthtml.common import *

css = Style(':root {--pico-font-size:90%,--pico-font-family: Pacifico, cursive;}')
app = FastHTML(hdrs=(picolink, css))

count = 0

@app.get("/")
def home():
    return (Title("Hello world"), Main(
        H1("Hello world"),
        P(f"Count is {count}", id="count"),
        Button("Increment", hx_post="/increment", hx_target="#count", hx_swap="innerHTML", cls="outline"),
        cls="container"))

@app.post("/increment")
def increment():
    global count
    count += 1
    return f"Count is {count}"

serve()