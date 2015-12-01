# -*- coding: utf-8 -*-

import json
import requests
url = "http://127.0.0.1:8000/webshop"

product = {"name": "Lenovo Tablet", "amount": "30", "price": "600"}
print "Adding Product"
r = requests.post("{!s}/webshop_api/add_product.json".format(url), data = json.dumps(product))
print (r.json())

product = {"name": "Ok Riddles", "amount": "30", "price": "600"}
print "Editing Product"
r = requests.post("{!s}/webshop_api/edit_product.json".format(url), data = json.dumps(product))
print (r.json())

product = {"name": "Lenovo Tablet"}
print "Removing Product"
r = requests.post("{!s}/webshop_api/remove_product.json".format(url), data = json.dumps(product))
print (r.json())

product = {"name": "Ok Riddles", "amount": "2"}
print "Adding Product to Basket"
r = requests.post("{!s}/webshop_api/add_product_to_basket.json".format(url), data = json.dumps(product))
print (r.json())

product = {"name": "Ok Riddles", "amount": "10"}
print "Editing Product from Basket"
r = requests.post("{!s}/webshop_api/edit_product_from_basket.json".format(url), data = json.dumps(product))
print (r.json())

product = {"name": "Ok Riddles"}
print "Removing Product from Basket"
r = requests.post("{!s}/webshop_api/remove_product_from_basket.json".format(url), data = json.dumps(product))
print (r.json())

product = {"name" : "Char", "min_price": "10", "max_price": "700","sort":"price"}
print "Query From Catalog"
r = requests.post("{!s}/webshop_api/query_products_from_catalog.json".format(url), data = json.dumps(product))
print (r.json())

product = {"min_price" : "10", "max_price": "90", "sort":"price"}
print "Query From Basket"
r = requests.post("{!s}/webshop_api/query_products_from_basket.json".format(url), data = json.dumps(product))
print (r.json())

product = {"id": "89", "amount": "3"}
print "Adding Product to Basket by Catalog ID"
r = requests.post("{!s}/webshop_api/add_product_to_basket_by_catalog_id.json".format(url), data = json.dumps(product))
print (r.json())