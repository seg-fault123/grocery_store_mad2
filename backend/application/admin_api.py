from flask import request
from flask_restful import Resource
from .models import *
from passlib.hash import pbkdf2_sha256 as hash_password
from .api import *
from flask_jwt_extended import create_access_token, current_user, jwt_required, get_jwt, decode_token

class Admin_Login(Resource):
    def post(self):
        user_name=request.json.get('user_name')
        password=request.json.get('password')
        admin=Admin.query.filter(Admin.user_name==user_name).first()
        if admin and hash_password.verify(password, admin.password):
            response = {'msg': "Successful", 'id': admin.id,
                        'access_token': admin.access_token}
            return response, 200
        else:
            return {'msg': 'Invalid Admin Credentials'}, 401

api.add_resource(Admin_Login, '/api/admin_login')
