# -*- coding: utf-8 -*-
import json

#Internal method
def __valid_product(name):
	"""
	This call is used to validate the existence of product in catalog with correct name and amount
	"""
	product_name = db.product_catalog.name == name
	query = db(product_name).select().first()
	if query.amount > 0:
		return True
	return False

def __valid_id(catalog_id):
	"""
	This call is used to validate the existence of product in catalog with correct id
	"""
	product_id = db.product_catalog.id == catalog_id
	query = db(product_id).select().first()
	if query.amount > 0:
		return True
	return False


#Commonly used response
def invalid_product():
	"""
	Returns the values that the product mentioned was invalid and data needs to be provided again.
	"""
	return dict(success = False, reason = "Not a valid basket product")

#API Features
def add_product():
	"""
	This call checks if the product is already added in catalog database, otherwise adds the product and returns its product ID.
	"""
	data = json.loads(request.body.read())
	
	#Checking for validity of inputs if following keys exist
	if not data.get("name") or not data.get("amount") or not data.get("price"):
		redirect('invalid_product.json')

	product_name = data["name"]
	product_amount = int(data["amount"])
	product_price = int(data["price"])
	
	product = db.product_catalog.name == product_name
	query = db(product).select().first()
	
	# Product already in the database
	if query:
		return dict(success = False, reason = "Product already in catalog")
	
	#Product added and ID returned
	product_id = db.product_catalog.insert(name = product_name, amount = product_amount, price = product_price)
	
	return dict(success = True, product_id = product_id, reason = 'Product added successfully to catalog')

def edit_product():
	"""
	This call lets you edit any product after checking its validity and lets you update price or amount or both in catalog.
	"""
	data = json.loads(request.body.read())

	#Checking for existence and validity of provided name
	if not data.get("name") or not __valid_product(data["name"]):
		redirect('invalid_product.json')

	product_name = data["name"]
	product_amount = int(data["amount"])
	product_price = int(data["price"])

	query = db.product_catalog.name == product_name

	if product_amount and product_price:
		db(query).update(amount = product_amount, price = product_price)
		return dict(success = True, reason = 'Amount and Price updated')
	
	elif product_amount:
		db(query).update(amount = product_amount)
		return dict(success = True, reason = 'Amount updated')
	
	elif product_price:
		db(query).update(price = product_price)
		return dict(success = True, reason = 'Price updated')

def remove_product():
	"""
	This call is used to remove any product from catalog deleting all the information related to amount and price of the product.
	"""
	data = json.loads(request.body.read())

	#Checking for existence and validity of provided name
	if not data.get("name") or not __valid_product(data["name"]):
		redirect('invalid_product.json')

	product_name = data["name"]
	
	query = db.product_catalog.name == product_name
	db(query).delete()
	db.commit()
	
	return dict(success = True, reason = 'Product successfully removed from catalog')

def add_product_to_basket():
	"""
	This call checks if the product is already added in shopping basket, otherwise adds the product and returns its product ID.
	"""
	data = json.loads(request.body.read())

	#Checking for validity of inputs if following keys exist
	if not data.get("name") or not data.get("amount"):
		redirect('invalid_product.json')

	product_name = data["name"]
	purchase_amount = int(data["amount"])

	if not __valid_product(product_name):
		redirect('invalid_product.json')

	query = db.product_catalog.name == product_name
	product = db(query).select().first()

	query2 = db.shopping_basket.name == product_name
	basket_entry = db(query2).select().first()

	#Checking for existence of product in basket
	if basket_entry:
		if product.name == basket_entry.name:
			return dict(success = False, reason = "Product already in basket")

	#Checking for availability of Product in inventory(database)
	if product.amount > purchase_amount:
		product_id = db.shopping_basket.insert(name = product_name, catalog_id = product.id , purchase_amount = purchase_amount)
		new_amount = product.amount - purchase_amount
		db(query).update(amount = new_amount)
		return dict(success = True, product_id = product_id, reason = "Product added successfully to basket")

	else:
		return dict(success = False, reason = "Product not available")	
	
def edit_product_from_basket():
	"""
	This call lets you edit any product from shopping basket after checking its validity and lets you update purchase amount in basket 
	"""
	data = json.loads(request.body.read())

	#Checking for existence of keys
	if not data.get("name") or not data.get("amount") or not __valid_product(data["name"]):
		redirect('invalid_product.json')

	product_name = data["name"]
	purchase_amount = int(data["amount"])

	query = db.shopping_basket.name == product_name
	basket_entry = db(query).select().first()

	query2 = db.product_catalog.name == product_name
	product = db(query2).select().first()

	if not basket_entry:		
		return dict(success = False, reason = "Product not in basket")
	
	db(query).update(purchase_amount = purchase_amount)
	new_amount = basket_entry.purchase_amount + product.amount - purchase_amount
	db(query2).update(amount = new_amount)

	return dict(success = True, reason = 'Basket successfully updated')	
		
def remove_product_from_basket():
	"""
	This call is used to remove any product from shopping basket deleting all the information related to purchase amount of the product.
	"""
	data = json.loads(request.body.read())

	#Checking for existence and validity of provided name
	if not data.get("name") or not __valid_product(data["name"]):
		redirect('invalid_product.json')

	product_name = data["name"]

	query = db.shopping_basket.name == product_name
	basket_entry = db(query).select().first()

	query2 = db.product_catalog.name == product_name
	product = db(query2).select().first()

	if not basket_entry:
		return dict(success = False, reason = "Product not in basket")

	new_amount = basket_entry.purchase_amount + product.amount
	db(query).delete()
	db(query2).update(amount = new_amount)
	db.commit()

	return dict(success = True, reason = 'Product successfully removed from basket')
		
def query_products_from_catalog():
	"""
	This call is used to query products from catalog based on name or price or price range, sort it according to name or price and group the
	products by specified price range.
	"""
	data = json.loads(request.body.read())
	pagination = (0,100) 
	
	if data.has_key("sort"):
		sorting_parameter = data["sort"]

	#Building query based on provided inputs
	if data.has_key("name"):
		product_name = data["name"]
		query = db.product_catalog.name.contains(product_name)

	elif data.has_key("price"):
		product_price = int(data["price"])
		query = db.product_catalog.price == product_price

	else:
		query = db.product_catalog.id > 0
	
	#Building a new query for grouping output by price range
	if data.has_key("min_price"):
		min_price = int(data["min_price"])
		min_range = db.product_catalog.price > min_price 
		query2 = min_range

	if data.has_key("max_price"):
		max_price = int(data["max_price"])
		max_range = db.product_catalog.price < max_price 
		query2 = max_range
		
	if data.has_key("min_price") & data.has_key("max_price"):
		price_range = min_range & max_range
		query2 = price_range

	#Sorting and grouping of query results
	if sorting_parameter:
		rows = db(query).select(
			limitby = pagination,
			orderby = getattr(db.product_catalog,sorting_parameter))

	if query2 != None:
		rows = db(query).select(
			limitby = pagination,
			groupby = db.product_catalog.name, having = query2)

	elif query2 != None and sorting_parameter:
		rows = db(query).select(
			limitby = pagination,
			orderby = getattr(db.product_catalog,sorting_parameter),
			groupby = db.product_catalog.name, having = query2)

	else:
		rows = db(query).select(limitby = pagination, orderby = db.product_catalog.name)

	return dict(success = True, products = rows)

def query_products_from_basket():
	"""
	This call is used to query products from shopping basket based on name or price or price range, sort it according to name or price 
	and group the products by specified price range.
	"""
	data = json.loads(request.body.read())
	pagination = (0,100) 

	if data.has_key("sort"):
		sorting_parameter = data["sort"]

	if data.has_key("min_price"):
		min_price = int(data["min_price"])

	if data.has_key("max_price"):
		max_price = int(data["max_price"])

	#Building query based on provided inputs
	if data.has_key("name"):
		product_name = data["name"]
		query = db.shopping_basket.name.contains(product_name)
		query2 = db.shopping_basket.catalog_id == db.product_catalog.id
		query3 = query & query2
		rows = db(query3).select(limitby = pagination)

	elif data.has_key("price"):
		product_price = int(data["price"])
		print product_price
		query = db.product_catalog.price == product_price
		query2 = db.shopping_basket.catalog_id == db.product_catalog.id
		query3 = query & query2
		rows = db(query3).select(limitby = pagination)

	else:
		query = db.shopping_basket.catalog_id == db.product_catalog.id
		rows = db(query).select(limitby = pagination)

	#Sorting and grouping of query results			
	if sorting_parameter:
		if max_price:
			test = rows.find(lambda row: row.product_catalog.price < max_price)
			results = test.sort(lambda row: getattr(row.product_catalog,sorting_parameter))

		if min_price:
			test = rows.find(lambda row: row.product_catalog.price > min_price)
			results = test.sort(lambda row: getattr(row.product_catalog,sorting_parameter))
		
		elif min_price and max_price:
			test = rows.find(lambda row: row.product_catalog.price > min_price and row.product_catalog.price < max_price)
			results = test.sort(lambda row: row.product_catalog.price)

		else:
			results = rows.sort(lambda row: getattr(row.product_catalog,sorting_parameter))

	else:
		results = rows

	return dict(success = True, products = results)

def add_product_to_basket_by_catalog_id():
	"""
	This call checks if the product is already added in shopping basket, otherwise adds the product and returns its product ID.
	"""
	data = json.loads(request.body.read())

	#Checking for validity of inputs if following keys exist
	if not data.get("id") or not data.get("amount"):
		redirect('invalid_product.json')

	product_id = int(data["id"])
	purchase_amount = int(data["amount"])

	if not __valid_id(product_id):
		redirect('invalid_product.json')

	query = db.product_catalog.id == product_id
	product = db(query).select().first()

	query2 = db.shopping_basket.catalog_id == product_id
	basket_entry = db(query2).select().first()

	#Checking for existence of product in basket
	if basket_entry:
		if product.id == basket_entry.catalog_id:
			return dict(success = False, reason = "Product already in basket")

	#Checking for availability of Product in inventory(database)
	if product.amount > purchase_amount:
		basket_id = db.shopping_basket.insert(name = product.name, catalog_id = product_id , purchase_amount = purchase_amount)
		new_amount = product.amount - purchase_amount
		db(query).update(amount = new_amount)
		return dict(success = True, basket_id = basket_id, reason = "Product added successfully to basket")

	else:
		return dict(success = False, reason = "Product not available")