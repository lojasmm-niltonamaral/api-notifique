# -*- coding: utf-8 -*-

# Importamos as classes API e Resource
from flask_restful import Api, Resource
from apps.users.resources import Cadastrar,Inativar,Ativar,Alterar
from apps.users.resources_list import Consultas,ConsultaUnitaria
from apps.auth.resources import AuthResource, RefreshTokenResource

class Index(Resource):

    def get(self):
        return {'Olá': 'Nova API Ativa em Flask Python =D'}


# Instânciamos a API do FlaskRestful
api = Api()


def configure_api(app):

    # adicionamos na rota '/' a sua classe correspondente Index
    api.add_resource(Index, '/')
    api.add_resource(Cadastrar, '/usuarios')
    api.add_resource(Inativar, '/usuarios/inativar/<string:user_id>')
    api.add_resource(Ativar, '/usuarios/ativar/<string:user_id>')
    api.add_resource(Alterar, '/usuarios/alterar/<string:user_id>')
    api.add_resource(Consultas, '/usuarios/<int:page_id>')
    api.add_resource(ConsultaUnitaria, '/usuarios/unitario/<string:user_id>')

    api.add_resource(AuthResource, '/auth')
    api.add_resource(RefreshTokenResource, '/auth/refresh')

    # inicializamos a api com as configurações do flask vinda por parâmetro
    api.init_app(app)