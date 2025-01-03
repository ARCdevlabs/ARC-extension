# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
import traceback
if module.AutodeskData():
    try:
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        Currentview = doc.ActiveView
        Ele = module.get_elements(uidoc,doc, 'Select Elements', noti = False)
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
        for tung_tag in ListAnotation:
            WhatView = tung_tag.OwnerViewId
            if str(WhatView) == str(CurrentviewId):
                ListAnotationInCurrentView.append(tung_tag)
            elif str(WhatView) == str(ParentView):
                ListAnotationInCurrentView.append(tung_tag)
        for i in Ele:
            EleId = i.Id
            for b in ListAnotationInCurrentView:
                if b.Category.Name != "Room Tags" or b.Category.Name != "部屋タグ":
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
    except:
        pass


