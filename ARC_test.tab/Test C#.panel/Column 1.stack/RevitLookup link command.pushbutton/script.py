# # encoding: utf-8
# from pyrevit import HOST_APP, UI
# from Autodesk.Revit.UI import UIApplication, RevitCommandId, PostableCommand
# uiapp = HOST_APP.uiapp
# uiapp.PostCommand(RevitCommandId.LookupCommandId("aadd99af-8655-461a-8b01-c00697988038"))
# encoding: utf-8
from pyrevit import HOST_APP, UI
uiapp = HOST_APP.uiapp
command_id = UI.RevitCommandId.LookupCommandId("CustomCtrl_%CustomCtrl_%CustomCtrl_%Add-Ins%Revit Lookup%RevitLookupButton%RevitLookup.Commands.SnoopSelectionCommand")
uiapp.PostCommand(command_id)
# "CustomCtrl_%CustomCtrl_%CustomCtrl_%Add-Ins%Revit Lookup%RevitLookupButton%RevitLookup.Commands.SnoopSelectionCommand:RevitLookup.Commands.SnoopSelectionCommand"