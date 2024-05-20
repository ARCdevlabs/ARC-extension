S__doc__ = 'python for revit api'
__author__ = 'Sonkawamura'
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import Element
from System.Collections.Generic import *
from rpw import ui
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
def get_selected_elements():
    selection = uidoc.Selection
    selection_ids = selection.GetElementIds()
    elements = []
    for element_id in selection_ids:
        elements.append(doc.GetElement(element_id))
    return elements
Ele = get_selected_elements()
select = uidoc.Selection
wallid = []
pick = Ele
try:
    for i in Ele:  
        EleId = i.Id
        ele = doc.GetElement(EleId)
        host = ele.Host.Id
        wallid.append(host)
        Icollection = List[ElementId](wallid)
        select.SetElementIds(Icollection)
except:
    pass