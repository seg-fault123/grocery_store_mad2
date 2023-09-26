from flask import request
from flask_restful import Resource
from .models import *
from passlib.hash import pbkdf2_sha256 as hash_password
from .api import *
from flask_jwt_extended import create_access_token, current_user, jwt_required, get_jwt, decode_token


class CustomerApi(Resource):
    @jwt_required()
    def get(self, id):
        response, status, customer=validate_requester(id, get_jwt())
        if customer is None:
            return response, status
        else:
            response['msg']='User Found'
            response['id']=customer.id
            response['first_name']=customer.first_name
            response['role_id']=customer.role.id
            response['role_name']=customer.role.name
            return response


class Signup(Resource):
    def post(self):
        pass

class Login(Resource):
    def post(self):
        user_name=request.json.get('user_name')
        password=request.json.get('password')
        customer=Customer.query.filter(Customer.user_name==user_name).first()
        if customer and hash_password.verify(password, customer.password):
            response={'msg': "Successful", 'id': customer.id,
                      'access_token': customer.access_token}
            return response, 200
        else:
            return {'msg': 'Invalid Customer Credentials'}, 401


def validate_requester(requested_id, requester_jwt):
    identity=requester_jwt['sub']
    if identity['role_name']!='customer':
        return {'msg': 'Unauthorized Access'}, 401, None
    elif identity['id']!=requested_id:
        return {'msg': 'Unauthorized Access'}, 401, None
    customer = Customer.query.get(requested_id)
    if customer is None:
        return {'msg': 'User Not Found'}, 404, None
    customer_token_data=decode_token(customer.access_token)
    if customer_token_data['jti']!=requester_jwt['jti']:
        return {'msg': 'Unauthorized Access'}, 401, None
    return {}, 200, customer




api.add_resource(CustomerApi, '/api/customer/<int:id>')
api.add_resource(Login, '/api/customer_login')
