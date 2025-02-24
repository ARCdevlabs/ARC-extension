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
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
Currentview = doc.ActiveView
t = Transaction (doc, "Fix warning wall overlap")
t.Start()
def get_selected_elements():
    selection = uidoc.Selection
    selection_ids = selection.GetElementIds()
    elements = []
    for element_id in selection_ids:
        elements.append(doc.GetElement(element_id))
    return elements
try:
    Ele = get_selected_elements()
    for i in Ele:
        get_parameter = i.LookupParameter("Structural").AsValueString()
        param_structural = i.get_Parameter(BuiltInParameter.WALL_STRUCTURAL_SIGNIFICANT)
        if get_parameter == "Yes":
            param_structural.Set(0)
            param_structural.Set(1)
        else:
            param_structural.Set(1)
            param_structural.Set(0)
except:
    pass
t.Commit()

    


