from .database import db


class Admin(db.Model):
    __tablename__='admin'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    email_id=db.Column(db.String, unique=True, nullable=False)
    user_name=db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    access_token=db.Column(db.String, nullable=False, unique=True)
    role_id=db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    def make_json(self):
        response=dict(id=self.id, email_id=self.email_id,user_name=self.user_name,
                      access_token=self.access_token, role_id=self.role_id, role_name=self.role.name)
        return response


class Cart_Product(db.Model):
    customer_id=db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    product_id=db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity=db.Column(db.Integer, nullable=False)
class Category(db.Model):
    __tablename__='category'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    name=db.Column(db.String, nullable=False, unique=True)
    description=db.Column(db.String, nullable=False)
    products=db.relationship('Product', backref='category')
    def make_json(self):
        response=dict(id=self.id, name=self.name, description=self.description)
        products=[{'id': product.id, 'name': product.name} for product in self.products]
        response['products']=products
        return response

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name=db.Column(db.String, nullable=False)
    last_name=db.Column(db.String, default='')
    email_id=db.Column(db.String, unique=True, nullable=False)
    user_name=db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    access_token=db.Column(db.String, unique=True)
    role_id=db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    last_active=db.Column(db.Date)
    def make_json(self):
        response=dict(id=self.id, first_name=self.first_name, last_name=self.last_name,
                      email_id=self.email_id, user_name=self.user_name, access_token=self.access_token,
                      role_id=self.role_id, role_name=self.role.name)
        return response

class Delete_Category_Request(db.Model):
    __tablename__='delete_category_request'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    reason=db.Column(db.String, nullable=False)
    category_id=db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    sm_id=db.Column(db.Integer, db.ForeignKey('store_manager.id'), nullable=False)
    category=db.relationship('Category')

class Edit_Category_Request(db.Model):
    __tablename__ = 'edit_category_request'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    reason = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    sm_id = db.Column(db.Integer, db.ForeignKey('store_manager.id'), nullable=False)
    category=db.relationship('Category')

class New_Category_Request(db.Model):
    __tablename__ = 'new_category_request'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    reason = db.Column(db.String, nullable=False)
    sm_id = db.Column(db.Integer, db.ForeignKey('store_manager.id'), nullable=False)

class Order(db.Model):
    __tablename__='order'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    date=db.Column(db.Date, nullable=False)
    customer_id=db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer=db.relationship('Customer', backref='orders')

class Order_Product(db.Model):
    __tablename__='order_product'
    order_id=db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id=db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity=db.Column(db.Integer, nullable=False)

class Product(db.Model):
    __tablename__='product'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    price=db.Column(db.Integer, nullable=False)
    unit_measure=db.Column(db.String, nullable=False)
    stock=db.Column(db.Integer, nullable=False)
    units_sold=db.Column(db.Integer, nullable=False, default=0)
    category_id=db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    sm_id=db.Column(db.Integer, db.ForeignKey('store_manager.id'), nullable=False)
    mfg_date=db.Column(db.Date)
    exp_date=db.Column(db.Date)
    store_manager=db.relationship('Store_Manager', backref='products')
    def make_json(self):
        response=dict(id=self.id, name=self.name, description=self.description,
                      price=self.price, unit_measure=self.unit_measure, stock=self.stock,
                      units_sold=self.units_sold, category_id=self.category_id,
                      category_name=self.category.name, sm_id=self.sm_id)
        return response

class Role(db.Model):
    __tablename__='role'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    name=db.Column(db.String, nullable=False, unique=True)
    description=db.Column(db.String, default='')
    customers=db.relationship('Customer', backref='role')
    admins=db.relationship('Admin', backref='role')
    store_managers=db.relationship('Store_Manager', backref='role')

class Store_Manager(db.Model):
    __tablename__='store_manager'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, default='')
    email_id = db.Column(db.String, unique=True, nullable=False)
    user_name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    access_token = db.Column(db.String, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    approved=db.Column(db.Integer, nullable=False, default=0)
