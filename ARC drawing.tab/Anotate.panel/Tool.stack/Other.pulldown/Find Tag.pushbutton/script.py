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
        for tung_element in Ele:
            EleId = tung_element.Id
            
            for tung_tag in ListAnotationInCurrentView:
                # if tung_tag.Category.Name != "Room Tags" or tung_tag.Category.Name != "部屋タグ":                
                if "Room,部屋" not in tung_tag.Category.Name:
                    tung_tag_host = tung_tag.GetTaggedLocalElementIds()                  
                    if EleId in tung_tag_host:
                        ListTag.append(tung_tag)
                else:
                    if tung_tag.TaggedLocalRoomId == EleId:
                        ListTag.append (tung_tag)

        for tung_tag in ListTag:
            listid.append(tung_tag.Id)
        Icollection = List[ElementId](listid)
        select.SetElementIds(Icollection)
    except:
        import traceback
        print(traceback.format_exc())
        pass


