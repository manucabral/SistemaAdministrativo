from src.core import Core
from gen import get_all_products, get_all_suppliers
from random import randint


core = Core(max_stock=50, min_stock=30, max_suppliers=1, verbose=True)
core.load()
value = core.check_deposit()
core.compare_quotes()

core.generate_purchase_request()
