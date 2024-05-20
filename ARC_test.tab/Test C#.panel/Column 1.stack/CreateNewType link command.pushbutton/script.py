# encoding: utf-8
from pyrevit import HOST_APP, UI
from Autodesk.Revit.UI import UIApplication, RevitCommandId, PostableCommand
uiapp = HOST_APP.uiapp
uiapp.PostCommand(UI.RevitCommandId.LookupCommandId("aadd99af-8655-461a-8b01-c00697988038"))