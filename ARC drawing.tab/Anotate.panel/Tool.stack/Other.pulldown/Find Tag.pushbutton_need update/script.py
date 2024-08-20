# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import*
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Element
from System.Collections.Generic import *
from Autodesk.Revit.DB.Architecture import RoomTag
import math
from rpw import ui
from rpw.ui.forms import Alert
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
Currentview = doc.ActiveView
t = Transaction (doc, "Get Tag of element in current view")
t.Start()
def get_selected_elements():
    selection = uidoc.Selection
    selection_ids = selection.GetElementIds()
    elements = []
    for element_id in selection_ids:
        elements.append(doc.GetElement(element_id))
    return elements
Ele = get_selected_elements()
ListTag = []
ListAnotation = []
select = uidoc.Selection
ListAnotationInCurrentView = []
listid = []
def all_elements_of_category(category):
	return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()
ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_WallTags))
ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_DoorTags))
ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_WindowTags))
ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_FloorTags))
ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_StructuralColumnTags))
ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_StructuralFramingTags))
ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_RoomTags))
ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_GenericModelTags))
ListAnotation = [item for items in ListAnotation for item in items]
CurrentviewId = Currentview.Id
ParentView = Currentview.GetPrimaryViewId()
for a in ListAnotation:
    WhatView = a.OwnerViewId
    if str(WhatView) == str(CurrentviewId):
        ListAnotationInCurrentView.append(a)
    elif str(WhatView) == str(ParentView):
        ListAnotationInCurrentView.append(a)
for i in Ele:
    EleId = i.Id
    for b in ListAnotationInCurrentView:
        if b.Category.Name != "Room Tags" or "部屋タグ":
            bhost = b.TaggedLocalElementId
            if b.TaggedLocalElementId == EleId:
                ListTag.append(b)
        else:
            if b.TaggedLocalRoomId == EleId:
                ListTag.append (b)
for c in ListTag:
    listid.append(c.Id)
Icollection = List[ElementId](listid)
select.SetElementIds(Icollection)
t.Commit()   


