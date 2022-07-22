
from .product import Product
from .supplier import Supplier
from .document import Document
from .directory import Directory
from copy import copy


"""
    Terminar la adjudicación de la compra.
    Archivar los documentos pendientes (Orden de Compra, Solicitud de Presupuesto)
    Cuadruplicar la Orden de Compra
"""


class Core:

    products_file = 'products'
    suppliers_file = 'suppliers'
    documents_file = 'documents'
    replacement_orders_file = 'replacement_orders'  # pedidos de reposición

    products = suppliers = documents = []
    replacement_orders = []

    temp_products = []
    quotes = []

    # Parches System Administrative

    def __init__(self, **kwargs):
        self.max_stock = kwargs.get('max_stock', 0)
        self.min_stock = kwargs.get('min_stock', 0)
        self.max_suppliers = kwargs.get('max_suppliers', 0)
        self.verbose = kwargs.get('verbose', False)
        self.dir = Directory(
            app_name='ParchesSystemAdministrative', file_extension='par')

    def add_product(self, product):
        product.id = len(self.products)
        self.products.append(product)

    def add_supplier(self, supplier):
        supplier.id = len(self.suppliers)
        self.suppliers.append(supplier)

    def add_document(self, document):
        document.id = len(self.documents)
        self.documents.append(document)

    def copy_document(self, document, quantity: int):
        documents = []
        for _ in range(quantity):
            documents.append(document)
        return documents

    def purchase(self, products: [Product]):
        if self.verbose:
            print('Creando Orden de Compra ...')
        purchase_request = Document(
            name='Orden de Compra', description='Productos que necesitan reponerse', author=self, data=products, is_copy=False)
        self.documents.append(purchase_request)
        duplicate = self.duplicate_document(purchase_request)
        self.replacement_orders.append(duplicate)
        self.suppliers_selector(purchase_request)

    def duplicate_document(self, document: Document) -> Document:
        if self.verbose:
            print(f'Duplicando documento {document.name} ...')
        duplicate_document = copy(document)
        duplicate_document.copyof = document.id
        duplicate_document.is_copy = True
        self.documents.append(duplicate_document)
        return duplicate_document

    def suppliers_selector(self, document: Document):
        if self.verbose:
            print('Seleccionando proveedores ...')
        request_products = document.data
        selected_suppliers = []
        for request_product in request_products:
            for supplier in self.suppliers:
                if request_product.category in supplier.categories and not supplier in selected_suppliers:
                    selected_suppliers.append(supplier)

        request_quote = Document(name='Solicitud de Presupuesto',
                                 author=self,
                                 description='Presupuesto para reponer productos',
                                 data=request_products, is_copy=False)
        self.documents.append(request_quote)
        self.replacement_orders.append(self.duplicate_document(request_quote))
        self.send_request_quote(selected_suppliers, request_quote)

    def send_request_quote(self, suppliers: [Supplier], document: Document):
        if self.verbose:
            print('Enviando solicitud de presupuesto para cada proveedor...')
        for supplier in suppliers:
            self.on_receive_quote(supplier.on_receive_document(document))

    def on_receive_quote(self, document: Document):
        if self.verbose:
            print(f'Recibiendo Presupuesto de {document.author.name} ...')
        for product in document.data:
            self.quotes.append(product)

    def compare_quotes(self):
        if self.verbose:
            print('Comparando presupuestos ...')
        categories = [product.category for product in self.quotes]
        categories = list(set(categories))
        selected_products = []
        for category in categories:
            selected_products.append(self.get_minor_price(category))
        self.quotes = selected_products

    def generate_purchase_request(self):
        selected_suppliers = []
        test_supplier = self.quotes[0].supplier
        purchase_request = Document(
            name='Orden de Compra', description='Productos que vamos a comprar', author=self, data=self.quotes[0], is_copy=False)
        test_supplier.on_receive_document(purchase_request)

    def get_minor_price(self, category: str) -> Product:
        minor_price = 9999
        minor_product = None
        for product in self.quotes:
            if product.category == category and product.price < minor_price:
                minor_price = product.price
                minor_product = product
        return minor_product

    def check_deposit(self) -> bool:
        products = []
        if self.verbose:
            print('Chequeando el deposito ...')
        for product in self.products:
            if product.stock <= self.min_stock:
                product.stock = self.max_stock - product.stock
                products.append(product)
        if len(products) > 0:
            self.purchase(products)
            return False
        return True

    def get_document(self, name: str, is_copy: bool) -> Document:
        for document in self.documents:
            if document.name == name and document.is_copy == is_copy:
                return document
        return None

    def load(self):
        self.products = self.dir.load_file(filename=self.products_file)
        self.suppliers = self.dir.load_file(filename=self.suppliers_file)
        self.documents = self.dir.load_file(filename=self.documents_file)
        self.replacement_orders = self.dir.load_file(
            filename=self.replacement_orders_file)

    def save(self):
        self.dir.save_file(self.products_file, self.products)
        self.dir.save_file(self.suppliers_file, self.suppliers)
        self.dir.save_file(self.documents_file, self.documents)
        self.dir.save_file(self.replacement_orders_file,
                           self.replacement_orders)
