__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FailuresAccessor
from Autodesk.Revit.DB import Line
from Autodesk.Revit.Creation import ItemFactoryBase
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
import math
import sys
import string
import importlib
import traceback
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document

ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
if module.AutodeskData():
    Currentview = doc.ActiveView
    view_scale = Currentview.Scale
    Curve = []

"""Activates selection tool that picks only Detail 2D elements."""
#pylint: disable=import-error,invalid-name,unused-argument,broad-except,missing-docstring
from pyrevit import revit, DB, UI
selection = revit.get_selection()
class MassSelectionFilter(UI.Selection.ISelectionFilter):
    # standard API override function
    def AllowElement(self, element):
        # only allow view-specific (detail) elements
        # that are not part of a group
        if element.ViewSpecific:
            if element.GroupId == element.GroupId.InvalidElementId:
                return True
        return False
    # standard API override function
    def AllowReference(self, refer, point):
        return False
try:
    msfilter = MassSelectionFilter()
    selection_list = revit.pick_rectangle(pick_filter=msfilter)

    filtered_list = []
    for el in selection_list:
        filtered_list.append(el.Id)
    selection.set_to(filtered_list)
    revit.uidoc.RefreshActiveView()
except Exception:
    pass

if len(filtered_list) != 2:
    message = module.message_box("Please select only 2 tags")
else:
    try:
        tag_1 = selection_list[0]
        tag_2 = selection_list[1]
        t = Transaction(doc,"Swap position of 2 tags")
        t.Start()
        position_1 = tag_1.TagHeadPosition
        position_2 = tag_2.TagHeadPosition
        tag_1.TagHeadPosition = position_2
        tag_2.TagHeadPosition = position_1
        t.Commit()
    except:
        pass




