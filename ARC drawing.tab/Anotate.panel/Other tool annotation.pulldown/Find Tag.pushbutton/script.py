# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
import nances
if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Currentview = doc.ActiveView
    Ele = nances.get_elements(uidoc,doc, 'Select Elements', noti = False)
    
    filter = ElementClassFilter(IndependentTag)
    tag_in_current_view =[]
    for tung_element in Ele:
        get_dependent_element = tung_element.GetDependentElements(filter)
        # print get_dependent_element
        for tung_tag_id in get_dependent_element:
            element_tag = doc.GetElement(tung_tag_id)
            if element_tag.OwnerViewId == Currentview.Id:
                tag_in_current_view.append(tung_tag_id)
    select = uidoc.Selection
    thong_bao = nances.message_box("Tool này chỉ hoạt động được trên view tổng thôi nhé.\nNếu đang ở view tổng rồi thì bỏ qua tin nhắn này")
    for c in tag_in_current_view:
        Icollection = List[ElementId](tag_in_current_view)
        select.SetElementIds(Icollection)