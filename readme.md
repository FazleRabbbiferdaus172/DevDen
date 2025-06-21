The intention of this repository was to explore fasthtml.

1. Another way to add routes:
   ```app.router.add_route(path='/login', endpoint=login, methods=['get'], name='signup', include_in_schema=True)```
2. Catch the reqest objects in request handlers: 'req' should be the first argument of the method
   ```
    def post(req , sess):
   ```
3. Mentioned in the htmx documents [Refer to this](https://htmx.org/attributes/hx-trigger/#non-standard-events)
```
If you are using overflow in css like overflow-y: scroll you should use intersect once instead of revealed
```
