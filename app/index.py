from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user
import datetime

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__)


#class SearchForm(Form):
#  search = StringField('search', [DataRequired()])
#  submit = SubmitField('Search',
#                       render_kw={'class': 'btn btn-success btn-block'})


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
    if name == "":
        matches = Product.get_all(True)
    else:
        matches = Product.get_item(name)

    return render_template('index.html',
                           avail_products=matches,
                           purchase_history=None)

