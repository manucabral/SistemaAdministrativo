from src.supplier import Supplier
from src.product import Product
from random import randint

"""
    La propiedad 'category' de cada proveedor fue cambiado por 'categories'
    Se removió la propiedad 'provides' de cada proveedor
"""

philips = Supplier(name='Philips', address='unknown',
                   phone='11934853', email='philips@contact.me',
                   categories=['Technologies', 'Tech and Tools'],
                   prices={
                       'Technologies': 1000,
                       'Tech and Tools': 300
                   })

happydance = Supplier(name='Happy Dance', address='unknown',
                      phone='12312312', email='happydance@gmail.com',
                      categories=['Clothes', 'Beverages'],
                      prices={
                          'Clothes': 300,
                          'Beverages': 20
                      })

manaos = Supplier(name='Manaos', address='brasilmanito',
                  phone='12312312', email='manaos@me.com',
                  categories=['Beverages', 'Dairy'],
                  prices={
                      'Beverages': 15,
                      'Dairy': 20
                  })

sancor = Supplier(name='Sancor', address='unknown',
                  phone='12312312', email='sancor@yandex.com',
                  categories=['Dairy'],
                  prices={
                      'Dairy': 18
                  })

patagonia = Supplier(name='Patagonia', address='Yapeyú 1546',
                     phone='12312312', email='patagonia@yahoo.cum',
                     categories=['Beverages', 'Tech and Tools'],
                     prices={
                         'Beverages': 13,
                         'Tech and Tools': 250
                     })


def gen_products(supplier: Supplier, max_stock: int):
    products = []
    for category in supplier.categories:
        for i in range(max_stock):
            product = Product(name=f'{supplier.name.replace(" ","")}{i}', description='none',
                              price=randint(100, 1200), stock=randint(0, 50),
                              supplier=supplier, category=category)
            products.append(product)
    return products


def get_all_products():
    items = gen_products(philips, 1)
    items += gen_products(happydance, 1)
    items += gen_products(manaos, 1)
    items += gen_products(sancor, 1)
    items += gen_products(patagonia, 1)
    return items


def get_all_suppliers():
    suppliers = [philips, happydance, manaos, sancor, patagonia]
    return suppliers
