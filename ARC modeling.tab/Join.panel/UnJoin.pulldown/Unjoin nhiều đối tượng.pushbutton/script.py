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
from rpw.ui.forms import Alert
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
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
listele = []
t = Transaction (doc, "Unjoin multiple")
t.Start()
try:
    pick = Ele
    dependent = []
    for i in pick:
        pickid = i.Id
        listele.append(doc.GetElement(pickid)) 
    for e in listele:
        dependent.append (JoinGeometryUtils.GetJoinedElements(doc,e))
        for a in dependent:
            for b in a:
                eleb = doc.GetElement(b)
                if JoinGeometryUtils.AreElementsJoined(doc, e, eleb):
                    JoinGeometryUtils.UnjoinGeometry(doc, e, eleb)
except:
    pass
t.Commit()