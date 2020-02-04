# -*- coding: utf-8 -*-

from marshmallow import Schema
from marshmallow.fields import Email, Str, Boolean,Nested
from apps.messages import MSG_FIELD_REQUIRED

class UserSchema(Schema):
    
    nome = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    email = Email(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    cpf = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    dataNascimento = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    sexo = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    telefone = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    endereco = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    cidade = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    estado = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    senha = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    ativo = Boolean()

class UserUpdateSchema(Schema):
    full_name = Str()
    email = Email()
    cpf_cnpj = Str()
    endereco = Str()
    cidade = Str()
    estado = Str()