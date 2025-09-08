from PySide2 import QtWidgets, QtCore
import maya.cmds as cmds
import shiboken2

from utils import window_utils


class DockWindow(QtWidgets.QWidget):
    CONTROL_NAME = "DockableQtTool"
    TITLE = "Dockable Qt Tool"
    WIDGET_OBJECT_NAME = "DockableQtToolWidget"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName(self.WIDGET_OBJECT_NAME)

        self.create()

        self.setParentWindow()

    def create(self):
        self.createWidgets()
        self.layoutWidgets()
        self.connectWidgets()

    def createWidgets(self):
        pass

    def layoutWidgets(self):
        pass

    def connectWidgets(self):
        pass

    def setParentWindow(self):
        """
        Creates a Maya workspaceControl and inserts this widget into it.
        """
        ctrl = self.CONTROL_NAME
        title = self.TITLE

        # Create the container if needed
        if not cmds.workspaceControl(ctrl, q=True, exists=True):
            cmds.workspaceControl(ctrl, label=title, retain=False, floating=False)

        # Wrap the control container as a QWidget
        ptr = window_utils.get_maya_control_ptr(ctrl)
        container = shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)

        # Parent this widget into the container
        self.setParent(container)
        self.setWindowFlags(QtCore.Qt.Widget)

        # Ensure a clean layout, then add self
        lay = container.layout()
        if lay is None:
            lay = QtWidgets.QVBoxLayout(container)
            lay.setContentsMargins(0, 0, 0, 0)
        else:
            # remove any existing children to avoid duplicates
            while lay.count():
                item = lay.takeAt(0)
                w = item.widget()
                if w:
                    w.setParent(None)

        lay.addWidget(self)

        # Raise/restore the dock
        cmds.workspaceControl(ctrl, e=True, restore=True)