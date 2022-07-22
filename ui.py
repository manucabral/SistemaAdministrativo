from sys import argv, exit
from PyQt5 import QtCore, QtWidgets


class SubWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        parent = kwargs.get('parent', None)
        self.verbose = kwargs.get('verbose', False)
        self.title = kwargs.get('title', 'Test')
        self.width, self.height = kwargs.get('size', (200, 200))
        super(SubWindow, self).__init__(parent, QtCore.Qt.Window)
        self.init_settings()
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layouts = []
        self.table = None

    def log(self, text):
        print(f'[{self.title}] {text}')

    def init_settings(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

    def get_layout(self, index: int):
        return self.layouts[index]

    def add_layout(self, layout: QtWidgets):
        if self.verbose:
            self.log(f'Agregando nuevo layout ID:{len(self.layouts)}')
        self.layout.addLayout(layout)
        self.layouts.append(layout)

    def add_table(self, parentid: int = 0, **kwargs):
        labels = kwargs.get('labels', [])
        data = kwargs.get('data', [])
        self.table = QtWidgets.QTableWidget(len(data), len(labels))
        self.table.setHorizontalHeaderLabels(labels)
        parent = self.get_layout(parentid)
        parent.addWidget(self.table)
        """
        for i in range(len(data)):
            for j in range(len(labels)):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
        """

    def add_button(self, text: str, callback: callable, parentid: int = 0):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(callback)
        parent = self.get_layout(parentid)
        parent.addWidget(button)


class Window(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.width = kwargs.get('width', 300)
        self.height = kwargs.get('height', 300)
        self.button_width, self.button_height = kwargs.get(
            'button_size', (100, 100))
        self.appname = kwargs.get('appname', 'None')
        self.verbose = kwargs.get('verbose', False)
        self.init_settings()
        self.add_buttons()
        self.products_panel_config()

    def products_panel_config(self):
        self.products_window = SubWindow(
            parent=self, title='Panel de Productos', size=(900, 200), verbose=True)

        self.products_window.add_layout(
            QtWidgets.QVBoxLayout())
        self.products_window.add_layout(
            QtWidgets.QVBoxLayout())
        self.products_window.add_button(
            'Agregar Producto', self.add_product, 0)
        self.products_window.add_button(
            'Eliminar Producto', self.remove_product, 0)
        self.products_window.add_button('Cerrar', self.products_window.close)

        self.products_window.add_table(
            1, labels=['ID', 'Nombre', 'Precio', 'Proveedor', 'Categoría', 'Stock', 'Descripción'], data=[])

    def init_settings(self):
        self.setWindowTitle(self.appname)
        self.setFixedSize(self.width, self.height)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.layout = QtWidgets.QVBoxLayout(self)  # vertical layout
        self.layout.setAlignment(QtCore.Qt.AlignCenter)

    def add_button(self, text: str, callback: callable, parent: QtWidgets.QWidget):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(callback)
        button.setFixedSize(self.button_width, self.button_height)
        parent.addWidget(button)
        if self.verbose:
            print(f'Boton ({text}) agregado correctamente.')

    def add_buttons(self):
        self.add_button('Panel de Productos', lambda: self.open_window(
            self.products_window), self.layout)
        self.add_button('Salir', self.exit_program, self.layout)

    def add_product(self):
        if self.verbose:
            print('Agregando producto')

    def remove_product(self):
        if self.verbose:
            print('Eliminando producto')

    def open_window(self, window: SubWindow):
        if self.verbose:
            print(f'Abriendo ventana ({window.title})')
        window.show()

    def exit_program(self):
        reply = QtWidgets.QMessageBox.question(
            self, 'Cerrar programa', '¿En serio queres cerrar el programa?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(argv)
    main_window = Window(width=400, height=200,
                         appname='Parches System Administrative', button_size=(200, 50), verbose=True)
    main_window.show()
    exit(app.exec_())
