from flask import Flask
import os
from application.database import db
from flask_cors import CORS
from application.worker import celery_init_app
from celery.schedules import crontab
from flask_excel import init_excel
from application.tasks import send_daily_reminder, send_monthly_report

app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///{0}'.format(os.path.join(os.getcwd(), 'store.db'))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.getcwd() + r'/store.db'
app.config['JWT_SECRET_KEY']='EvI1xOU73MuhiGNd4Qr-ZA'
app.config['JWT_ACCESS_TOKEN_EXPIRES']=False
app.config['CACHE_TYPE']='RedisCache'
app.config['CACHE_REDIS_HOST']='localhost'
app.config['CACHE_REDIS_PORT']=6379


db.init_app(app)
cors=CORS(app, origins='http://localhost:8080')
celery_app=celery_init_app(app)
init_excel(app)
app.app_context().push()


def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
    dbapi_con.execute('pragma foreign_keys=ON')


with app.app_context():
    from application.customer_api import *
    from application.admin_api import *
    from application.store_manager_api import *
    from sqlalchemy import event
    event.listen(db.engine, 'connect', _fk_pragma_on_connect)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=12, minute=20),
                             send_daily_reminder.s())
    # sender.add_periodic_task(100, send_daily_reminder.s())
    sender.add_periodic_task(crontab(day_of_month=9, hour=12, minute=20),
                             send_monthly_report.s())
    # sender.add_periodic_task(200, send_monthly_report.s())


if __name__=='__main__':
    # print('sqlite:///{0}'.format(os.path.join(os.getcwd(), 'store.db')))
    app.run(debug=True)
    

