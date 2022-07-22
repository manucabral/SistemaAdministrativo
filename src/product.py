class Product:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 0)
        self.name = kwargs.get('name', 'Product')
        self.description = kwargs.get('description', 'Description')
        self.price = kwargs.get('price', 0.0)
        self.supplier = kwargs.get('supplier', None)
        self.category = kwargs.get('category', None)
        self.stock = kwargs.get('stock', 0)

    def set_stock(self, stock: int):
        self.stock = stock

    def __repr__(self) -> str:
        return f'Product({self.name}, {self.price}, {self.stock}, {self.category})'

    def __eq__(self, other) -> bool:
        return self.category == other.category
