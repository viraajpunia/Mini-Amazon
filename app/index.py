from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user
import datetime
import sys

from wtforms.validators import DataRequired

from .models.product import Product
from .models.purchase import Purchase
from .models.sellproduct import Sellproduct
from .models.user2 import User2
from .models.user import User
from .models.cart import UserCart
from .models.useracct import UserAccount
from .models.productfeedback import ProductFeedback
from .models.avgratings import AvgRating
from .models.review import Review


from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.route('/seller/<variable>', methods=['GET', 'POST'])
def seller(variable):
    
    #id = request.args.get('seller_id')

    userinfo = User2.get(variable)
    #prods = Sellproduct.get_by_seller(10)
    prods = Sellproduct.get_by_seller(variable) #prods returns all of the product_ids

    seller_products = []

    for prod in prods:
        product_id = prod.product_id
        #print(product_id, file=sys.stderr)
        product_obj = Product.get(product_id)
        seller_products.append(product_obj)
        #print(product_obj, file=sys.stderr)

    return render_template('seller.html',
                            user = userinfo,
                            products = seller_products)

@bp.route('/nonsellerpublicinfo/<variable>', methods=['GET', 'POST'])
def nonsellerpublicinfo(variable):
    #id = request.args.get('uid')
    #email = request.args.get('email')
    #password = request.args.get('password')

    userinfo = User2.get(variable)
    
    return render_template('nonsellerpublicinfo.html',
                            user = userinfo)

@bp.route('/useracctpage', methods=['GET', 'POST'])
def useracctpage():
    id = request.args.get('uid')
    email = request.args.get('email')
    password = request.args.get('password')

    userinfo = User2.get(7)
    purchase = Purchase.get(7)
    account = UserAccount.get(7)
    
    
    return render_template('useracctpage.html',
                            user = userinfo, purchase = purchase, acct  = account)

@bp.route('/newuseracctpage', methods=['GET', 'POST'])
def newuseracctpage():
    id = request.args.get('uid')
    email = request.args.get('email')
    password = request.args.get('password')

    userinfo = User2.get(8)
    purchase = Purchase.get(7)
    account = UserAccount.get(8)
    
    
    return render_template('newuseracctpage.html',
                            user = userinfo, purchase = purchase, acct  = account)


@bp.route('/cart')
def cart():
    carts = UserCart.cart_by_user("1")
    item = Product.get(5)
    return render_template('cart.html', cartofuser = carts, product = item)

@bp.route('/order')
def order():
    item = Product.get(5)
    return render_template('order.html', product = item)

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
    reviews = ProductFeedback.get_item_reviews(variable)
    sells_item = Sellproduct.get_by_product(variable)
    rating = AvgRating.get_item_avg_rating(variable)
    
    return render_template('products.html',
                           product=item,
                           sells=sells_item,
                           reviews=reviews,
                           rate=rating)

@bp.route('/review/<variable>', methods=["POST","GET"])
def review(variable):
    buyer_id = 1 #hardcoded, change later
    product_id = variable
    rating = request.form.get("stars")
    review = request.form.get("review")
    date = datetime.datetime.now()
    
    #Review.post_rating(buyer_id, product_id, rating, review, date)
    
    title = "Thank you for leaving a review :)"

    return render_template('review.html',
                            title=title, 
                            content = review,
                            rating = rating)






