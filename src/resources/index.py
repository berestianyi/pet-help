from flask import make_response, render_template
from flask_restful import Resource


class MainPage(Resource):
    def get(self):
        return make_response(render_template('index.html'))


class AboutUs(Resource):
    def get(self):
        return make_response(render_template('information/about_us.html'))


class OurTeam(Resource):
    def get(self):
        return make_response(render_template('information/our_team.html'))


class HowToHelp(Resource):
    def get(self):
        return make_response(render_template('information/how_to_help.html'))
