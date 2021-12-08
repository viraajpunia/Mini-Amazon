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
from .models.sellerfeedback import SellerFeedback
from .models.addtocart import addtocart


from flask import Blueprint
bp = Blueprint('index', __name__)

def truncate(num,n):
    temp = str(num)
    for x in range(len(temp)):
        if temp[x] == '.':
            try:
                return float(temp[:x+n+1])
            except:
                return float(temp)      
    return float(temp)

@bp.route('/seller/<variable>', methods=['GET', 'POST'])
def seller(variable):
    seller_id = variable

    #Get associated seller reviews
    reviews = SellerFeedback.get_by_uid(seller_id)
    #print(reviews, file=sys.stderr)

    #Get associated seller products
    userinfo = User2.get(seller_id)
    prods = Sellproduct.get_by_seller(seller_id) #prods returns all of the product_ids

    seller_products = []

    #Get average rating
    avg = 0

    for prod in prods:
        product_id = prod.product_id
        #print(product_id, file=sys.stderr)
        product_obj = Product.get(product_id)
        seller_products.append(product_obj)
        #print(product_obj, file=sys.stderr)

        ratings = [p.rating for p in ProductFeedback.get_item_reviews(product_id)]
        if len(ratings) != 0:
            avg += sum(ratings)/(len(ratings)*5)
        
    print(avg, file=sys.stderr)
    return render_template('seller.html',
                            user = userinfo,
                            products = seller_products,
                            reviews = reviews,
                            avg = truncate(avg,2))

@bp.route('/nonsellerpublicinfo/<variable>', methods=['GET', 'POST'])
def nonsellerpublicinfo(variable):
    id = request.args.get('uid')
    email = request.args.get('email')
    password = request.args.get('password')

    userinfo = User.get(variable)
    
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

@bp.route('/newuseracctpage/<variable>', methods=['GET', 'POST'])
def newuseracctpage(variable):
    id = request.args.get('uid')
    email = request.args.get('email')
    password = request.args.get('password')

    userinfo = User.get(variable)
    purchase = Purchase.get_all_by_uid(variable)
    account = UserAccount.get(variable)
    
    
    return render_template('newuseracctpage.html',
                            user = userinfo, purchase = purchase, acct  = account)


@bp.route('/cart', methods=['GET', 'POST'])
def cart():
    #carts = Product.get_all(True)
    #uid = current_user.id
    uid = request.args.get("uid")
    num = request.args.get("num")
    product_id = request.args.get("product_id")
    seller_id = request.args.get("seller_id")
    print(num, file=sys.stderr)
    print(product_id, file=sys.stderr)
    print(seller_id, file=sys.stderr)
    #if product_id not in 
    addtocart.addtocart(uid, product_id, seller_id, num)
    carts = UserCart.get(uid)

    return render_template('cart.html', cartofuser = carts)

@bp.route('/cartdisplay', methods=['GET', 'POST'])
def cartdisplay():
    uid = current_user.id
    carts = UserCart.get(uid)
    return render_template('cart.html', cartofuser = carts)


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
    delete = request.form.get("delete")
    #if True then delete the review
    if delete == "True":
        Review.delete_row(current_user.id)
    

    review = request.form.get("edit_review")
    edit = request.form.get("edit")
    if edit == "True":
        Review.update_row(current_user.id,review)
        
    item = Product.get(variable)
    reviews = ProductFeedback.get_item_reviews(variable)
    sells_item = Sellproduct.get_by_product(variable)
    rating = AvgRating.get_item_avg_rating(variable)

    


    return render_template('products.html',
                           product=item,
                           sells=sells_item,
                           reviews=reviews,
                           rate=rating,
                           current_user = current_user)

@bp.route('/review/<variable>', methods=["POST","GET"])
def review(variable):
    buyer_id = current_user.id
    product_id = variable
    rating = request.form.get("stars")
    review = request.form.get("review")
    date = datetime.datetime.now()
    
    Review.post_rating(buyer_id, product_id, rating, review, date)
    
    title = "Thank you for leaving a review :)"

    return render_template('review.html',
                            title=title, 
                            content = review,
                            rating = rating)



@bp.route('/additem', methods=['GET', 'POST'])
def additem():
    name = request.args.get("name")
    category = request.args.get("category")
    descrip = request.args.get("descrip")
    img_link = request.args.get("img_link")
    price = request.args.get("price")

    total_items = Product.get_all()

    Product.add_item(len(total_items), name, category, descrip, img_link, price)
    Sellproduct.add_sell_item(current_user.id, len(total_items))

    seller_id = current_user.id

    #Get associated seller reviews
    reviews = SellerFeedback.get_by_uid(seller_id)
    #print(reviews, file=sys.stderr)

    #Get associated seller products
    userinfo = User2.get(seller_id)
    prods = Sellproduct.get_by_seller(seller_id) #prods returns all of the product_ids

    seller_products = []

    #Get average rating
    avg = 0

    for prod in prods:
        product_id = prod.product_id
        #print(product_id, file=sys.stderr)
        product_obj = Product.get(product_id)
        seller_products.append(product_obj)
        #print(product_obj, file=sys.stderr)

        ratings = [p.rating for p in ProductFeedback.get_item_reviews(product_id)]
        if len(ratings) != 0:
            avg += sum(ratings)/(len(ratings)*5)

    return render_template('seller.html',
                            user = userinfo,
                            products = seller_products,
                            reviews = reviews,
                            avg = truncate(avg,2))

'''
@bp.route('/edit', method=['GET', 'POST'])
def edit():
    name = request.args.get("name")
    category = request.args.get("category")
    descrip = request.args.get("descrip")
    img_link = request.args.get("img_link")
    price = request.args.get("price")

    Product.edit_item(name, category, descrip, img_link, price)

    seller_id = current_user.id

    #Get associated seller reviews
    reviews = SellerFeedback.get_by_uid(seller_id)
    #print(reviews, file=sys.stderr)

    #Get associated seller products
    userinfo = User2.get(seller_id)
    prods = Sellproduct.get_by_seller(seller_id) #prods returns all of the product_ids

    seller_products = []

    #Get average rating
    avg = 0

    for prod in prods:
        product_id = prod.product_id
        #print(product_id, file=sys.stderr)
        product_obj = Product.get(product_id)
        seller_products.append(product_obj)
        #print(product_obj, file=sys.stderr)

        ratings = [p.rating for p in ProductFeedback.get_item_reviews(product_id)]
        if len(ratings) != 0:
            avg += sum(ratings)/(len(ratings)*5)

    return render_template('seller.html',
                            user = userinfo,
                            products = seller_products,
                            reviews = reviews,
                            avg = truncate(avg,2))
'''
'''
@bp.route('/remove', methods=['GET', 'POST'])
def remove():
    name = request.args.get("name")

    prod_by_name = Product.get_item(name)
    #print(prod_by_name, file=sys.stderr)

    #pid = prod_by_name[0].product_id


    Sellproduct.delete_sell_item(current_user.id, pid)

    seller_id = current_user.id

    #Get associated seller reviews
    reviews = SellerFeedback.get_by_uid(seller_id)
    #print(reviews, file=sys.stderr)

    #Get associated seller products
    userinfo = User2.get(seller_id)
    prods = Sellproduct.get_by_seller(seller_id) #prods returns all of the product_ids

    seller_products = []

    #Get average rating
    avg = 0

    for prod in prods:
        product_id = prod.product_id
        #print(product_id, file=sys.stderr)
        product_obj = Product.get(product_id)
        seller_products.append(product_obj)
        #print(product_obj, file=sys.stderr)

        ratings = [p.rating for p in ProductFeedback.get_item_reviews(product_id)]
        if len(ratings) != 0:
            avg += sum(ratings)/(len(ratings)*5)

    return render_template('seller.html',
                            user = userinfo,
                            products = seller_products,
                            reviews = reviews,
                            avg = truncate(avg,2))
'''
