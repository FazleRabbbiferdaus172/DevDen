1. Another way to add routes:
   ```app.router.add_route(path='/login', endpoint=login, methods=['get'], name='signup', include_in_schema=True)```
2. Catch the reqest objects in request handlers: 'req' should be the first argument of the method
   ```
    def post(req , sess):
   ```