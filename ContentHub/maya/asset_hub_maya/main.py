from PySide2 import QtWidgets
import maya.cmds as cmds
import shiboken2
import os

from utils import dock_window
from asset_hub_maya.widgets.tree_browser.view import tree_view
from asset_hub_maya.widgets.content_browser.view import asset_display_view
from asset_hub_maya.widgets.asset_detail import asset_details


IN_MAYA = False
try:
    import maya.cmds as cmds
    import maya.OpenMayaUI as omui
    import shiboken2
    from PySide2 import QtCore, QtWidgets
    IN_MAYA = True
except Exception:
    from PySide2 import QtCore, QtWidgets
    IN_MAYA = False

from importlib import reload
reload(dock_window)
reload(tree_view)
reload(asset_display_view)
reload(asset_details)


class AssetHub(dock_window.DockWindow):
    CONTROL_NAME = "ContentHub"
    TITLE = "Content Hub"

    def __init__(self, parent=None):
        super().__init__(parent)

    def setParentWindow(self):
        if not IN_MAYA:
            self.setWindowFlags(QtCore.Qt.Window)
            self.resize(400, 300)
            self.setWindowTitle(self.TITLE)
            self.show()
            return
        return super().setParentWindow()

    def createWidgets(self):
        asset_root = r"D:\Xicheng\Projects\HarshBlue\Maya-Unreal-Tool-Dev-Course\Projects\Ellie"
        asset_root = asset_root.replace("\\", "/")
        self.asset_explorer = tree_view.AssetExplorerWidget(root_path=asset_root)
        self.asset_display_view = asset_display_view.AssetDisplayView()
        self.asset_details_view = asset_details.AssetDetailsDialog(parent=self)
        self.asset_details_view.setVisible(False)
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

    def layoutWidgets(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.splitter)
        self.splitter.addWidget(self.asset_explorer)
        self.splitter.addWidget(self.asset_display_view)
        self.splitter.addWidget(self.asset_details_view)
        self.splitter.setSizes([300, 700, 0])
        self.setLayout(layout)
    
    def connectWidgets(self):
        self.asset_explorer.tree_view.item_selected.connect(self.on_tree_item_selected)
        self.asset_display_view.itemSelectionChanged.connect(
            lambda: self.on_asset_display_selected(self.asset_display_view.selected_asset_path())
        )

    def on_tree_item_selected(self, path: str):
        self.asset_display_view.populate_assets(path)

    def on_asset_display_selected(self, asset_path: str):
        if not asset_path:
            return
        metadata_path = os.path.join(asset_path, 'metadata.json').replace("\\", "/")
        self.asset_details_view.populate_details(metadata_path)
        self.asset_details_view.setVisible(True)

        sizes = self.splitter.sizes()
        details_width = 200
        new_sizes = [sizes[0], sizes[1], details_width]
        self.splitter.setSizes(new_sizes)


def launch():
    content_hub = AssetHub()
    content_hub.show()


if __name__ == "__main__":
    launch()
