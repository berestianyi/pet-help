from src import app, api
from src.routes import Login, Register

api.add_resource(Login, '/login', strict_slashes=False)
api.add_resource(Register, '/register', strict_slashes=False)

if __name__ == '__main__':
    app.run(debug=True)
