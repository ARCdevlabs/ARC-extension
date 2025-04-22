__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import*
from Autodesk.Revit.DB import IndependentTag
from Autodesk.Revit.DB.Architecture import RoomTag
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Element
from System.Collections.Generic import *
import math
from rpw import ui
from rpw.ui.forms import Alert
import collections
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
Currentview = doc.ActiveView
Curve = []
def get_selected_elements():
    selection = uidoc.Selection
    selection_ids = selection.GetElementIds()
    elements = []
    for element_id in selection_ids:
        elements.append(doc.GetElement(element_id))
    return elements
Ele = get_selected_elements()
ListDuplicate = []
select = uidoc.Selection
NewList = []
t = Transaction (doc, "Check double tag")
t.Start()
try:
    for tung_tag in Ele:
        if tung_tag.Category.Name != "Room Tags":
            # host_tung_tag = tung_tag.TaggedLocalElementId
            tung_tag_host = tung_tag.GetTaggedLocalElementIds()
            for tung_doi_tuong in tung_tag_host:
                NewList.append (tung_doi_tuong)
        else:
            host = tung_tag.TaggedLocalRoomId
            NewList.append (host)
    ListDuplicate.append([item for item, count in collections.Counter(NewList).items() if count > 1])
    ListDuplicate = [item for items in ListDuplicate for item in items]
    Icollection = List[ElementId](ListDuplicate)
    select.SetElementIds(Icollection)        
except:
    pass
t.Commit()


