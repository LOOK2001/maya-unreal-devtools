from __future__ import annotations

import os
import json

from PySide2 import QtCore, QtGui, QtWidgets


class AssetDisplayView(QtWidgets.QListWidget):
    """
    Displays assets in an icon grid
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QtWidgets.QListWidget.IconMode)
        self.setIconSize(QtCore.QSize(64, 64))
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setUniformItemSizes(True)
        self.setSpacing(10)
        self.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)

    def selected_asset_path(self) -> str | None:
        """
        Returns the absolute path of the currently selected asset
        """
        item = self.currentItem()
        return item.data(QtCore.Qt.UserRole) if item else None
    
    def populate_assets(self, root_path: str):
        """
        Populates the view with assets from the given root path
        """
        self.clear()
        
        if not (root_path and os.path.exists(root_path) and os.path.isdir(root_path)):
            return
        
        metas = self._find_all_metadata(root_path)
        
        for meta in metas:
            with open(meta, 'r') as f:
                data = f.read()
            try:
                metadata = json.loads(data)
            except Exception as e:
                print(f"Failed to parse metadata {meta}: {e}")
                continue

            asset_name = metadata.get("name")
            latest = metadata.get("latest", "")
            versions = metadata.get("versions", [])
            latest = metadata.get('latest', '')

            latest_version = {}
            for v in versions:
                if v.get('version', '') == latest:
                    latest_version = v
            thumbnail_path = latest_version.get('thumbnail', '')
            thumbnail_path = os.path.join(os.path.dirname(meta), thumbnail_path).replace("\\", "/")

            item = QtWidgets.QListWidgetItem(asset_name)
            item.setData(QtCore.Qt.UserRole, os.path.dirname(meta))
            item.setText(asset_name)
            item.setIcon(QtGui.QIcon(thumbnail_path))
            
            self.addItem(item)
        
    def get_all_assets(self, root_path: str) -> list[str]:
        pass

    def _find_all_metadata(self, root: str) -> list[str]:
        """
        Finds all metadata.json files under the given root path.
        """
        metadata_files = []
        for dirpath, dirnames, filenames in os.walk(root):
            if 'metadata.json' in filenames:
                metadata_files.append(os.path.join(dirpath, 'metadata.json'))
        return metadata_files