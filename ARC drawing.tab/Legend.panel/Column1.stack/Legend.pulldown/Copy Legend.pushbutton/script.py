# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
from nances import forms
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
import traceback
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
active_view = doc.ActiveView

def get_fill_regions_and_text_in_active_view(idoc, view):
    list_plan_region = []
    collector = FilteredElementCollector(idoc, view.Id)
    for i in collector:
        if str(type(i)) == "<type 'FilledRegion'>" or "<type 'TextNote'>":
            list_plan_region.append(i)
    return list_plan_region

def copy_elements_to_view(element_to_copy, sourceView, target_view):
    copied_element_id = Autodesk.Revit.DB.ElementTransformUtils.CopyElements(sourceView, element_to_copy, target_view, None, None)
    return copied_element_id

def get_all_legends(idoc):
    get_all_views = FilteredElementCollector(idoc).OfClass(View).ToElements()
    list_legends = []
    for tung_view in get_all_views:
        try:
            get_type = idoc.GetElement(tung_view.GetTypeId())
            view_family = get_type.ViewFamily
            if str(view_family) == "Legend":
                list_legends.append(tung_view.Name)
        except:
            pass
    return list_legends

def override_graphics_in_view(target_view_name, element_id, override_setting):
    all_views = FilteredElementCollector(doc).OfClass(View).ToElements()
    target_view = None
    for view in all_views:
        if view.Name == target_view_name:
            target_view = view
            break
    override = Autodesk.Revit.DB.OverrideGraphicSettings()
    override = override_setting
    target_view.SetElementOverrides(element_id, override)
    return

all_legends = get_all_legends(doc)
return_legend_view_name = \
    forms.SelectFromList.show(
        all_legends,
        title = 'Select Legend Need Paste to',
        width = 500,
        button_name = 'Select Legend',
        multiselect = False
        )

get_all_views = FilteredElementCollector(doc).OfClass(View).ToElements()
for tung_view in get_all_views:
    if str(tung_view.Name) == str(return_legend_view_name):
        return_legend_view = tung_view

fill_regions_in_active_view = get_fill_regions_and_text_in_active_view(doc, active_view)
fill_regions_id = []
try:
    t = Transaction (doc, "Copy Fill Region")
    t.Start()
    for fill_region in fill_regions_in_active_view:
        fill_regions_id.append(fill_region.Id)
        get_override = active_view.GetElementOverrides(fill_region.Id)
        list_element_id = List[ElementId](fill_regions_id)
        copied_element = copy_elements_to_view(list_element_id, active_view , return_legend_view)
        override_graphics_in_view(return_legend_view_name, copied_element[0], get_override)
        fill_regions_id.remove(fill_region.Id)     
    t.Commit()
except:
    pass
if return_legend_view:
    uidoc.ActiveView = return_legend_view