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
	This call lets you edit any product after checking its validation and update 
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