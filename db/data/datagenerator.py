from faker import Faker
from datetime import datetime
import random
import csv

fake = Faker()

def generate_users(n_users, num_sellers, products, sells_products, orders, n_carts, n_reviews, n_seller_reviews):
	'''
	Generate data

	Parameters:
		n_users: number of users to generate
		num_sellers: number of sellers to pick
		products: number of products to generate
		sells_products: number of seller-product pairs to generate
		orders: number of orders to generate
		n_carts: number of carts to generate
		n_reviews: number of reviews to generate
		n_seller_reviews: number of seller reviews to generate
	'''

	# Generate fake users and user accounts
	user_data = []
	account_data = []

	for i in range(0, n_users):
		newuser = {}
		newuser['uid'] = i
		newuser['first_name'] = fake.first_name()
		newuser['mid_name'] = fake.first_name()
		newuser['last_name'] = fake.last_name()
		newuser['email'] = fake.email()
		newuser['address'] = fake.address()
		newuser['password'] = fake.password()
		user_data.append(newuser)

		newacc = {}
		newacc['uid'] = i
		newacc['balance'] = round(random.uniform(0, 5000), 2)
		account_data.append(newacc)

	write_file(user_data, "Users.csv")
	write_file(account_data, "UserAccounts.csv")


	# Pick some users to also be sellers
	seller_list = []
	count = 0
	while count < num_sellers:
		seller = random.randint(0, n_users)
		if seller not in seller_list:
			seller_list.append(seller)
			count += 1

	with open('Sellers.csv', 'w') as f:
		writer = csv.writer(f)
		for s in seller_list:
			writer.writerow([s])


	# Generate fake products
	product_data = []
	product_id_set = set()

	for i in range(0, products):
		newprod = {}
		pid = i
		newprod['product_id'] = pid
		product_id_set.add(pid)
		categories = ['a', 'b', 'c', 'd', 'e', 'f']
		newprod['category'] = random.choice(categories)
		newprod['name'] = fake.word()
		newprod['descrip'] = fake.text()
		newprod['img_link'] = fake.image_url()
		newprod['price'] = round(random.uniform(0, 3000), 2)
		newprod['available'] = random.choice([True, False])
		product_data.append(newprod)

	write_file(product_data, "Products.csv")


	# Generate fake seller-product pairs
	sells_product_data = []
	sell_product_set = set()
	product_id_set = list(product_id_set)
	counter = 0
	while counter <  sells_products:
		new_sell_prod = {}
		new_sell_prod['seller_id'] = random.choice(seller_list)
		new_sell_prod['product_id'] = random.choice(product_id_set)
		if (new_sell_prod['seller_id'], new_sell_prod['product_id']) not in sell_product_set:
			sells_product_data.append(new_sell_prod)
			sell_product_set.add((new_sell_prod['seller_id'], new_sell_prod['product_id']))
			counter += 1

	write_file(sells_product_data, "SellProducts.csv")


	# Generate fake purchases
	purchase_data = []
	sell_product_set = list(sell_product_set)
	for i in range(0, orders):
		neworder = {}
		neworder['order_id'] = i
		sp = random.choice(sell_product_set)
		neworder['seller_id'] = sp[0]
		neworder['product_id'] = sp[1]

		timestamp = fake.date_time_this_month()
		neworder['current_timestamp'] = timestamp.strftime('%Y-%m-%d %r')

		neworder['uid'] = random.randint(0, n_users-1)

		neworder['num_items'] = random.randint(1, 20)
		neworder['fulfillment_status'] = random.choice(["Order received", "Shipped", "Delivered"])
		purchase_data.append(neworder)

	write_file(purchase_data, "Purchases.csv")


	cart_data = []
	for i in range(0, n_carts):
		newcart = {}
		newcart['uid'] = i
		newcart['product_id'] = random.choice(product_id_set)
		newcart['quantity'] = random.randint(1, 20)
		cart_data.append(newcart)

	write_file(cart_data, "Carts.csv")


	feedback_data = []
	for i in range(0, n_reviews):
		newreview = {}
		newreview['product_id'] = random.choice(product_id_set)
		newreview['uid'] = i
		newreview['rating'] = random.randint(1, 5)
		newreview['review'] = fake.sentence

		timestamp = fake.date_time_this_month()
		newreview['date'] = timestamp.strftime('%Y-%m-%d %r')

		feedback_data.append(newcart)

	write_file(feedback_data, "Feedback.csv")


	sellerReviews_data = []
	for i in range(0, n_seller_reviews):
		newsreview = {}
		newsreview['uid'] = i
		newsreview['review_id'] = random.randint(0, n_seller_reviews-1)
		newsreview['review'] = fake.sentence

		sellerReviews_data.append(newsreview)

	write_file(sellerReviews_data, "SellerReviews.csv")




def write_file(dict_data, csv_file):
	"""
	Writes a list of dictionaries to csv file.
	
	Parameters:
		dict_data: list of dictionaries
		csv_file: file name to write to
	"""
	try:
		with open(csv_file, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=dict_data[0].keys())
			for data in dict_data:
				writer.writerow(data)
	except IOError:
		print("I/O error")


def main():
	n = 20
	ns = 10
	p = 20
	sp = 20
	o = 20
	nc = 20
	nr = 20
	nsr = 20
	generate_users(n, ns, p, sp, o, nc, nr, nsr)

main()


