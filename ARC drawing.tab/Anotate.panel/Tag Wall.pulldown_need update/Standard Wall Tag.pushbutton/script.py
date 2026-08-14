# -*- coding: utf-8 -*-
__doc__ = 'nguyenthanhson1712@gmail.com'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *




uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
from pyrevit import revit, DB, UI


def contains_substring(main_string, substring):
    if substring in main_string:
        return True


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
list_tag_tieu_chuan = ["ZA","ZW", "ZZ", "ZS", "ZT", "S1", "ST1", "T1", "T2"]
filter_tag = []
for i in selection_list:
    category = i.Category.Name
    if category == "Wall Tags":
    # print dir (i)
        tag_text = i.TagText
        for tieu_chuan in list_tag_tieu_chuan:
            if contains_substring(tag_text, tieu_chuan):
                filter_tag.append(i.Id)

select = uidoc.Selection
Icollection = List[ElementId](filter_tag)
select.SetElementIds(Icollection)



