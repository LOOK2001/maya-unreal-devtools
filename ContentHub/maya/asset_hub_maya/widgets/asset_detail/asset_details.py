from __future__ import annotations

from typing import Any

import os
import json

from PySide2 import QtCore, QtGui, QtWidgets


class AssetDetailsDialog(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Create Widgets
        self.asset_label = QtWidgets.QLabel("Asset Name:")
        self.asset_name = QtWidgets.QLabel("")
        self.thumbnail = QtWidgets.QLabel()
        self.thumbnail.setFixedSize(128, 128)
        self.thumbnail.setFrameShape(QtWidgets.QFrame.Box)
        self.version_label = QtWidgets.QLabel("Latest Version:")
        self.version = QtWidgets.QLabel("")
        self.author_label = QtWidgets.QLabel("Author:")
        self.author = QtWidgets.QLabel("")
        self.date_label = QtWidgets.QLabel("Date:")
        self.date = QtWidgets.QLabel("")

        # Layout
        layout = QtWidgets.QVBoxLayout()
        asset_layout = QtWidgets.QHBoxLayout()
        asset_layout.addWidget(self.asset_label)
        asset_layout.addWidget(self.asset_name)
        layout.addLayout(asset_layout)
        layout.addWidget(self.thumbnail, alignment=QtCore.Qt.AlignCenter)
        version_layout = QtWidgets.QHBoxLayout()
        version_layout.addWidget(self.version_label)
        version_layout.addWidget(self.version)
        layout.addLayout(version_layout)
        author_layout = QtWidgets.QHBoxLayout()
        author_layout.addWidget(self.author_label)
        author_layout.addWidget(self.author)
        layout.addLayout(author_layout)
        date_layout = QtWidgets.QHBoxLayout()
        date_layout.addWidget(self.date_label)
        date_layout.addWidget(self.date)
        layout.addLayout(date_layout)
        layout.addStretch()
        self.setLayout(layout)

        # Configuration
        self.resize(200, 400)

    def populate_details(self, metadata_path: str):
        with open(metadata_path, 'r') as f:
                data = f.read()
        try:
            metadata = json.loads(data)
        except Exception as e:
            print(f"Failed to parse metadata {metadata_path}: {e}")
            return
        
        asset_name = metadata.get("name")
        latest = metadata.get("latest", "")
        versions = metadata.get("versions", [])
        latest = metadata.get('latest', '')

        latest_version = {}
        for v in versions:
            if v.get('version', '') == latest:
                latest_version = v
        thumbnail_path = latest_version.get('thumbnail', '')
        thumbnail_path = os.path.join(os.path.dirname(metadata_path), thumbnail_path).replace("\\", "/")

        self.asset_name.setText(asset_name)
        self.version.setText(str(int(latest.lstrip('v'))))
        self.author.setText(latest_version.get('author', ''))
        self.date.setText(latest_version.get('date', ''))
        if os.path.exists(thumbnail_path):
            pixmap = QtGui.QPixmap(thumbnail_path)
            pixmap = pixmap.scaled(self.thumbnail.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.thumbnail.setPixmap(pixmap)
        else:
            self.thumbnail.setPixmap(QtGui.QPixmap())