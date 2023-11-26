import datetime
from flask import current_app as app
from flask_restful import Api
from .models import *
from flask_jwt_extended import JWTManager
from flask_caching import Cache

api=Api(app)
jwt=JWTManager(app)
cache=Cache(app)
cache.clear()
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
    elif identity['role_name']=='store_manager':
        user=Store_Manager.query.get(identity['id'])
    return user

def to_date(date_str):
    if date_str=='':
        return None
    date_list=date_str.split('-')
    date_=datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    return date_


@cache.cached(timeout=300, key_prefix='all_categories')
def get_all_categories():
    return Category.query.all()


@cache.memoize(timeout=300)
def get_category_by_id(cat_id):
    category=Category.query.get(cat_id)
    print(f'cached {category.name}')
    return category

@cache.memoize(timeout=100)
def get_customer_cart(c_id):
    customer=Customer.query.get(c_id)
    cart = [(cart_product.product, cart_product.quantity) for cart_product in customer.cart]
    cart = [dict(id=product.id, name=product.name, price=product.price, quantity=quantity) for product, quantity in
            cart]
    return cart

@cache.memoize(timeout=300)
def get_customer_orders(c_id):
    customer=Customer.query.get(c_id)
    orders = [dict(id=order.id, date=order.date.__str__()) for order in customer.orders[::-1]]
    return orders

@cache.memoize(timeout=200)
def get_order_by_id(o_id):
    order = Order.query.get(o_id)
    return order
