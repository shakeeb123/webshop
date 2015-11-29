# -*- coding: utf-8 -*-
import json

#Internal method
def __valid_product(product_name):
	"""
	This call is used to validate the existence of product in catalog with amount because if there is amount, product is not valid for shopping
	"""
	product_name = db.product_catalog.name == product_name
	query = db(product_name).select().first()
	if query.amount > 0:
		return True
	return False

#Commonly used response
def invalid_product():
	"""
	Returns the values that the product mentioned was invalid and data needs to be provided again.
	"""
	return dict(success = False, reason = "Not a valid product.")

#API Features
def add_product():
	"""
	This call checks if the product is already added in catalog database, otherwise adds the product and returns its product ID.
	"""
	data = json.loads(request.body.read())
	product_name = data["name"]
	product_amount = int(data["amount"])
	product_price = int(data["price"])
	product = db.product_catalog.name == product_name
	query = db(product).select().first()
	if query.amount > 0:
		return dict(success = False, reason = "Product already in catalog.")
	product_id = db.product_catalog.insert(name = product_name, amount = product_amount, price = product_price)
	return dict(success = True, product_id = product_id)

def edit_product():
	"""
	This call lets you edit any product after checking its validity and lets you update price or amount or both in catalog .
	"""
	data = json.loads(request.body.read())
	product_name = data["name"]

	if not __valid_product(product_name):
		redirect('invalid_product.json')

	query = db.product_catalog.name == product_name

	if data["amount"] and data["price"]:
		db(query).update(amount = product_amount, price = product_price)
		return dict(success = True)
	
	elif data["amount"]:
		product_amount = int(data["amount"])
		db(query).update(amount = product_amount)
		return dict(success = True)
	
	elif data["price"]:
		product_price = int(data["price"])
		db(query).update(price = product_price)
		return dict(success = True)

def remove_product():
	"""
	This call is used to remove any product from catalog deleting all the information related to amount and price of the product.
	"""
	data = json.loads(request.body.read())
	product_name = data["name"]

	if not __valid_product(product_name):
		redirect('invalid_product.json')

	query = db.product_catalog.name == product_name
	db(query).delete()
	db.commit()
	return dict(success = True)

def add_product_to_basket():
	"""
	This call checks if the product is already added in shopping basket, otherwise adds the product and returns its product ID.
	"""
	data = json.loads(request.body.read())
	product_name = data["name"]
	purchase_amount = int(data["amount"])

	if not __valid_product(product_name):
		redirect('invalid_product.json')

	query = db.product_catalog.name == product_name
	product = db(query).select().first()

	query2 = db.shopping_basket.name == product_name
	basket_entry = db(query2).select().first()

	if product.amount > purchase_amount:
		product_id = db.shopping_basket.insert(name = product_name, catalog_id = product.id , purchase_amount = purchase_amount)
		new_amount = product.amount - purchase_amount
		db(query).update(amount = new_amount)
		return dict(success = True, product_id = product_id)
	elif product.name == basket_entry.name:
		return dict(success = False, reason = "Product already in basket.")
	else:
		return dict(success = False, reason = "Product not available.")	
	
def edit_product_from_basket():
	"""
	This call lets you edit any product from shopping basket after checking its validity and lets you update purchase amount in basket 
	"""
	data = json.loads(request.body.read())
	product_name = data["name"]
	purchase_amount = int(data["amount"])

	if not __valid_product(product_name):
		redirect('invalid_product.json')

	query = db.shopping_basket.name == product_name
	basket_entry = db(query).select().first()

	query2 = db.product_catalog.name == product_name
	product = db(query2).select().first()

	if not basket_entry:
		return dict(success = False, reason = "Product not in basket.")

	db(query).update(amount = purchase_amount)
	new_amount = basket_entry.amount + product.amount - purchase_amount
	db(query2).update(amount = new_amount)
	return dict(success = True)	
		
def remove_product_from_basket():
	"""
	This call is used to remove any product from shopping basket deleting all the information related to purchase amount of the product.
	"""
	data = json.loads(request.body.read())
	product_name = data["name"]
	
	if not __valid_product(product_name):
		redirect('invalid_product.json')

	query = db.shopping_basket.name == product_name
	basket_entry = db(query).select().first()

	query2 = db.product_catalog.name == product_name
	product = db(query2).select().first()

	if not basket_entry:
		return dict(success = False, reason = "Product not in basket.")

	new_amount = basket_entry.amount + product.amount
	db(query).delete()
	db(query2).update(amount = new_amount)
	db.commit()
	return dict(success = True)
		
def query_products_from_catalog():
	"""
	This call is used to query products from catalog based on name or price or price range, sort it according to name or price and group the
	products by specified price range.
	"""
	data = json.loads(request.body.read())	
	pagination = 100
	sorting_parameter = data["sort"]

	if data["name"]:
		product_name = data["name"]
		query = db(db.product_catalog.name.contains(product_name))
	
	elif data["price"]:
		product_price = data["price"]
		query = db(db.product_catalog.price == product_price)
	
		min_price = data["min_price"]
		min_range = db.product_catalog.price > min_price 

		max_price = data["max_price"]
		max_range = db.product_catalog.price < max_price 
		
		if min_price & max_price:
			price_range = min_range & max_range
			query = db(price_range)

		elif min_price:			
			query = db(min_range)
		
		elif max_price:			
			query = db(max_range)
		
	if sorting_parameter:
		rows = query.select(
			limitby = pagination,
			orderby = getattr(db.product_catalog,sorting_parameter))
	
	elif sorting_parameter & price_range:
		rows = query.select(
			limitby = pagination,
			orderby = getattr(db.product_catalog,sorting_parameter),
			groupby = db.product_catalog.name, having = price_range)
	else:
		rows = query.select(limitby = pagination, orderby = db.product_catalog.name)
	return dict(success = True, rows = rows)

def query_products_from_basket():
	"""
	This call is used to query products from shopping basket based on name or price or price range, sort it according to name or price and group the
	products by specified price range.
	"""
	data = json.loads(request.body.read())	
	pagination = 100
	sorting_parameter = data["sort"]

	if data["name"]:
		product_name = data["name"]
		query = db(db.shopping_basket.name.contains(product_name))
	
	elif data["price"]:
		product_price = data["price"]
		query = db(db.shopping_basket.price == product_price)
	
		min_price = data["min_price"]
		min_range = db.shopping_basket.price > min_price 

		max_price = data["max_price"]
		max_range = db.shopping_basket.price < max_price 
		
		if min_price & max_price:
			price_range = min_range & max_range
			query = db(price_range)

		elif min_price:			
			query = db(min_range)
		
		elif max_price:			
			query = db(max_range)
		
	if sorting_parameter:
		rows = query.select(
			limitby = pagination,
			orderby = getattr(db.shopping_basket,sorting_parameter))
	
	elif sorting_parameter & price_range:
		rows = query.select(
			limitby = pagination,
			orderby = getattr(db.shopping_basket,sorting_parameter),
			groupby = db.shopping_basket.name, having = price_range)
	else:
		rows = query.select(limitby = pagination, orderby = db.shopping_basket.name)
	return dict(success = True, rows = rows)