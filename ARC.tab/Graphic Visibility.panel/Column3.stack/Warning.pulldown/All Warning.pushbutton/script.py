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
t = Transaction (doc, "Isolate warning")
t.Start()
warning = doc.GetWarnings()
Id = []
warningtext, warningele = [], []
if isinstance(warning, list):
    for i in warning:
        warningtext.append(i.GetDescriptionText())
        warningele.append(i.GetFailingElements())
else: 
    for i in warning:
        warningtext.append(i.GetDescriptionText())
        warningele.append(i.GetFailingElements())
for a in warningele:
    for b in a:
        Id.append(b)
ielements = List[ElementId]([x for x in Id])
Currentview.IsolateElementsTemporary(ielements)
t.Commit()

    




