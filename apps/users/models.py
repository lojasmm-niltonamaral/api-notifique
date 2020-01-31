# Python
from datetime import datetime

# Third
from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    StringField,
    URLField
)

# Apps
from apps.db import db


class UserMixin(db.Document):
    """
    Default implementation for User fields
    """
    meta = {
        'abstract': True,
        'ordering': ['email']
    }

    email = EmailField(required=True, unique=True)
    telefone = StringField(required=True,unique=True)
    dataNascimento = StringField(required=True)
    sexo = StringField(required=True)
    senha = StringField(required=True)
    criadoem = DateTimeField(default=datetime.now)
    ativo = BooleanField(default=True)

    def is_active(self):
        return self.active

class Enderecos(EmbeddedDocument):
    """
    Endereço de cadastro
    """
    meta = {
        'ordering': ['endereco']
    }
    
    endereco = StringField(default='')
    cidade = StringField(default='')
    estado = StringField(default='')

class User(UserMixin):
    '''
    Users
    '''
    meta = {'collection': 'users'}

    nome = StringField(required=True)
    cpf = StringField(default='')
    endereco = EmbeddedDocumentField(Enderecos, default=Enderecos)
