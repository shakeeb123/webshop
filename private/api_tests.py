# -*- coding: utf-8 -*-
from pprint import pprint
import json
import requests
# stuff = {"username": "morgfl", "password":"customer"}
url = "http://127.0.0.1:8000/webshop"
# username = "morgfl"
# deployment_id_1 = 1
# deployment_id_2 = 2
# deployment_id_3 = 3

# product = {"name": "Lenovo Tablet", "amount": "30", "price": "600"}
# print "Adding Product"
# r = requests.post("{!s}/webshop_api/add_product.json".format(url), data = json.dumps(product))
# print (r.json())

# product = {"name": "Devon Faught", "amount": "30", "price": "600"}
# print "Editing Product"
# r = requests.post("{!s}/webshop_api/edit_product.json".format(url), data = json.dumps(product))
# print (r.json())

# product = {"name": "Lenovo Tablet"}
# print "Removing Product"
# r = requests.post("{!s}/webshop_api/remove_product.json".format(url), data = json.dumps(product))
# print (r.json())

# product = {"name": "Devon Faught", "amount": "2"}
# print "Adding Product to Basket"
# r = requests.post("{!s}/webshop_api/add_product_to_basket.json".format(url), data = json.dumps(product))
# print (r.json())

# product = {"name": "Devon Faught", "amount": "10"}
# print "Editing Product from Basket"
# r = requests.post("{!s}/webshop_api/edit_product_from_basket.json".format(url), data = json.dumps(product))
# print (r.json())

# product = {"name": "Devon Faught"}
# print "Removing Product from Basket"
# r = requests.post("{!s}/webshop_api/remove_product_from_basket.json".format(url), data = json.dumps(product))
# print (r.json())

product = {"min_price": "100", "max_price": "700", "sort":"name"}
print "Query From Catalog"
r = requests.post("{!s}/webshop_api/query_products_from_catalog.json".format(url), data = json.dumps(product))
print (r.json())
# print "Getting Token:",
# r = requests.post(url + "/sds_api/get_token.json", data = json.dumps(stuff))
# print (r.json())
# token = r.json()['token']

# print "Getting user details:",
# r = requests.post(url + "/sds_api/user_details.json", data = json.dumps({"token": token}))
# print (r.json())

# print "Getting Pending artifacts:"
# r = requests.post(url + "/sds_api/pending_artifacts.json", data = json.dumps({"token": token, "username": username}))
# print (r.json())

# print "Getting Token Information:"
# r = requests.post(url + "/sds_api/token_info.json", data = json.dumps({"token": token}))
# print (r.json())

# print "Testing if Deployment Received by PROSPER:"
# r = requests.post(url + "/sds_api/deployment_received.json", data = json.dumps({"token": token, "deployment_id": deployment_id_1}))
# print (r.json())

# print "Testing if Deployment Processed by PROSPER:"
# r = requests.post(url + "/sds_api/deployment_processed.json", data = json.dumps({"token": token, "deployment_id": deployment_id_1}))
# print (r.json())

# print "Testing if Deployment Activated by PROSPER:"
# r = requests.post(url + "/sds_api/deployment_activated.json", data = json.dumps({"token": token, "deployment_id": deployment_id_1}))
# print (r.json())

# print "Removing the token:",
# r = requests.post(url + "/sds_api/delete_token.json", data = json.dumps({"token": token}))
# print (r.json())

# print "Testing for bad token:"
# r = requests.post(url + "/sds_api/delete_token.json", data = json.dumps({"token": "1234"}))
# print (r.json())

#http://127.0.0.1:8000/admin/shell/index/sds_webapp