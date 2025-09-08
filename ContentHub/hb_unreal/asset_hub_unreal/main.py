import unreal
import sys

from hb_unreal.lib import unreal_stylesheet
from PySide6 import QtWidgets

from shared import tree_view

from importlib import reload
reload(unreal_stylesheet)


class TestWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TestWindow")
        self.resize(400, 200)

        self.asset_tree = tree_view.AssetTreeWidget("D:/Xicheng/Projects/HarshBlue/Maya-Unreal-Tool-Dev-Course/Projects/Ellie")

        # widgets
        self.label = QtWidgets.QLabel("Hello Unreal Style!", self)
        self.button = QtWidgets.QPushButton("Click Me", self)

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.asset_tree)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # connect
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        self.label.setText("Button clicked!")


def launch():
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    # style your QApp, requires a QApplication instance
    unreal_stylesheet.setup()  # <== Just 1 line of code to make the magic happen

    w = TestWindow()
    w.show()

    unreal.parent_external_window_to_slate(w.winId())

    print(int(w.winId()))
    sys.exit(app.exec())

if __name__ == '__main__':
    launch()