__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import*
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Element
from System.Collections.Generic import *
from rpw.ui.forms import SelectFromList

import math
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
Currentview = doc.ActiveView
t = Transaction (doc, "List warning")
t.Start()
warning = doc.GetWarnings()
Id = []
select = uidoc.Selection
warningtext, warningele, test = [], [], []

if isinstance(warning, list):
    for i in warning:
        warningtext.append(i.GetDescriptionText())
else: 
    for i in warning:
        warningtext.append(i.GetDescriptionText())   
warningtext = list(dict.fromkeys(warningtext))
value = SelectFromList('Please select type of warning', warningtext)

if isinstance(warning, list):
    for i in warning:
        description = i.GetDescriptionText()
        test.append(description)
        if description == value:
            warningtext.append(i.GetDescriptionText())
            warningele.append(i.GetFailingElements())

else: 
    for i in warning:
        description = i.GetDescriptionText()
        test.append(description)
        if description == value:
            warningtext.append(i.GetDescriptionText())   
            warningele.append(i.GetFailingElements())

for a in warningele:
    for b in a:
        Id.append(b)
ielements = List[ElementId]([x for x in Id])
select.SetElementIds(ielements)
# Currentview.IsolateElementsTemporary(ielements)
t.Commit()

    


