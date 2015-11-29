# -*- coding: utf-8 -*-
import json

#Internal method
def __valid_product(product_name):
	"""
	"""
	product_name = db.product_catalog.name == product_name
	query = db(product_name).select().first()
	if query.amount > 0:
		return True
	return False

#Commonly used response
def bad_product():
	"""
	Returns the values that the token was bad so it needs to be made again with the get_token function.
	"""
	return dict(success = False, reason = "Not a valid product.")

def add_product():
	"""
	"""
	data = json.loads(request.body.read())
	product_name = data["name"]
	product_amount = int(data["amount"])
	product_price = int(data["price"])

	product_id = db.product_catalog.insert(name = product_name, amount = product_amount, price = product_price)
	return dict(success = True, product_id = product_id)

def edit_product():
	"""
	"""
	data = json.loads(request.body.read())
	product_name = data["name"]
	product_amount = int(data["amount"])
	product_price = int(data["price"])

	if not __valid_product(product_name):
		redirect('bad_product.json')

	query = db.product_catalog.name == product_name
	db(query).update(amount = product_amount, price = product_price)
	return dict(success = True)

def remove_product():
	"""
	"""
	data = json.loads(request.body.read())
	product_name = data["name"]

	if not __valid_product(product_name):
		redirect('bad_product.json')

	query = db.product_catalog.name == product_name
	db(query).delete()
	db.commit()
	return dict(success = True)

def add_product_to_basket():
	"""
	"""
	data = json.loads(request.body.read())
	product_name = data["name"]
	purchase_amount = int(data["amount"])

	if not __valid_product(product_name):
		redirect('bad_product.json')

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
	"""
	data = json.loads(request.body.read())
	product_name = data["name"]
	purchase_amount = int(data["amount"])

	if not __valid_product(product_name):
		redirect('bad_product.json')

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
	"""
	data = json.loads(request.body.read())
	product_name = data["name"]
	
	if not __valid_product(product_name):
		redirect('bad_product.json')

	query = db.shopping_basket.name == product_name
	basket_entry = db(query).select().first()

	query2 = db.product_catalog.name == product_name
	product = db(query2).select().first()

	if not basket_entry:
		return dict(success = False, reason = "Product not in basket.")

	new_amount = basket_entry.amount + product.amount
	print new_amount
	db(query).delete()
	db(query2).update(amount = new_amount)
	return dict(success = True)
		

def query_products_from_catalog():
	"""
	"""
	data = json.loads(request.body.read())	
	pagination = 100
	sorting_parameter = data["sort"]

	if data["name"]:
		product_name = data["name"]
		query = db(db.product_catalog.name.contains(product_name))
	if data["price"]:
		product_price = data["price"]
		query = db(db.product_catalog.price == product_price)
	if data["min_price"]:
		min_price = data["min_price"]
		min_range = db.product_catalog.price > min_price 
		query = db(min_range)
	elif data["max_price"]:
		max_price = data["max_price"]
		max_range = db.product_catalog.price < max_price 
		query = db(max_range)
	if min_price & max_price:
		price_range = min_range & max_range
		query = db(price_range)

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
	"""
	data = json.loads(request.body.read())
	if not __valid_product(data["name"]):
		redirect('bad_product.json')	
	if data["name"]:
		product_name = data["name"]
		query = db(db.shopping_basket.name.contains(product_name))
	if data["price"]:
		product_price = data["price"]
		query = db(db.product_catalog.price == product_price)
	if data["min_price"]:
		min_price = data["min_price"]
		min_range = db.product_catalog.price > min_price
	if data["max_price"]:
		max_price = data["max_price"]
		max_range = db.product_catalog.price < max_price
	if min_price & max_price:
		price_range = min_range & max_range
	pagination = 100
	sorting_parameter = data["sort"]
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

#API Features
# def get_token():
# 	"""
# 	Take a username and password and return a token if valid.
# 	NOTE: Tokens should be used in ALL methods except this one.
# 	"""
# 	data = json.loads(request.body.read())
# 	if not data["username"] and data["password"]:
# 		return dict(success = False, reason = "No username and password provided.")
# 	username = data["username"]
# 	password = data["password"]
# 	user_details = db(db.auth_user.username == username).select().first()
# 	if not user_details:
# 		return dict(success = False, reason = "No valid username or password.")
# 	#Check the password of that user.
# 	salted_password = db.auth_user.password.validate(password)[0]
# 	if not user_details.password == salted_password:
# 		return dict(success = False, reason = "No valid username or password.")
# 	#Create a token for that user
# 	import uuid
# 	import time
# 	token = str(uuid.uuid1())
# 	db.api_token.insert(token = token, username = username)
# 	return dict(success = True, token = token)
	
# def user_details():
# 	"""
# 	Get's the auth.user.id of the user that is currently logged in with this token.
# 	"""
# 	data = json.loads(request.body.read())
# 	token = data["token"]
# 	if not __valid_token(token):
# 		redirect('bad_token.json')
# 	username = db(db.api_token.token == token).select().first().username
# 	user_id = db(db.auth_user.username == username).select().first().id
# 	return dict(user_id = user_id, success = True)

# def pending_artifacts():
# 	"""
# 	Get's the pending artifacts for a particular user based on username.
# 	"""
# 	data = json.loads(request.body.read())
# 	token = data["token"]
# 	if not __valid_token(token):
# 		redirect('bad_token.json')
# 	username = data["username"]
# 	artifact = db.artifact_revision.id > 0
# 	revised_artifact = db.artifact.id == db.artifact_revision.artifact_id
# 	artifact_type = db.artifact_type.id == db.artifact.artifact_type_id
# 	user_email = db(db.auth_user.username == username).select().first().email
# 	approver = db.review_cycle_step_definition.approver_email.contains(user_email)
# 	updated_artifacts = artifact & revised_artifact & artifact_type & approver
# 	process_artifacts = db(updated_artifacts).select()
# 	review_count = len(process_artifacts)
# 	pending = []
# 	for item in process_artifacts:
# 		pending.append({"name":item.artifact.name,
# 					"revision_number":item.artifact_revision.revision_number})
# 	return dict(pending = pending, success = True)

# def token_info():
# 	"""
# 	Show information about the token.  It can be an expired token at this point.
# 	"""
# 	data = json.loads(request.body.read())
# 	token = data["token"]
# 	if not __valid_token(token):
# 		redirect('bad_token.json')
# 	data = db(db.api_token.token == token).select().first()
# 	return dict(data = data,success = True, valid = __valid_token(token))

# def delete_token():
# 	"""
# 	Takes a token and if valid will make it invalid be deleting it.
# 	#TODO Should make as invalid not delete.
# 	"""
# 	data = json.loads(request.body.read())
# 	token = data["token"]
# 	if not __valid_token(token):
# 		redirect('bad_token.json')
# 	db(db.api_token.token == token).delete()
# 	return dict(success = True)

# def deployment_request():
# 	if deployment_target_type_name == 'PROSPER':
# 		file_transfer_scp()
# 	else:
# 		file_transfer_sftp()
# 	return
	
# def deployment_received():
# 	data = json.loads(request.body.read())
# 	token = data["token"]
# 	if not __valid_token(token):
# 		redirect('bad_token.json')
# 	deployment_id = data["deployment_id"]	
# 	user_data = db(db.api_token.token == token).select().first().username
# 	deployment_data = db(db.deployment_queue.deployment_package_id == deployment_id)
# 	deployment_check = db(db.deployment_history.deployment_package_id == deployment_id)
# 	deploy = deployment_data.select().first()
# 	deploy_check = deployment_check.select().first()
# 	if not deploy:
# 		reason = "Not a valid deployment_id: {!s}".format(deployment_id)
# 		return dict(reason = reason, success = False)
# 	else:
# 		if deploy.status == 'queued':
# 	 		activity(logged_username = user_data,
# 					message_data = 'DEPLOYMENT RECEIVED BY {!s} for deployment ID: {!s}'.format(user_data,deployment_id),db=db)
# 			db.deployment_history.insert(artifact_id = deploy_check.artifact_id,
# 										deployment_target_type_id = deploy_check.deployment_target_type_id,
# 										deployment_package_id = deployment_id,
# 										status = 'received')
# 			db.commit()
# 			deployment_data.update(status = 'done')			
# 			return dict(success = True)
# 		else:
# 			reason = "Already deployed - deployment_id: {!s}".format(deployment_id)
# 			return dict(reason = reason , success = False)

# def deployment_processed():
# 	data = json.loads(request.body.read())
# 	token = data["token"]
# 	if not __valid_token(token):
# 		redirect('bad_token.json')
# 	deployment_id = data["deployment_id"]	
# 	user_data = db(db.api_token.token == token).select().first().username
# 	deployment_data = db(db.deployment_queue.deployment_package_id == deployment_id)
# 	deployment_check = db(db.deployment_history.deployment_package_id == deployment_id)
# 	deploy = deployment_data.select().first()
# 	deploy_check = deployment_check.select().first()
# 	if not deploy:
# 		return dict(reason = "Not a valid deployment_id: {!s}".format(deployment_id), success = False)
# 	else:
# 		if deploy.status == 'done':
# 	 		activity(logged_username = user_data,
# 					message_data = 'DEPLOYMENT PROCESSED BY {!s} for deployment ID: {!s}'.format(user_data,deployment_id),db=db)
# 			db.deployment_history.insert(artifact_id = deploy_check.artifact_id,
# 										deployment_target_type_id = deploy_check.deployment_target_type_id,
# 										deployment_package_id = deployment_id,
# 										status = 'processed')
# 			db.commit()
# 	 		deployment_data.update(status = 'processed')
# 	 		return dict(success = True)
# 		else:
# 			reason = "Already processed - deployment_id: {!s}".format(deployment_id)
# 			return dict(reason = reason , success = False)

# def deployment_activated():
# 	data = json.loads(request.body.read())
# 	token = data["token"]
# 	if not __valid_token(token):
# 		redirect('bad_token.json')
# 	deployment_id = data["deployment_id"]	
# 	user_data = db(db.api_token.token == token).select().first().username
# 	deployment_data = db(db.deployment_queue.deployment_package_id == deployment_id)
# 	deployment_check = db(db.deployment_history.deployment_package_id == deployment_id)
# 	deploy = deployment_data.select().first()
# 	deploy_check = deployment_check.select().first()
# 	if not deploy:
# 		reason = "Not a valid deployment_id: {!s}".format(deployment_id)
# 		return dict(reason = reason , success = False)
# 	else:
# 		if deploy.status == 'processed':
# 	 		activity(logged_username = user_data,
# 					message_data = 'DEPLOYMENT ACTIVATED BY {!s} for deployment ID: {!s}'.format(user_data,deployment_id),db=db)
# 			db.deployment_history.insert(artifact_id = deploy_check.artifact_id,
# 										deployment_target_type_id = deploy_check.deployment_target_type_id,
# 										deployment_package_id = deployment_id,
# 										status = 'activated')
# 			db.commit()
# 	 		db(db.deployment_queue.deployment_package_id == deployment_id).delete()
# 			return dict(success = True)
# 		else:
# 			reason = "Already activated - deployment_id: {!s}".format(deployment_id)
# 			return dict(reason = reason , success = False)
