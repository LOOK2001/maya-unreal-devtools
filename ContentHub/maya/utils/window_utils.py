from PySide2 import QtWidgets
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import shiboken2


def maya_main_window(in_maya=True):
    if not in_maya:
        return None
    return shiboken2.wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)


def get_maya_control_ptr(name):
    ptr = omui.MQtUtil.findControl(name)
    if ptr is None:
        ptr = omui.MQtUtil.findLayout(name)
    if ptr is None:
        ptr = omui.MQtUtil.findMenuItem(name)
    return ptr


def delete_workspace_control(ctrl_name):
    if cmds.workspaceControl(ctrl_name, q=True, exists=True):
        cmds.deleteUI(ctrl_name)