# -*- coding: utf-8 -*-
db.define_table('shopping_basket',
    Field('name', 'string', unique = True),
 	Field('catalog_id', db.product_catalog, unique = True),
    Field('purchase_amount', 'bigint')
)

db.shopping_basket.id.readable = False
db.shopping_basket.catalog_id.requires = IS_IN_DB(db,'product_catalog.id','%(name)s')


# from gluon.contrib.populate import populate
# populate(db.product_catalog,100)
# db.commit()