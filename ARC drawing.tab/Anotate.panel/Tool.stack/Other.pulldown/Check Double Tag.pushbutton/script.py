# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import*
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
import collections
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
Currentview = doc.ActiveView

def get_selected_elements():
    selection = uidoc.Selection
    selection_ids = selection.GetElementIds()
    elements = []
    for element_id in selection_ids:
        elements.append(doc.GetElement(element_id))
    return elements
Ele = get_selected_elements()
list_duplicate = []
select = uidoc.Selection
list_element = []
try:
    t = Transaction (doc, "Check double tag")
    t.Start()
    for tung_tag in Ele:
        tung_tag_host = tung_tag.GetTaggedLocalElementIds()
        for tung_doi_tuong in tung_tag_host:
                list_element.append (tung_doi_tuong)
    list_duplicate.append([item for item, count in collections.Counter(list_element).items() if count > 1])
    list_duplicate = [item for items in list_duplicate for item in items]
    Icollection = List[ElementId](list_duplicate)
    select.SetElementIds(Icollection)
    t.Commit()  
except:
    t.RollBack
    pass



