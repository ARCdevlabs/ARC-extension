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
import nances
#Get Document 
doc = uidoc.Document
Currentview = doc.ActiveView
Ele = nances.get_elements(uidoc,doc, 'select tags', noti = False)
ListDuplicate = []
select = uidoc.Selection
NewList = []
try:
    for i in Ele:
        if i.Category.Name != "Room Tags":
            host = i.TaggedLocalElementId
            NewList.append (host)
        else:
            host = i.TaggedLocalRoomId
            NewList.append (host)
    ListDuplicate.append([item for item, count in collections.Counter(NewList).items() if count > 1])
    ListDuplicate = [item for items in ListDuplicate for item in items]
    Icollection = List[ElementId](ListDuplicate)
    select.SetElementIds(Icollection)        
except:
    pass


