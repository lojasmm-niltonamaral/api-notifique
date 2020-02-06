# -*- coding:utf-8 -*-

# Python

# Flask
from flask import request

# Third
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, jwt_required
from bcrypt import checkpw

# Apps
from apps.users.models import User
from apps.users.schemas import UserSchema
from apps.users.utils import get_user_by_email
from apps.messages import MSG_NO_DATA, MSG_TOKEN_CREATED
from apps.responses import resp_ok, resp_data_invalid, resp_notallowed_user

# Local
from .schemas import LoginSchema


class AuthResource(Resource):
    def post(self, *args, **kwargs):

        req_data = request.get_json() or None
        user = None
        login_schema = LoginSchema()
        schema = UserSchema()

        if req_data is None:
            return resp_data_invalid('Users', [], msg=MSG_NO_DATA)

        data, errors = login_schema.load(req_data)

        if errors:
            return resp_data_invalid('Users', errors)

        user = get_user_by_email(data.get('email'))

        if not isinstance(user, User):
            return user

        if not user.is_active():
            return resp_notallowed_user('Auth')

        if checkpw(data.get('senha').encode('utf-8'), user.senha.encode('utf-8')):

            extras = {
                'token': create_access_token(identity=user.email),
                'refresh': create_refresh_token(identity=user.email)
            }

            result = schema.dump(user)

            return resp_ok(
                'Auth', MSG_TOKEN_CREATED, data=result.data, **extras
            )

        return resp_notallowed_user('Auth')

class RefreshTokenResource(Resource):

    @jwt_refresh_token_required
    def post(self, *args, **kwargs):
        
        extras = {
            'token': create_access_token(identity=get_jwt_identity()),
        }

        return resp_ok(
            'Auth', MSG_TOKEN_CREATED, **extras
        )