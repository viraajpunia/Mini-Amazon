from flask import Flask, render_template, request, redirect, url_for, flash
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
    
    #Logic for submitting a new review for the Seller
    #seller_ids = the sellers that the logged in user has bought from 
    seller_ids = Purchase.get_sellers_by_uid(current_user.id)
    leave_review = False
    
    if int(seller_id) in seller_ids:
        print("User has bought from this seller", file=sys.stderr)
        leave_review = True
    
    new_review = request.form.get("seller_review")
    #SellerFeedback.post_review(seller_id,new_review)
    
    #Aggregate number of reviews for this seller
    num_reviews = SellerFeedback.get_num_reviews(seller_id)
    #print(num_reviews,file=sys.stderr)

    return render_template('seller.html',
                            user = userinfo,
                            products = seller_products,
                            reviews = reviews,
                            avg = truncate(avg,2),
                            leave_review = leave_review,
                            num_reviews=num_reviews)

@bp.route('/sellerpublic/<variable>', methods=['GET', 'POST'])
def sellerpublic(variable):
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
    
    #Logic for submitting a new review for the Seller
    #seller_ids = the sellers that the logged in user has bought from 
    seller_ids = Purchase.get_sellers_by_uid(current_user.id)
    leave_review = False
    
    if int(seller_id) in seller_ids:
        print("User has bought from this seller", file=sys.stderr)
        leave_review = True
    
    new_review = request.form.get("seller_review")
    #SellerFeedback.post_review(seller_id,new_review)
    
    #Aggregate number of reviews for this seller
    num_reviews = SellerFeedback.get_num_reviews(seller_id)
    #print(num_reviews,file=sys.stderr)

    return render_template('sellerpublic.html',
                            user = userinfo,
                            products = seller_products,
                            reviews = reviews,
                            avg = truncate(avg,2),
                            leave_review = leave_review,
                            num_reviews=num_reviews)

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

@bp.route('/updateuserinfo/<variable>', methods=['GET', 'POST'])
def updateuserinfo(variable):

    
    newfirstname = request.form.get("editfirstname")
    editfirstname = request.form.get("editfirstnamebutton")
    if editfirstname == "True":
        User.updatefirstname(current_user.id, newfirstname)

    newmiddlename = request.form.get("editmiddlename")
    editmiddlename = request.form.get("editmiddlenamebutton")
    if editmiddlename == "True":
        User.updatemiddlename(current_user.id, newmiddlename)

    newlastname = request.form.get("editlastname")
    editlastname = request.form.get("editlastnamebutton")
    if editlastname == "True":
        User.updatelastname(current_user.id, newlastname)

    newlastname = request.form.get("editlastname")
    editlastname = request.form.get("editlastnamebutton")
    if editlastname == "True":
        User.updatelastname(current_user.id, newlastname)

    newemail = request.form.get("editemail")
    editemail = request.form.get("editemailbutton")
    if editemail == "True" and not(User.email_exists(newemail)):
        User.updateemail(current_user.id, newemail)

    newpassword = request.form.get("editpassword")
    editpassword = request.form.get("editpasswordbutton")
    if editpassword == "True" and not(User.email_exists(newpassword)):
        User.updatepassword(current_user.id, newpassword)

    newaddress = request.form.get("editaddress")
    editaddress = request.form.get("editaddressbutton")
    if editaddress == "True":
        User.updateaddress(current_user.id, newaddress)

    newbalance = request.form.get("editbalance")
    editbalance = request.form.get("editbalancebutton")
    if editbalance == "True":
        User.updatebalance(current_user.id, newbalance)

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
    delete = request.form.get("delete1")
    #if delete == "True":
        #addtocart.delete_from_cart(uid, product_id, seller_id, num)
    print(num, file=sys.stderr)
    print(product_id, file=sys.stderr)
    print(seller_id, file=sys.stderr)
    #if product_id not in 
    checked = addtocart.check(uid, product_id, seller_id)
    if len(checked) == 0:
        addtocart.addtocart(uid, product_id, seller_id, num)
    else:
        n = int(checked[0].quantity) + int(num)
        addtocart.update(uid, product_id, seller_id, n)
    carts = UserCart.get(uid)
    price = [float(i.price)*float(i.quantity) for i in carts]
    total = sum(price)
    return render_template('cart.html', cartofuser = carts, product = truncate(total,2))

@bp.route('/cartdisplay', methods=['GET', 'POST'])
def cartdisplay():
    uid = current_user.id
    
    product_id = request.form.get("product_id")
    seller_id = request.form.get("seller_id")
    num = request.form.get("num")
    print(product_id,file=sys.stderr)

    plus = request.form.get("plus")
    if plus == "True":
        n = int(num)+1
        addtocart.update(uid, product_id, seller_id, str(n))
    minus = request.form.get("minus")
    if minus == "True":
        n = int(num)-1
        addtocart.update(uid, product_id, seller_id, str(n))
        if n==0:
            addtocart.delete_from_cart(uid, product_id, seller_id)
    delete = request.form.get("delete1")
    if delete == "True":
       addtocart.delete_from_cart(uid, product_id, seller_id)
    carts = UserCart.get(uid)
    price = [float(i.price)*float(i.quantity) for i in carts]
    total = sum(price)
    return render_template('cart.html', cartofuser = carts, product = truncate(total,2))


@bp.route('/order', methods=['GET', 'POST'])
def order():
    items = UserCart.get(current_user.id)
    price = [float(i.price)*float(i.quantity) for i in items]
    balance = items[0].balance
    total = sum(price)
    promo = request.form.get("promo")
    usercode = request.form.get("usercode")
    print(usercode,file=sys.stderr)
    print(promo,file=sys.stderr)
    if (promo=="True" and (usercode=="20-OFF" or usercode=="HOLIDAYS" or usercode=="SUMMERFUN")):
        total = total*0.80
    return render_template('order.html', product = truncate(total,2), balance = balance)


@bp.route('/submitted')
def submitted():
    items = UserCart.get(current_user.id)
    uid = current_user.id
    price = [float(i.price)*float(i.quantity) for i in items]
    total = sum(price)
    balance = items[0].balance
    carts = UserCart.get(uid)
    if (balance>=total):
        newbalance = balance-total
        UserCart.update(uid, truncate(newbalance,3))
        addtocart.delete_cart(uid)
        return render_template('submitted.html', cartofuser = carts, items=items, total = truncate(total,2), newbalance=newbalance)
    else:
        return render_template('insufficient.html')

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
    sort = request.args.get("sort")
    if name == "":
        if category == "All":
            matches = Product.get_all(True)
            if sort == "price":
                matches = Product.get_all_sorted(True)
        else:
            matches = Product.get_category(category)
            if sort == "price":
                matches = Product.get_category_sorted(category)
    else:
        if category == "All":
            matches = Product.get_item(name)
            #matches = Product.get_item_keyword(name)
            if sort == "price":
                matches = Product.get_item_sorted(name)
        else:
            matches = Product.get_item_in_category(name, category)
            if sort == "price":
                matches = Product.get_category_sorted(category)

    return render_template('index.html',
                           avail_products=matches,
                           purchase_history=None)

#variable = product_id
@bp.route('/more/<variable>', methods=['GET', 'POST'])
def moreInfo(variable):
    product_id = variable
    delete = "False"
    delete = request.form.get("delete")
    #if True then delete the review
    if delete == "True":
        Review.delete_row(current_user.id)
    
    review = request.form.get("edit_review")
    edit = request.form.get("edit")
    if edit == "True":
        new_stars = request.form.get("new_stars")
        Review.update_row(current_user.id,review,new_stars)
        
    item = Product.get(variable)
    reviews = ProductFeedback.get_item_reviews(variable)
    sells_item = Sellproduct.get_by_product(variable)
    rating = AvgRating.get_item_avg_rating(variable)

    #Check if current user has already submitted a review:
    already_reviewed = False
    buyer_ids = Review.list_ratings_buyer_ids(current_user.id,variable)
    if current_user.id in buyer_ids:
        print("Current user already reviewed this product",file=sys.stderr)
        already_reviewed = True

    return render_template('products.html',
                           product=item,
                           sells=sells_item,
                           reviews=reviews,
                           rate=rating,
                           current_user = current_user,
                           already_reviewed = already_reviewed)

@bp.route('/review/<variable>', methods=["POST","GET"])
def review(variable):
    buyer_id = current_user.id
    product_id = variable
    rating = request.form.get("stars")
    review = request.form.get("review")
    date = datetime.datetime.now()
    
    Review.post_rating(buyer_id, product_id, rating, review, date)
    print("Review Posted", file=sys.stderr)
    title = "Thank you for leaving a review :)"

    return render_template('review.html',
                            title=title, 
                            content = review,
                            rating = rating,
                            product_id=product_id)

@bp.route('/my_reviews/<variable>', methods=["POST","GET"])
def my_reviews(variable):
    product_id = request.form.get("product_id")
    delete = request.form.get("delete")
    #if True then delete the review
    if delete == "True":
        Review.delete_row_product_id(product_id)
    
    review = request.form.get("edit_review")
    edit = request.form.get("edit")
    if edit == "True":
        new_stars = request.form.get("new_stars")
        Review.update_row_2(current_user.id,review,new_stars,product_id)
        
    buyer_id = variable
    reviews = Review.list_ratings(buyer_id)
    
    #print(reviews, file=sys.stderr)

    return render_template('my_reviews.html',reviews=reviews)



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

@bp.route('/remove', methods=['GET', 'POST'])
def remove():
    name = request.args.get("name")

    prod_by_name = Product.get_item(name)
    #print(prod_by_name, file=sys.stderr)

    pid = prod_by_name[0].id


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

@bp.route('/edit', methods=['GET', 'POST'])
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