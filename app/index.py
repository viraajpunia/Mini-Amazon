from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user
import datetime

from wtforms.validators import DataRequired

from .models.product import Product
from .models.purchase import Purchase
from .models.sellproduct import Sellproduct
from .models.user2 import User2

from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.route('/seller', methods=['GET', 'POST'])
def seller():
    id = request.args.get('seller_id')

    userinfo = User2.get(1)
    
    return render_template('seller.html',
                            user = userinfo)


@bp.route('/cart')
def cart():
    return render_template('cart.html')

@bp.route('/order')
def order():
    return render_template('order.html')

@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)


@bp.route('/search', methods=['GET', 'POST'])
def search():
    name = request.args.get("item")
    category = request.args.get("categories")
    if name == "":
        if category == "All":
            matches = Product.get_all(True)
        else:
            matches = Product.get_category(category)
    else:
        if category == "All":
            matches = Product.get_item(name)
        else:
            matches = Product.get_item_in_category(name, category)

    return render_template('index.html',
                           avail_products=matches,
                           purchase_history=None)


@bp.route('/more/<variable>', methods=['GET', 'POST'])
def moreInfo(variable):
    item = Product.get(variable)
    reviews = Product.get_all(True)
    sells_item = Sellproduct.get_by_product(variable)

    return render_template('products.html',
                           product=item,
                           sells= sells_item,
                           reviews=reviews)






