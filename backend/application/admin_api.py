from flask import request
from flask_restful import Resource
from .models import *
from passlib.hash import pbkdf2_sha256 as hash_password
from .api import *
from flask_jwt_extended import current_user, jwt_required, get_jwt, decode_token

class Admin_Category(Resource):
    @jwt_required()
    def get(self, a_id, cat_id):
        response, status, admin=validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        category=Category.query.get(cat_id)
        if category is None:
            response['msg']="Category Not Found!"
            return response, 404
        response=category.make_json()
        response['msg']='Successful'
        return response, 200

    @jwt_required()
    def post(self, a_id):
        response, status, admin=validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        data=request.json
        name=data.get('name')
        description=data.get('description')
        if (name is None) or (name==''):
            return {'msg': 'Name cannot be empty!'}, 406
        if (description is None) or (description==''):
            return {'msg': 'Description cannot be empty!'}, 406
        name_already=Category.query.filter_by(name=name).first()
        if name_already is not None:
            return {'msg': 'Category with same name already exists!'}, 406
        category=Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        return {'msg': 'Category added successfully!'}, 200

class Admin_Login(Resource):
    def post(self):
        user_name = request.json.get('user_name')
        password = request.json.get('password')
        if (user_name is None) or (user_name == ''):
            return {'msg': 'UserName cannot be empty!'}, 406
        if (password is None) or (password == ''):
            return {'msg': 'Password cannot be empty!'}, 406
        admin=Admin.query.filter_by(user_name=user_name).first()
        if admin and hash_password.verify(password, admin.password):
            response=admin.make_json()
            response['msg']='Successful'
            return response, 200
        else:
            return {'msg': 'Invalid Admin Credentials!'}, 401


def validate_admin(requested_id, requester_jwt):
    identity=requester_jwt['sub']
    if identity['role_name']!='admin':
        return {'msg': 'Unauthorized Access'}, 401, None
    elif identity['id']!=requested_id:
        return {'msg': 'Unauthorized Access'}, 401, None
    admin=Admin.query.get(requested_id)
    if admin is None:
        return {'msg': 'User Not Found'}, 404, None
    admin_token_data=decode_token(admin.access_token)
    if admin_token_data['jti']!=requester_jwt['jti']:
        return {'msg': 'Unauthorized Access'}, 401, None
    return {}, 200, admin

api.add_resource(Admin_Login, '/api/admin_login')
api.add_resource(Admin_Category, '/api/admin/<int:a_id>/category/<int:cat_id>',
                 '/api/admin/<int:a_id>/category')
