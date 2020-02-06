# -*- coding:utf-8 -*-

# Python

# Flask
from flask import request

# Third
from flask_restful import Resource
from bcrypt import gensalt, hashpw
from mongoengine.errors import NotUniqueError, ValidationError

# Apps
from apps.responses import (
    resp_already_exists,
    resp_exception,
    resp_data_invalid,
    resp_ok
)
from apps.messages import MSG_NO_DATA, MSG_PASSWORD_DIDNT_MATCH, MSG_INVALID_DATA
from apps.messages import MSG_RESOURCE_CREATED,MSG_RESOURCE_INATIVO,MSG_RESOURCE_ATIVO,MSG_RESOURCE_UPDATED

from flask_jwt_extended import get_jwt_identity, jwt_required

# Local
from .models import User
from .schemas import UserSchema,UserUpdateSchema
from .utils import check_password_in_signup,get_user_by_id, exists_email_in_users


class Cadastrar(Resource):
    def post(self, *args, **kwargs):
        
        req_data = request.get_json() or None
        data, errors, result = None, None, None
        senha, confirma_senha = None, None
        schema = UserSchema()

        if req_data is None:
            return resp_data_invalid('Users', [], msg=MSG_NO_DATA)

        senha = req_data.get('senha', None)
        confirma_senha = req_data.pop('confirma_senha', None)

        if not check_password_in_signup(senha, confirma_senha):
            errors = {'senha': MSG_PASSWORD_DIDNT_MATCH}
            return resp_data_invalid('Users', errors)

        data, errors = schema.load(req_data)

        if errors:
            return resp_data_invalid('Users', errors)

        hashed = hashpw(senha.encode('utf-8'), gensalt(12))

        try:
            data['senha'] = hashed
            data['email'] = data['email'].lower()
            model = User(**data)
            model.save()

        except NotUniqueError:
            return resp_already_exists('Users', 'usuario')

        except ValidationError as e:
            return resp_exception('Users', description=str(e),msg=MSG_INVALID_DATA)

        except Exception as e:
            return resp_exception('Users', description=str(e), msg=MSG_INVALID_DATA)

        schema = UserSchema()
        result = schema.dump(model)

        return resp_ok(
            'Users', MSG_RESOURCE_CREATED.format('Usuário'),  data=result.data,
        )


class Inativar(Resource):
    @jwt_required
    def get(self, user_id):
        
        user = get_user_by_id(user_id)

        if not isinstance(user, User):
            return user

        try:
            user.ativo = False
            user.save()

        except NotUniqueError:
            return resp_already_exists('Users', 'usuário')

        except ValidationError as e:
            return resp_exception('Users', msg=MSG_INVALID_DATA, description=e.__str__())

        except Exception as e:
            return resp_exception('Users', description=e.__str__())

        return resp_ok('Users', MSG_RESOURCE_INATIVO.format('Usuário'))

class Ativar(Resource):
    @jwt_required
    def get(self, user_id):
        
        user = get_user_by_id(user_id)

        if not isinstance(user, User):
            return user

        try:
            user.ativo = True
            user.save()

        except NotUniqueError:
            return resp_already_exists('Users', 'usuário')

        except ValidationError as e:
            return resp_exception('Users', msg=MSG_INVALID_DATA, description=e.__str__())

        except Exception as e:
            return resp_exception('Users', description=e.__str__())

        return resp_ok('Users', MSG_RESOURCE_ATIVO.format('Usuário'))

class Alterar(Resource):
    @jwt_required
    def put(self, user_id):
        result = None
        schema = UserSchema()
        update_schema = UserUpdateSchema()
        req_data = request.get_json() or None
        email = None

        
        if req_data is None:
            return resp_data_invalid('Users', [], msg=MSG_NO_DATA)

        
        user = get_user_by_id(user_id)

        
        if not isinstance(user, User):
            return user

        data, errors = update_schema.load(req_data)

        if errors:
            return resp_data_invalid('Users', errors)

        email = data.get('email', None)

        if email and exists_email_in_users(email, user):
            return resp_data_invalid(
                'Users', [{'email': [MSG_ALREADY_EXISTS.format('usuário')]}]
            )

        try:
            for i in data.keys():
                user[i] = data[i]

            user.save()

        except NotUniqueError:
            return resp_already_exists('Users', 'usuário')

        except ValidationError as e:
            return resp_exception('Users', msg=MSG_INVALID_DATA, description=e.__str__())

        except Exception as e:
            return resp_exception('Users', description=e.__str__())

        result = schema.dump(user)

        return resp_ok(
            'Users', MSG_RESOURCE_UPDATED.format('Usuário'),  data=result.data
        )
