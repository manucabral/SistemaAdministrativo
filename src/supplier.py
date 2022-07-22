from .document import Document
from .product import Product
from random import randint


class Supplier:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 0)
        self.name = kwargs.get('name', 'Supplier')
        self.address = kwargs.get('address', 'Avenida Siempre Viva')
        self.phone = kwargs.get('phone', '1234567890')
        self.email = kwargs.get('email', 'test@gmail.com')
        self.categories = kwargs.get('categories', [])
        self.prices = kwargs.get('prices', {})

    def __repr__(self) -> str:
        return f'Supplier(name={self.name},categories={self.categories})'

    def on_receive_document(self, document: Document):
        name = document.name
        if name == 'Solicitud de Presupuesto':
            return self.generate_price_quote(document)
        elif name == 'Orden de Compra':
            print(self.name, 'Recibiendo Orden de Compra')
            print(document)

    def generate_price(self, category: str, range: int) -> float:
        return randint(self.prices[category] - range, self.prices[category] + range)

    def generate_price_quote(self, document: Document):
        quote = []
        products = []
        for product in document.data:
            if product.category in self.categories:
                products.append(product)
        print(f'{self.name}: Generando Presupuesto para {len(products)} productos')
        for product in products:
            product.price = self.generate_price(product.category, 10)
            quote.append(product)
        quote_document = Document(
            name='Presupuesto', description='Presupuesto para reponer productos', author=self,
            data=quote, is_copy=False)
        return quote_document
