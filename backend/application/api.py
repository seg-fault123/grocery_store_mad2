from flask import current_app as app
from flask_restful import Api
from .models import *
from flask_jwt_extended import JWTManager

api=Api(app)
jwt=JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    response={'id': user.id, 'role_name': user.role.name}
    return response

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity=jwt_data['sub']
    user=None
    if identity['role_name']=='customer':
        user=Customer.query.get(identity['id'])
    elif identity['role_name']=='admin':
        user=Admin.query.get(identity['id'])
    return user
