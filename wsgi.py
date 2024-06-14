from src import app, api
from src.resources import user, adoption, index

api.add_resource(user.Login, '/login', strict_slashes=False)
api.add_resource(user.Register, '/register', strict_slashes=False)
api.add_resource(user.Email, '/email/validation', strict_slashes=False)
api.add_resource(user.Password, '/password/validation', strict_slashes=False)
api.add_resource(user.Username, '/username/validation', strict_slashes=False)
api.add_resource(user.FormValidation, '/from/validation', strict_slashes=False)

api.add_resource(adoption.Questionnaire, '/questionnaire', strict_slashes=False)
api.add_resource(adoption.FormFilter, '/form/filter', strict_slashes=False)
api.add_resource(adoption.PetsCards, '/cards/pets', strict_slashes=False)
api.add_resource(index.MainPage, '/', strict_slashes=False)
api.add_resource(adoption.Info, '/info', strict_slashes=False)


if __name__ == '__main__':
    app.run(debug=True)
