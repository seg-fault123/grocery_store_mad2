import datetime
from flask import request
from flask_restful import Resource
from .models import *
from passlib.hash import pbkdf2_sha256 as hash_password
from .api import *
from flask_jwt_extended import create_access_token, current_user, jwt_required, get_jwt, decode_token



class Buy_Now(Resource):
    @jwt_required()
    def post(self, c_id, p_id):
        response, status, customer=validate_customer(c_id, get_jwt())
        if customer is None:
            return response, status
        product=Product.query.get(p_id)
        if product is None:
            response['msg']='Product Not Found!'
            return response, 404
        quantity=request.json.get('quantity')
        max_available=min(product.stock, 10)
        try:
            quantity=int(quantity)
        except:
            response['msg']='Quantity should be Integer!'
            return response, 406
        if quantity<1:
            response['msg']='Quantity has to be at least 1!'
            return response, 406
        if quantity > max_available:
            response['msg']=f'Quantity cannot be more than {max_available}!'
            return response, 406
        product.stock-=quantity
        db.session.add(Order(customer_id=c_id, date=datetime.date.today()))
        db.session.commit()
        order=Order.query.all()[-1]
        db.session.add(Order_Product(order_id=order.id, product_id=product.id, quantity=quantity))
        db.session.commit()
        response['msg']='Successfully Placed'
        response['order_id']=order.id
        return response, 200




class Customer_Api(Resource):
    @jwt_required()
    def get(self, id):
        response, status, customer=validate_customer(id, get_jwt())
        if customer is None:
            return response, status
        response=customer.make_json()
        response['msg']="Successful"
        return response, 200

    def post(self):
        data=request.json
        email=data.get('email_id')
        first_name=data.get('first_name')
        last_name=data.get('last_name')
        if last_name is None:
            last_name=''
        user_name=data.get('user_name')
        password=data.get('password')
        if (email is None) or (email==''):
            return {'msg': 'Email-ID cannot be empty!'}, 406
        if (first_name is None) or (first_name==''):
            return {'msg': "First Name cannot be empty!"}, 406
        if (user_name is None) or (user_name==''):
            return {'msg': "UserName cannot be empty!"}, 406
        if (password is None) or (password==''):
            return {'msg': "Password cannot be empty!"}, 406
        email_already=Customer.query.filter_by(email_id=email).first()
        if email_already is not None:
            return {'msg': 'Email-ID is already registered!'}, 406
        user_name_already=Customer.query.filter_by(user_name=user_name).first()
        if user_name_already is not None:
            return {'msg': "UserName is already taken! Try a different username."}, 406
        role=Role.query.filter_by(name='customer').first()
        customer=Customer(first_name=first_name, last_name=last_name, email_id=email,
                          user_name=user_name, password=hash_password.hash(password), last_active=datetime.date.today(),
                          role_id=role.id)
        db.session.add(customer)
        db.session.commit()
        customer=Customer.query.filter_by(user_name=user_name).first()
        customer.access_token=create_access_token(identity=customer)
        db.session.commit()
        return {'msg': 'Account Created Successfully! You can now Login.'}, 200



class Customer_Category(Resource):
    @jwt_required()
    def get(self, c_id, cat_id):
        response, status, customer=validate_customer(c_id, get_jwt())
        if customer is None:
            return response, status
        category=Category.query.get(cat_id)
        if category is None:
            response['msg']='Category Not Found!'
            return response, 404
        response=category.make_json()
        response['msg']="Successful"
        return response, 200


class Customer_Home(Resource):
    @jwt_required()
    def get(self, c_id):
        response, status, customer=validate_customer(c_id, get_jwt())
        if customer is None:
            return response, status
        categories=Category.query.all()
        response['msg']="Successful"
        response['categories']=[category.id for category in categories]
        return response, 200

class Customer_Login(Resource):
    def post(self):
        user_name=request.json.get('user_name')
        password=request.json.get('password')
        if (user_name is None) or (user_name==''):
            return {'msg': 'UserName cannot be empty!'}, 406
        if (password is None) or (password==''):
            return {'msg': 'Password cannot be empty!'}, 406
        customer=Customer.query.filter(Customer.user_name==user_name).first()
        if customer and hash_password.verify(password, customer.password):
            customer.last_active=datetime.date.today()
            db.session.commit()
            response=customer.make_json()
            response['msg']='Successful'
            return response, 200
        else:
            return {'msg': 'Invalid Customer Credentials!'}, 401


class Customer_Product(Resource):
    @jwt_required()
    def get(self, c_id, p_id):
        response, status, customer=validate_customer(c_id, get_jwt())
        if customer is None:
            return response, status
        product=Product.query.get(p_id)
        if product is None:
            response['msg']='Product Not Found!'
            return response, 404
        response=product.make_json()
        response['msg']='Successful'
        return response, 200


def validate_customer(requested_id, requester_jwt):
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




api.add_resource(Buy_Now, '/api/customer/<int:c_id>/buy_now/<int:p_id>')
api.add_resource(Customer_Api, '/api/customer/<int:id>', '/api/customer')
api.add_resource(Customer_Category, '/api/customer/<int:c_id>/category/<int:cat_id>')
api.add_resource(Customer_Home, '/api/customer/<int:c_id>/home')
api.add_resource(Customer_Login, '/api/customer_login')
api.add_resource(Customer_Product, '/api/customer/<int:c_id>/product/<int:p_id>')
