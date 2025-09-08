from __future__ import annotations

import os

try:
    from PySide2 import QtCore, QtGui, QtWidgets
except:
    from PySide6 import QtCore, QtGui, QtWidgets

from importlib import reload


class AssetTreeWidget(QtWidgets.QTreeWidget):
    """
    Lists a folder hierarchy
    """

    item_selected = QtCore.Signal(str)

    def __init__(self, root_path: str, parent=None):
        super().__init__(parent)
        self.root_path = root_path
        self.setColumnCount(1)
        self.setHeaderLabels(["Asset Hierarchy"])
        self.setUniformRowHeights(True)
        self.setIconSize(QtCore.QSize(12, 12))
        self.setAlternatingRowColors(True)
        self.selectionModel().selectionChanged.connect(lambda: self.item_selected.emit(self.selected_path() or ""))
        # Add context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuEvent)

        if self.root_path:
            self.rebuild_tree(self.root_path)

    def contextMenuEvent(self, pos: QtCore.QPoint):
        menu = QtWidgets.QMenu(self)

        add_action = menu.addAction("Add Folder")
        rename_action = menu.addAction("Rename Folder")
        refresh_action = menu.addAction("Refresh")

        action = menu.exec_(self.mapToGlobal(pos))

        if action == add_action:
            self.create_folder(self.selected_path() or "")
        elif action == rename_action:
            item = self.currentItem()
            # temporarily make editable
            if item:
                self.rename_folder(item)
        elif action == refresh_action:
            self.rebuild_tree()

    def rename_folder(self, item: QtWidgets.QTreeWidgetItem):
        """
        Handles renaming the folder in the filesystem when the user edits the item name.
        """
        old_path = item.data(0, QtCore.Qt.UserRole)
        if not old_path:
            return
        
        new_name, ok = QtWidgets.QInputDialog.getText(self,
                                                      "Rename Folder",
                                                      "New folder name:",
                                                      text=os.path.basename(old_path))
        if not ok:
            return
        
        old_name = os.path.basename(old_path)
        new_name = new_name.strip()
        if not new_name or new_name == old_name:
            return

        parent_path = os.path.dirname(old_path)
        new_path = os.path.join(parent_path, new_name)

        if os.path.exists(new_path):
            QtWidgets.QMessageBox.warning(self, "Error", f"A folder named '{new_name}' already exists.")
            item.setText(0, os.path.basename(old_path))
        else:
            try:
                os.rename(old_path, new_path)
                item.setText(0, new_name)
                item.setData(0, QtCore.Qt.UserRole, new_path)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to rename folder: {e}")
                item.setText(0, old_path)

        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

    def create_folder(self, parent_path: str):
        """
        Creates a new folder under the given parent path.
        """
        if not (parent_path and os.path.exists(parent_path) and os.path.isdir(parent_path)):
            return

        base_name = "NewFolder"
        new_folder_path = os.path.join(parent_path, base_name)
        counter = 1
        while os.path.exists(new_folder_path):
            new_folder_path = os.path.join(parent_path, f"{base_name}_{counter}")
            counter += 1

        os.makedirs(new_folder_path)
        self.rebuild_tree(parent_path)

    def rebuild_tree(self, root_path: str | None = None):
        """
        Rebuilds the tree view from the given root path.
        """
        self.clear()
        self.setHeaderLabels(['Asset Hierarchy'])

        if not root_path:
            root_path = self.root_path

        if not (root_path and os.path.exists(root_path) and os.path.isdir(root_path)):
            return

        root_name = os.path.basename(os.path.normpath(root_path)) or root_path
        root_item = QtWidgets.QTreeWidgetItem([root_name])
        root_item.setData(0, QtCore.Qt.UserRole, root_path)
        self.addTopLevelItem(root_item)

        self._add_dir_children(root_item, root_path)
        self.expandToDepth(0)

    def selected_path(self) -> str | None:
        """
        Returns the absolute path of the currently selected item
        """
        item = self.currentItem()
        return item.data(0, QtCore.Qt.UserRole) if item else None

    def _add_dir_children(self, parent_item: QtGui.QStandardItem, parent_path: str):       
        """
        Recursively adds directory children to the parent item.
        """
        if os.path.isfile(os.path.join(parent_path, 'metadata.json')):
            return

        entries = os.scandir(parent_path)
        for entry in entries:
            if not entry.is_dir():
                continue

            child_path = entry.path
            child_item = QtWidgets.QTreeWidgetItem([entry.name])
            child_item.setData(0, QtCore.Qt.UserRole, child_path)
            parent_item.addChild(child_item)

            # recurse into subdirectories
            self._add_dir_children(child_item, child_path)


class AssetExplorerWidget(QtWidgets.QWidget):
    """
    Combines a tree widget and buttons
    """

    def __init__(self, root_path: str, parent=None):
        super().__init__(parent)
        self.root_path = root_path

        self.setup_ui()

    def setup_ui(self):
        # Create Widgets
        self.tree_view = AssetTreeWidget(root_path=self.root_path)
        self.add_btn = QtWidgets.QPushButton("Export")

        # Layout
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self.add_btn)
        top_layout.addStretch()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(top_layout)
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

        # Connections
        self.add_btn.clicked.connect(self.export_selected_assets)

    def export_selected_assets(self):
        """
        Exports the selected assets in Maya to FBX files.
        """
        folder = os.path.join(self.tree_view.selected_path(), 'test')
        version = 1

        #asset_controller.export_selected_assets(folder, version)

    def populate_assets(self, root_path: str):
        """
        Populates the asset display view with assets from the given root path.
        """
        asset_paths = self.get_all_assets(root_path)
        self.asset_display_view.display_assets(asset_paths)

    def get_all_assets(self, root_path: str) -> list[str]:
        """
        Recursively collects all asset file paths under the given root path.
        """
        asset_paths = []
        for dirpath, _, filenames in os.walk(root_path):
            for filename in filenames:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Example image formats
                    asset_paths.append(os.path.join(dirpath, filename))
        return asset_paths
