from datetime import datetime

STATUSES = {
    0: 'Pendiente',
    1: 'Terminado',
    2: 'Anulado'
}


class Document:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 0)
        self.copyof = kwargs.get('copyof', 0)
        self.is_copy = kwargs.get('is_copy', False)
        self.name = kwargs.get('name', 'Documento')
        self.description = kwargs.get('description', 'Descripcion')
        self.author = kwargs.get('author', 'Autor')
        self.type = kwargs.get('type', 'Orden')
        self.data = kwargs.get('data', None)
        self.date = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        self.state = 0

    def __repr__(self) -> str:
        return f'Document({self.name}, {self.is_copy}, {self.description}, {self.data}, {self.date}, {STATUSES[self.state]})'
