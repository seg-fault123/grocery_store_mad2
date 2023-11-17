from celery import shared_task
from jinja2 import Template
from .my_mail import send_mail
from flask_excel import make_response_from_array as create_csv
from .models import *
from datetime import date, timedelta

@shared_task(ignore_result=False)
def create_store_manager_report(sm_id):
    products=Product.query.filter_by(sm_id=sm_id).all()
    array=[]
    array.append(['Product ID', 'Product Name', 'Product Description', 'Price', 'Unit Measure', "Stock",
                  "Units Sold", "Category Name"])
    for product in products:
        array.append([product.id, product.name, product.description, product.price, product.unit_measure,
                      product.stock, product.units_sold, product.category.name])
    csv_result=create_csv(array, 'csv')
    filename='report.csv'
    with open(filename, 'wb') as file:
        file.write(csv_result.data)
    return filename


@shared_task(ignore_result=True)
def send_daily_reminder():
    customers=Customer.query.filter(Customer.last_active!=date.today()).all()
    subject="Daily Reminder for Groceries"
    body="""
    Hey {0}!
    Looks like you haven't logged in to the Grocery Store today.
    Visit the website to buy your daily groceries seamlessly.
    """
    for customer in customers:
        send_mail(customer.email_id, subject, body.format(customer.first_name), 'plain')
    return "Done"

@shared_task(ignore_result=True)
def send_monthly_report():
    customers=Customer.query.all()
    today=date.today()
    max_date=today-timedelta(days=1)
    min_date=date(year=max_date.year, month=max_date.month, day=1)
    subject=f'Your Monthly Report for {min_date.strftime("%B")} {min_date.year}'
    for customer in customers:
        orders=Order.query.filter(Order.date.between(min_date, max_date), Order.customer_id==customer.id).all()
        total_orders=len(orders)
        grand_total=0
        for order in orders:
            for order_product in order.order_products:
                grand_total+=(order_product.quantity * order_product.product.price)
        with open('monthly_report.html') as file:
            mail=Template(file.read())
            send_mail(customer.email_id, subject, mail.render(customer_name=customer.first_name,
                                                              orders=orders, total_orders=total_orders,
                                                              grand_total=grand_total), 'html')

