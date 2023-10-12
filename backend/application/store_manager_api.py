import datetime
from flask import request
from flask_restful import Resource
from .models import *
from passlib.hash import pbkdf2_sha256 as hash_password
from .api import *
from flask_jwt_extended import create_access_token, current_user, jwt_required, get_jwt, decode_token

class Store_Manager_Api(Resource):
    def post(self):
        data = request.json
        email = data.get('email_id')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if last_name is None:
            last_name = ''
        user_name = data.get('user_name')
        password = data.get('password')
        if (email is None) or (email == ''):
            return {'msg': 'Email-ID cannot be empty!'}, 406
        if (first_name is None) or (first_name == ''):
            return {'msg': "First Name cannot be empty!"}, 406
        if (user_name is None) or (user_name == ''):
            return {'msg': "UserName cannot be empty!"}, 406
        if (password is None) or (password == ''):
            return {'msg': "Password cannot be empty!"}, 406
        email_already = Store_Manager.query.filter_by(email_id=email).first()
        if email_already is not None:
            return {'msg': 'Email-ID is already registered!'}, 406
        user_name_already=Store_Manager.query.filter_by(user_name=user_name).first()
        if user_name_already is not None:
            return {'msg': "UserName is already taken! Try a different username."}, 406
        role = Role.query.filter_by(name='store_manager').first()
        store_manager = Store_Manager(first_name=first_name, last_name=last_name, email_id=email,
                                      user_name=user_name, password=hash_password.hash(password),
                                      role_id=role.id)
        db.session.add(store_manager)
        db.session.commit()
        store_manager=Store_Manager.query.filter_by(user_name=user_name).first()
        store_manager.access_token=create_access_token(identity=store_manager)
        db.session.commit()
        return {'msg': 'Account Created Successfully! You can now Login.'}, 200

class Store_Manager_Product(Resource):
    @jwt_required()
    def get(self, sm_id, p_id):
        response, status, store_manager=validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        product=Product.query.get(p_id)
        if product is None:
            response['msg'] = 'Product Not Found!'
            return response, 404
        response = product.make_json()
        response['msg'] = 'Successful'
        return response, 200

def validate_store_manager(requested_id, requester_jwt):
    identity = requester_jwt['sub']
    if identity['role_name'] != 'store_manager':
        return {'msg': 'Unauthorized Access'}, 401, None
    elif identity['id'] != requested_id:
        return {'msg': 'Unauthorized Access'}, 401, None
    store_manager = Store_Manager.query.get(requested_id)
    if (store_manager is None) or (store_manager.approved==0):
        return {'msg': 'User Not Found'}, 404, None
    sm_token_data = decode_token(store_manager.access_token)
    if sm_token_data['jti']!=requester_jwt['jti']:
        return {'msg': 'Unauthorized Access'}, 401, None
    return {}, 200, store_manager

api.add_resource(Store_Manager_Api, '/api/store_manager')
api.add_resource(Store_Manager_Product, '/api/store_manager/<int:sm_id>/product/<int:p_id>')
