# -*- coding: utf-8 -*-
db.define_table('product_catalog',
    Field('name', 'string', unique=True),
    Field('amount', 'bigint'),
    Field('price','double')
)

db.product_catalog.id.readable = False
db.product_catalog.name.requires = IS_LENGTH(256) and IS_NOT_EMPTY()
