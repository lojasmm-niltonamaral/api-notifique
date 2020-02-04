# -*- coding: utf-8 -*-

# Importamos as classes API e Resource
from flask_restful import Api, Resource
from apps.users.resources import Cadastrar
from apps.users.resources_list import UserPageList,AdminUserResource
from apps.auth.resources import AuthResource, RefreshTokenResource

# Criamos uma classe que extende de Resource
class Index(Resource):

    # Definimos a operação get do protocolo http
    def get(self):

        # retornamos um simples dicionário que será automáticamente
        # retornado em json pelo flask
        return {'Olá': 'Nova API Ativa em Flask Python =D'}


# Instânciamos a API do FlaskRestful
api = Api()


def configure_api(app):

    # adicionamos na rota '/' a sua classe correspondente Index
    api.add_resource(Index, '/')
    api.add_resource(Cadastrar, '/users')
    api.add_resource(UserPageList, '/users/<int:page_id>')
    api.add_resource(AdminUserResource, '/users/single/<string:user_id>')

    api.add_resource(AuthResource, '/auth')
    api.add_resource(RefreshTokenResource, '/auth/refresh')

    # inicializamos a api com as configurações do flask vinda por parâmetro
    api.init_app(app)