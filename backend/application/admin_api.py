from flask import request
from flask_restful import Resource
from passlib.hash import pbkdf2_sha256 as hash_password
from .api import *
from flask_jwt_extended import current_user, jwt_required, get_jwt, decode_token

class Admin_Category(Resource):
    @jwt_required()
    def get(self, a_id, cat_id):
        response, status, admin=validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        category=get_category_by_id(cat_id)
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
        name=name.title()
        name_already=Category.query.filter_by(name=name).first()
        if name_already is not None:
            return {'msg': 'Category with same name already exists!'}, 406
        category=Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        cache.delete('all_categories')
        return {'msg': 'Category added successfully!'}, 200

    @jwt_required()
    def put(self, a_id, cat_id):
        response, status, admin=validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        category=Category.query.get(cat_id)
        if category is None:
            return {'msg': 'Category does not exist!'}, 404
        data=request.json
        name=data.get('name')
        description=data.get('description')
        if (name is None) or (name==''):
            return {'msg': 'Name cannot be empty!'}, 406
        if (description is None) or (description==''):
            return {'msg': 'Description cannot be empty!'}, 406
        name=name.title()
        name_already=Category.query.filter(Category.name == name, Category.id != cat_id).first()
        if name_already is not None:
            return {'msg': 'Category with the same new name already exits!'}, 406, None
        category.name=name
        category.description=description
        db.session.commit()
        cache.delete('all_categories')
        cache.delete_memoized(get_category_by_id, cat_id)
        return {'msg': 'Category Updated Successfully!'}, 200

    @jwt_required()
    def delete(self, a_id, cat_id):
        response, status, admin=validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        category = Category.query.get(cat_id)
        if category is None:
            return {'msg': 'Category does not exist!'}, 404
        db.session.delete(category)
        db.session.commit()
        cache.delete('all_categories')
        cache.delete_memoized(get_category_by_id, cat_id)
        return {'msg': 'Category Deleted Successfully!'}, 200



class Admin_Categories(Resource):
    @jwt_required()
    def get(self, a_id):
        response, status, admin = validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        categories = get_all_categories()
        categories = [dict(id=category.id, name=category.name) for category in categories]
        response['msg'] = 'Successful'
        response['categories'] = categories
        return response, 200


class Admin_Delete_Category_Request(Resource):
    @jwt_required()
    def get(self, a_id):
        response, status, admin = validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        requests=Delete_Category_Request.query.all()[::-1]
        requests=[dict(id=del_request.id, category_id=del_request.category.id, category_name=del_request.category.name,
                       reason=del_request.reason, sm_id=del_request.store_manager.id,
                       sm_name=del_request.store_manager.first_name) for del_request in requests]
        response['requests']=requests
        response['msg']='Successful'
        return response, 200

    @jwt_required()
    def delete(self, a_id, r_id):
        response, status, admin = validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        del_request=Delete_Category_Request.query.get(r_id)
        if del_request is None:
            return {'msg': "Request does not exist!"}, 404
        db.session.delete(del_request)
        db.session.commit()
        return {'msg': "Request Deleted Successfully!"}, 200



class Admin_Edit_Category_Request(Resource):
    @jwt_required()
    def get(self, a_id):
        response, status, admin = validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        requests=Edit_Category_Request.query.all()[::-1]
        requests=[dict(id=edit_request.id, category_id=edit_request.category.id,
                       category_name=edit_request.category.name, reason=edit_request.reason,
                       sm_id=edit_request.store_manager.id, sm_name=edit_request.store_manager.first_name,
                       new_name=edit_request.name,
                       new_description=edit_request.description) for edit_request in requests]
        response['requests'] = requests
        response['msg'] = 'Successful'
        return response, 200

    @jwt_required()
    def delete(self, a_id, r_id):
        response, status, admin = validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        edit_request = Edit_Category_Request.query.get(r_id)
        if edit_request is None:
            return {'msg': "Request does not exist!"}, 404
        db.session.delete(edit_request)
        db.session.commit()
        return {'msg': "Request Deleted Successfully!"}, 200




class Admin_New_Category_Request(Resource):
    @jwt_required()
    def get(self, a_id):
        response, status, admin = validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        requests = New_Category_Request.query.all()[::-1]
        requests=[dict(id=new_request.id, name=new_request.name, description=new_request.description,
                       reason=new_request.reason, sm_id=new_request.store_manager.id,
                       sm_name=new_request.store_manager.first_name) for new_request in requests]
        response['requests'] = requests
        response['msg'] = 'Successful'
        return response, 200

    @jwt_required()
    def delete(self, a_id, r_id):
        response, status, admin = validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        new_request = New_Category_Request.query.get(r_id)
        if new_request is None:
            return {'msg': "Request does not exist!"}, 404
        db.session.delete(new_request)
        db.session.commit()
        return {'msg': "Request Deleted Successfully!"}, 200





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



class Admin_Product(Resource):
    @jwt_required()
    def get(self, a_id, p_id):
        response, status, admin = validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        product = Product.query.get(p_id)
        if product is None:
            response['msg'] = 'Product Not Found!'
            return response, 404
        response = product.make_json()
        response['msg'] = 'Successful'
        return response, 200


class Admin_New_Store_Manager(Resource):
    @jwt_required()
    def get(self, a_id):
        response, status, admin = validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        requests=Store_Manager.query.filter_by(approved=0).all()[::-1]
        requests=[dict(id=store_manager.id, first_name=store_manager.first_name,
                       last_name=store_manager.last_name, email_id=store_manager.email_id,
                       user_name=store_manager.user_name) for store_manager in requests]
        response['requests'] = requests
        response['msg'] = 'Successful'
        return response, 200

    @jwt_required()
    def put(self, a_id, sm_id):
        response, status, admin = validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        store_manager=Store_Manager.query.get(sm_id)
        if (store_manager is None) or (store_manager.approved!=0):
            return {'msg': 'Request does not exist!'}, 404
        store_manager.approved=1
        db.session.commit()
        return {'msg': 'Request Accepted Successfully!'}, 200

    @jwt_required()
    def delete(self, a_id, sm_id):
        response, status, admin = validate_admin(a_id, get_jwt())
        if admin is None:
            return response, status
        store_manager = Store_Manager.query.get(sm_id)
        if (store_manager is None) or (store_manager.approved!=0):
            return {'msg': 'Request does not exist!'}, 404
        db.session.delete(store_manager)
        db.session.commit()
        return {'msg': 'Request Declined Successfully!'}, 200


@cache.memoize(timeout=300)
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
api.add_resource(Admin_Delete_Category_Request, '/api/admin/<int:a_id>/delete_category_requests',
                 '/api/admin/<int:a_id>/delete_category_request/<int:r_id>')
api.add_resource(Admin_Edit_Category_Request, '/api/admin/<int:a_id>/edit_category_requests',
                 '/api/admin/<int:a_id>/edit_category_request/<int:r_id>')
api.add_resource(Admin_New_Category_Request, '/api/admin/<int:a_id>/new_category_requests',
                 '/api/admin/<int:a_id>/new_category_request/<int:r_id>')
api.add_resource(Admin_Categories, '/api/admin/<int:a_id>/categories')
api.add_resource(Admin_Product, '/api/admin/<int:a_id>/product/<int:p_id>')
api.add_resource(Admin_New_Store_Manager, '/api/admin/<int:a_id>/new_store_managers',
                 '/api/admin/<int:a_id>/new_store_manager/<int:sm_id>')
