from flask import request, send_file
from flask_restful import Resource
from celery.result import AsyncResult
from passlib.hash import pbkdf2_sha256 as hash_password
from .api import *
from .tasks import create_store_manager_report
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
        return {'msg': 'Request Made Successfully! You can Login after the Admin approves.'}, 200



class Store_Manager_Category(Resource):
    @jwt_required()
    def get(self, sm_id, cat_id):
        response, status, store_manager=validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        category=get_category_by_id(cat_id)
        if category is None:
            response['msg']='Category Not Found!'
            return response, 404
        response=category.make_json()
        response['msg']="Successful"
        return response, 200

    @jwt_required()
    def post(self, sm_id):
        response, status, store_manager=validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        data=request.json
        response, status, new_category=validate_category_add(sm_id, data)
        if new_category is None:
            return response, status
        db.session.add(new_category)
        db.session.commit()
        return {'msg': 'Request Made Successfully!'}, 200

    @jwt_required()
    def put(self, sm_id, cat_id):
        response, status, store_manager = validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        data=request.json
        response, status, edit_category=validate_category_edit(sm_id, cat_id, data)
        if edit_category is None:
            return response, status
        db.session.add(edit_category)
        db.session.commit()
        return {'msg': 'Request Made Successfully!'}, 200

    @jwt_required()
    def delete(self, sm_id, cat_id):
        response, status, store_manager = validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        data = request.json
        response, status, delete_category=validate_category_delete(sm_id, cat_id, data)
        if delete_category is None:
            return response, status
        db.session.add(delete_category)
        db.session.commit()
        return {'msg': 'Request Made Successfully!'}, 200



class Store_Manager_Categories(Resource):
    #this can be used to get categories for both home page and categories page
    @jwt_required()
    def get(self, sm_id):
        response, status, store_manager=validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        categories=get_all_categories()
        categories=[dict(id=category.id, name=category.name) for category in categories]
        response['msg']='Successful'
        response['categories']=categories
        return response, 200



class Store_Manager_Login(Resource):
    def post(self):
        user_name = request.json.get('user_name')
        password = request.json.get('password')
        if (user_name is None) or (user_name == ''):
            return {'msg': 'UserName cannot be empty!'}, 406
        if (password is None) or (password == ''):
            return {'msg': 'Password cannot be empty!'}, 406
        store_manager=Store_Manager.query.filter_by(user_name=user_name).first()
        if store_manager and store_manager.approved and hash_password.verify(password, store_manager.password):
            response=store_manager.make_json()
            response['msg']="Successful"
            return response, 200
        else:
            return {"msg": "Invalid Store Manager Credentials!"}, 401




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
        if 'product/' in request.url:
            if product.sm_id!=sm_id:
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
        cache.delete_memoized(get_category_by_id, product.category_id)
        return {'msg': 'Product Created Successfully!'}, 200

    @jwt_required()
    def put(self, sm_id, p_id):
        response, status, store_manager = validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        data = request.json
        response, status, product = validate_product_edit(sm_id, p_id, data)
        if product is None:
            return response, status
        db.session.commit()
        return {'msg': "Product Updated Successfully!"}, 200

    @jwt_required()
    def delete(self, sm_id, p_id):
        response, status, store_manager = validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        product=Product.query.get(p_id)
        if (product is None) or (product.sm_id!=sm_id):
            return {'msg': 'Product does not exist!'}, 404
        db.session.delete(product)
        cache.delete_memoized(get_category_by_id, product.category_id)
        db.session.commit()
        return {'msg': 'Product deleted Successfully!'}, 200





class Store_Manager_Products(Resource):
    # to be used for product page
    # home page products will be included in the categories
    @jwt_required()
    def get(self, sm_id):
        response, status, store_manager=validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        products=Product.query.filter_by(sm_id=sm_id).all()
        products=[dict(id=product.id, name=product.name) for product in products]
        response['msg']='Successful'
        response['products']=products
        return response, 200


class Store_Manager_Create_Report(Resource):
    @jwt_required()
    def get(self, sm_id):
        response, status, store_manager = validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        if len(store_manager.products)==0:
            return {'msg': 'Store Manager does not have any Products! Report cannot be generated!'}, 406
        task=create_store_manager_report.delay(sm_id)
        response['msg']='Successful'
        response['task_id']=task.id
        return response, 200


class Store_Manager_Download_Report(Resource):
    @jwt_required()
    def get(self, sm_id, task_id):
        response, status, store_manager = validate_store_manager(sm_id, get_jwt())
        if store_manager is None:
            return response, status
        task=AsyncResult(task_id)
        if task.ready():
            filename=task.result
            send=send_file(filename, mimetype='text/csv', as_attachment=True)
            send.headers['Content-Disposition'] = f'attachment; filename={filename}'
            return send
        else:
            return {'msg': 'Task Pending'}, 404

@cache.memoize(timeout=300)
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
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    unit_measure = data.get('unit_measure')
    stock = data.get('stock')
    category_name = data.get('category_name')
    mfg_date = data.get('mfg_date')
    exp_date = data.get('exp_date')
    if (name is None) or (name == ''):
        return {'msg': 'Name cannot be empty!'}, 406, None
    name=name.title()
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
    if (category_name is None) or (category_name == ''):
        return {'msg': 'Category cannot be empty!'}, 406, None
    category=Category.query.filter_by(name=category_name).first()
    if category is None:
        return {'msg': 'Invalid Category Name!'}, 406, None
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
                      stock=stock, category_id=category.id, mfg_date=mfg_date, exp_date=exp_date,
                      sm_id=sm_id)
    return {}, 200, product

def validate_product_edit(sm_id, p_id, data):
    product=Product.query.get(p_id)
    if (product is None) or (product.sm_id!=sm_id):
        return {'msg': 'Product does not exist!'}, 404, None
    name=data.get('name')
    description = data.get('description')
    price = data.get('price')
    unit_measure = data.get('unit_measure')
    stock = data.get('stock')
    category_name = data.get('category_name')
    mfg_date = data.get('mfg_date')
    exp_date = data.get('exp_date')
    if (name is None) or (name == ''):
        return {'msg': 'Name cannot be empty!'}, 406, None
    name = name.title()
    name_already = Product.query.filter(Product.name == name, Product.id != p_id).first()
    if name_already is not None:
        return {'msg': 'Product with the same new name already exits!'}, 406, None
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
    if (category_name is None) or (category_name == ''):
        return {'msg': 'Category cannot be empty!'}, 406, None
    category=Category.query.filter_by(name=category_name).first()
    if category is None:
        return {'msg': 'Invalid Category Name!'}, 406, None
    if (mfg_date is not None) and (mfg_date != ''):
        try:
            mfg_date = to_date(mfg_date)
            exp_date = to_date(exp_date)
        except:
            return {'msg': "Date not in correct format! Format should be 'yyyy-mm-dd'"}, 406, None
    else:
        mfg_date = None
        exp_date = None
    product.name=name
    product.description=description
    product.price=price
    product.unit_measure=unit_measure
    product.stock=stock
    product.mfg_date=mfg_date
    product.exp_date=exp_date
    product.category_id=category.id
    return {}, 200, product


def validate_category_add(sm_id, data):
    name = data.get('name')
    description = data.get('description')
    reason= data.get('reason')
    if (name is None) or (name==''):
        return {'msg': 'Name cannot be empty!'}, 406, None
    name=name.title()
    name_already=Category.query.filter_by(name=name).first()
    if name_already is not None:
        return {'msg': 'Category with same name already exits!'}, 406, None
    if (description is None) or (description==''):
        return {'msg': 'Description cannot be empty!'}, 406, None
    if (reason is None) or (reason==''):
        return {'msg': 'Reason cannot be empty!'}, 406, None
    new_category=New_Category_Request(name=name, description=description, reason=reason, sm_id=sm_id)
    return {}, 200, new_category

def validate_category_edit(sm_id, cat_id, data):
    if get_category_by_id(cat_id) is None:
        return {'msg': 'Category does not exist!'}, 404, None
    name = data.get('name')
    description = data.get('description')
    reason = data.get('reason')
    if (name is None) or (name==''):
        return {'msg': 'Name cannot be empty!'}, 406, None
    name=name.title()
    name_already=Category.query.filter(Category.name==name, Category.id!=cat_id).first()
    if name_already is not None:
        return {'msg': 'Category with the same new name already exits!'}, 406, None
    if (description is None) or (description==''):
        return {'msg': 'Description cannot be empty!'}, 406, None
    if (reason is None) or (reason==''):
        return {'msg': 'Reason cannot be empty!'}, 406, None
    edit_category=Edit_Category_Request(name=name, description=description, reason=reason, sm_id=sm_id, category_id=cat_id)
    return {}, 200, edit_category

def validate_category_delete(sm_id, cat_id, data):
    if get_category_by_id(cat_id) is None:
        return {'msg': 'Category does not exist!'}, 404, None
    reason = data.get('reason')
    if (reason is None) or (reason==''):
        return {'msg': 'Reason cannot be empty!'}, 406, None
    delete_category=Delete_Category_Request(reason=reason, sm_id=sm_id, category_id=cat_id)
    return {}, 200, delete_category


api.add_resource(Store_Manager_Api, '/api/store_manager')
api.add_resource(Store_Manager_Category, '/api/store_manager/<int:sm_id>/category',
                 '/api/store_manager/<int:sm_id>/category/<int:cat_id>')
api.add_resource(Store_Manager_Categories, '/api/store_manager/<int:sm_id>/categories')
api.add_resource(Store_Manager_Login, '/api/store_manager_login')
api.add_resource(Store_Manager_Product, '/api/store_manager/<int:sm_id>/product/<int:p_id>',
                 '/api/store_manager/<int:sm_id>/product', '/api/store_manager/<int:sm_id>/product_home/<int:p_id>')
api.add_resource(Store_Manager_Products, '/api/store_manager/<int:sm_id>/products')
api.add_resource(Store_Manager_Create_Report, '/api/store_manager/<int:sm_id>/create_report')
api.add_resource(Store_Manager_Download_Report, '/api/store_manager/<int:sm_id>/download_report/<task_id>')
