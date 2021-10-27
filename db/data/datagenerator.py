from faker import Faker
from datetime import datetime
import random
import csv

fake = Faker()

def generate_users(n_users, num_sellers, products, orders):
	'''
	Generate data

	Parameters:
		n_users: number of users to generate
		num_sellers: number of sellers to pick
		products: number of products to generate
		orders: number of orders to generate
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
		pid = random.randint(0, products)
		newprod['product_id'] = pid
		product_id_set.add(pid)
		newprod['seller_id'] = random.choice(seller_list)
		categories = ['a', 'b', 'c', 'd', 'e', 'f']
		newprod['category'] = random.choice(categories)
		newprod['descript'] = fake.text()
		newprod['img_link'] = fake.image_url()
		newprod['price'] = round(random.uniform(0, 3000), 2)
		newprod['available'] = random.choice([True, False])
		product_data.append(newprod)

	write_file(product_data, "Products.csv")


	# Generate fake purchases
	purchase_data = []
	product_id_set = list(product_id_set)
	for i in range(0, orders):
		neworder = {}
		neworder['order_id'] = i
		neworder['product_id'] = random.choice(product_id_set)

		timestamp = fake.date_time_this_month()
		neworder['current_timestamp'] = timestamp.strftime('%Y-%m-%d %r')
		#neworder['total_price']
		neworder['num_items'] = random.randint(1, 20)
		neworder['fulfillment_status'] = random.choice(["Order received", "Shipped", "Delivered"])
		purchase_data.append(neworder)

	write_file(purchase_data, "Purchases.csv")


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
	n = 10
	ns = 5
	p = 10
	o = 10
	generate_users(n, ns, p, o)

main()


