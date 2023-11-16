from celery import shared_task
from flask_excel import make_response_from_array as create_csv
from .models import *

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




