# -*- coding: utf-8 -*-
import nances
from nances import forms
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
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

select_origin_view_name = \
    forms.SelectFromList.show(
        all_legends,
        title = 'Select Origin Legend',
        width = 500,
        button_name = 'Select Origin View',
        multiselect = False
        )

if select_origin_view_name:
    return_legend_view_name = \
        forms.SelectFromList.show(
            all_legends,
            title = 'Select Legend Need Paste to',
            width = 500,
            button_name = 'Select Legend',
            multiselect = False
            )
else:
    nances.message_box("Please select source legend")
    import sys
    sys.exit()
if select_origin_view_name:
    get_all_views = FilteredElementCollector(doc).OfClass(View).ToElements()

    for tung_view in get_all_views:
        if str(tung_view.Name) == str(select_origin_view_name):
            origin_view = tung_view

    for tung_view in get_all_views:
        if str(tung_view.Name) == str(return_legend_view_name):
            return_legend_view = tung_view

    fill_regions_in_origin_view = get_fill_regions_and_text_in_active_view(doc, origin_view)
    fill_regions_id = []

    trans_group = TransactionGroup(doc, 'Copy Fill Region')
    trans_group.Start()
    try:
        try:
            t = Transaction (doc, "Copy Fill Region_step 1")
            t.Start()
            for fill_region in fill_regions_in_origin_view:
                fill_regions_id.append(fill_region.Id)
                get_override = origin_view.GetElementOverrides(fill_region.Id)
                list_element_id = List[ElementId](fill_regions_id)
                copied_element = copy_elements_to_view(list_element_id, origin_view , return_legend_view)
                override_graphics_in_view(return_legend_view_name, copied_element[0], get_override)
                fill_regions_id.remove(fill_region.Id)     
            t.Commit()
            if return_legend_view:
                uidoc.ActiveView = return_legend_view
        except:
            t.RollBack()
            pass
        try:
            get_all_views_lan_2 = FilteredElementCollector(doc).OfClass(View).ToElements()
            t2 = Transaction (doc, "Delete Legend")
            t2.Start()
            new_origin_view = origin_view.Name + "1"
            for tung_view in get_all_views_lan_2:
                if str(tung_view.Name) == str(new_origin_view):
                    doc.Delete(tung_view.Id)
            t2.Commit()
        except:
            pass
        trans_group.Assimilate()
    except:
        trans_group.RollBack