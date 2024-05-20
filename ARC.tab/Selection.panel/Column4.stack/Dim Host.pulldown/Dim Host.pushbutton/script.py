__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import*
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Element
from System.Collections.Generic import *
import math
from rpw import ui
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
select = uidoc.Selection
t = Transaction (doc, "Find reference of dim, spot elevation")
listid = []
t.Start()
for i in Ele:
    try:
        ref_dim = i.References
        for a in ref_dim:
            idref_dim = a.ElementId
            listid.append(idref_dim)
            Icollection = List[ElementId](listid)
            select.SetElementIds(Icollection)
    except:
        pass
t.Commit()
      