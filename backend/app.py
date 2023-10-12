from flask import Flask
import os
from application.database import db


app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///{0}'.format(os.path.join(os.getcwd(), 'store.db'))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.getcwd() + r'\store.db'
app.config['JWT_SECRET_KEY']='EvI1xOU73MuhiGNd4Qr-ZA'
app.config['JWT_ACCESS_TOKEN_EXPIRES']=False

db.init_app(app)
app.app_context().push()

with app.app_context():
    from application.customer_api import *
    from application.admin_api import *
    from application.store_manager_api import *

if __name__=='__main__':
    # print('sqlite:///{0}'.format(os.path.join(os.getcwd(), 'store.db')))
    app.run(debug=True)
    

