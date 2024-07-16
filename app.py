from src import app, api
from src.resources import user, adoption, index

api.add_resource(user.Login, '/login', strict_slashes=False)
api.add_resource(user.Register, '/register', strict_slashes=False)
api.add_resource(user.EmailHTMX, '/email/validation', strict_slashes=False)
api.add_resource(user.PasswordHTMX, '/password/validation', strict_slashes=False)
api.add_resource(user.UsernameHTMX, '/username/validation', strict_slashes=False)
api.add_resource(user.FormValidationHTMX, '/from/validation', strict_slashes=False)
api.add_resource(user.Profile, '/profile', strict_slashes=False)

api.add_resource(adoption.Questionnaire, '/questionnaire', strict_slashes=False)
api.add_resource(adoption.QuestionnaireHTMX, '/questionnaire/htmx', strict_slashes=False)

api.add_resource(adoption.GiveShelter, '/give/shelter', strict_slashes=False)
api.add_resource(adoption.GiveShelterHTMX, '/give/shelter/htmx', strict_slashes=False)
api.add_resource(adoption.GiveShelterButtonSubmitHTMX, '/give/shelter/submit', strict_slashes=False)

api.add_resource(adoption.Adopt, '/adopt/<int:pet_id>', strict_slashes=False)


api.add_resource(index.MainPage, '/', strict_slashes=False)
api.add_resource(index.AboutUs, '/about', strict_slashes=False)
api.add_resource(index.OurTeam, '/team', strict_slashes=False)
api.add_resource(index.HowToHelp, '/help', strict_slashes=False)


if __name__ == '__main__':
    app.run(debug=True)
