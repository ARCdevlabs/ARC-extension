# encoding: utf-8
from pyrevit import HOST_APP, UI
from Autodesk.Revit.UI import UIApplication, RevitCommandId, PostableCommand
uiapp = HOST_APP.uiapp
uiapp.PostCommand(UI.RevitCommandId.LookupCommandId("CustomCtrl_%CustomCtrl_%Add-Ins%Create and Update Type%Create and Update Type"))