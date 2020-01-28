from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask_restplus import Api
from .game.game import api as api_game




def create_app():
    app = Flask(__name__)

    v1_blueprint = Blueprint('v1', __name__, url_prefix='/api')

    api = Api(v1_blueprint,
              doc='/docs',
              title='Desafio BrasilPrev',
              version='1.0',
              description='O objetivo deste desafio é montar um jogo muito parecido com o Banco Imobiliário.' )

    api.add_namespace(api_game)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProdConfig")
    else:
        app.config.from_object("config.DevConfig")


    app.register_blueprint(v1_blueprint)

    CORS(app)
    return app




