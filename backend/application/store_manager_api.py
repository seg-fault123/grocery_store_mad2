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



class Store_Manager_Category(Resource):
    @jwt_required()
    def get(self, sm_id, cat_id):
        response, status, store_manager=validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        category=Category.query.get(cat_id)
        if category is None:
            response['msg']='Category Not Found!'
            return response, 404
        response=category.make_json()
        response['msg']="Successful"
        return response, 200



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

    @jwt_required()
    def post(self, sm_id):
        response, status, store_manager=validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        data=request.json
        response, status, product=validate_product_add(sm_id, data)
        if product is None:
            return response, status
        db.session.add(product)
        db.session.commit()
        return {'msg': 'Product Created Successfully!'}, 200



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

def validate_product_add(sm_id, data):
    name = data.get('name').title()
    description = data.get('description')
    price = data.get('price')
    unit_measure = data.get('unit_measure')
    stock = data.get('stock')
    category_id = data.get('category_id')
    mfg_date = data.get('mfg_date')
    exp_date = data.get('exp_date')
    data_sm_id = data.get('sm_id')
    if (name is None) or (name == ''):
        return {'msg': 'Name cannot be empty!'}, 406, None
    name_already=Product.query.filter_by(name=name).first()
    if name_already is not None:
        return {'msg': 'Product with same name already exits!'}, 406, None
    if (description is None) or (description == ''):
        return {'msg': 'Description cannot be empty!'}, 406, None
    if (price is None) or (price == ''):
        return {'msg': 'Price cannot be Empty'}, 406, None
    try:
        price=int(price)
    except:
        return {'msg': "Price has to be numeric!"}, 406, None
    if price <= 0:
        return {'msg': 'Price cannot be less than or equal to 0!'}, 406, None
    if (unit_measure is None) or (unit_measure == ''):
        return {'msg': 'Unit Measure cannot be empty!'}, 406, None
    if (stock is None) or (stock == ''):
        return {'msg': "Stock cannot be empty!"}, 406, None
    try:
        stock=int(stock)
    except:
        return {'msg': 'Stock has to be numeric!'}, 406, None
    if stock < 0:
        return {'msg': 'Stock cannot be negative!'}, 406, None
    if (category_id is None) or (category_id == ''):
        return {'msg': 'Category cannot be empty!'}, 406, None
    try:
        category_id=int(category_id)
    except:
        return {'msg': 'Category ID has to be numeric!'}, 406, None
    if Category.query.get(category_id) is None:
        return {'msg': 'Invalid Category ID!'}, 406, None
    if (data_sm_id is None) or (data_sm_id == '') or data_sm_id != sm_id:
        return {'msg': 'Store Manager ID not valid!'}, 406, None
    if (mfg_date is not None) and (mfg_date != ''):
        try:
            mfg_date = to_date(mfg_date)
            exp_date = to_date(exp_date)
        except:
            return {'msg': "Date not in correct format! Format should be 'yyyy-mm-dd'"}, 406, None
    else:
        mfg_date = None
        exp_date = None
    product = Product(name=name, description=description, price=price, unit_measure=unit_measure,
                      stock=stock, category_id=category_id, mfg_date=mfg_date, exp_date=exp_date,
                      sm_id=sm_id)
    return {}, 200, product

def to_date(date_str):
    if date_str=='':
        return None
    date_list=date_str.split('-')
    date_=datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    return date_

api.add_resource(Store_Manager_Api, '/api/store_manager')
api.add_resource(Store_Manager_Category, '/api/store_manager/<int:sm_id>/category/<int:cat_id>')
api.add_resource(Store_Manager_Product, '/api/store_manager/<int:sm_id>/product/<int:p_id>',
                 '/api/store_manager/<int:sm_id>/product')
