__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import*
from Autodesk.Revit.DB import Location
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
t = Transaction (doc, "Auto check direction of all column")
t.Start()
def TempIsolate(view, items):
    ielements = List[ElementId]([x.Id for x in items])
    view.IsolateElementsTemporary(ielements)
def all_elements_of_category(category):
	return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()
#All Elements Of Column's Category.
Column = all_elements_of_category(BuiltInCategory.OST_StructuralColumns)
ListNotOk = []
ListOk = []
for i in Column:
    Location1 = i.Location
    Direction1 = i.FacingOrientation
    if round(Direction1.X, 3) == 0:
        if round(Direction1.Y, 3) == 1:
            ListOk.append(i)
        else:
            ListNotOk.append(i)
    else:
        ListNotOk.append(i)
TempIsolate(Currentview,ListNotOk)
t.Commit()


