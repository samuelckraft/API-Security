from flask import Flask
from database import db
from schema import ma

from models.customer import Customer
from models.employee import Employee
from models.product import Product
from models.order import Order
from models.production import Production


from routes.customerBP import customer_blueprint
from routes.employeeBP import employee_blueprint
from routes.productBP import product_blueprint
from routes.orderBP import order_blueprint
from routes.productionBP import production_blueprint

from limiter import limiter

from caching import cache

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    return app

def blue_print_config_customer(app):
    app.register_blueprint(customer_blueprint, url_prefix='/customers')

def blue_print_config_employee(app):
    app.register_blueprint(employee_blueprint, url_prefix='/employees')

def blue_print_config_order(app):
    app.register_blueprint(order_blueprint, url_prefix='/orders')

def blue_print_config_product(app):
    app.register_blueprint(product_blueprint, url_prefix='/products')

def blue_print_config_productions(app):
    app.register_blueprint(production_blueprint, url_prefix='/productions')


def configure_rate_limit():
    limiter.limit("5 per day")(customer_blueprint)
    limiter.limit("5 per day")(employee_blueprint)
    limiter.limit("5 per day")(order_blueprint)
    limiter.limit("5 per day")(product_blueprint)
    limiter.limit("5 per day")(production_blueprint)

if __name__ == '__main__':
    app = create_app('DevelopmentConfig')

    blue_print_config_customer(app)
    blue_print_config_employee(app)
    blue_print_config_order(app)
    blue_print_config_product(app)
    blue_print_config_productions(app)
    configure_rate_limit()

    with app.app_context():
        db.create_all()

    app.run(debug=True)