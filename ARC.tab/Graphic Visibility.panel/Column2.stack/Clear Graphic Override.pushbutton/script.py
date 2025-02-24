__doc__ = 'python for revit api'
__author__ = 'Sonkawamura'
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
from Autodesk.Revit.DB import (FilteredElementCollector, ElementId, Color, OverrideGraphicSettings,FilteredElementCollector, BuiltInCategory)
import os
import clr
import os.path as op
import sys
def override_graphics_in_view(view, list_element_id):
    override = OverrideGraphicSettings()
    for i in list_element_id:
        view.SetElementOverrides(i, override)
    return

#Get UIDocument
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
AcView= doc.ActiveView
t = Transaction(doc, "Reset template Vn03")
t.Start()
Checkviewtemplate = str(AcView.ViewTemplateId)
#Check view have ViewTemplate or not, if not => don't need to Enable Temporary view
if Checkviewtemplate != "-1":
    tem = AcView.EnableTemporaryViewPropertiesMode(AcView.Id)
#Get FillPattern by name
GetFillPattern = Autodesk.Revit.DB.FillPatternElement.GetFillPatternElementByName(doc,FillPatternTarget.Drafting,"<Solid fill>")
#Def OverrideFraming (Color)
""" Framing """
OverrideFraming = Autodesk.Revit.DB.OverrideGraphicSettings()
SetColorFrame = AcView.SetCategoryOverrides(ElementId(-2001320),OverrideFraming)
""" Floor """
OverrideFloor = Autodesk.Revit.DB.OverrideGraphicSettings()
SetColorFloor = AcView.SetCategoryOverrides(ElementId(-2000032),OverrideFloor)
""" Wall """
OverrideWall = Autodesk.Revit.DB.OverrideGraphicSettings()
SetColorWall = AcView.SetCategoryOverrides(ElementId(-2000011),OverrideWall)
""" Column """
OverrideColumn = Autodesk.Revit.DB.OverrideGraphicSettings()
SetColorColumn = AcView.SetCategoryOverrides(ElementId(-2001330),OverrideColumn)
""" Foundation """
OverrideFoundation = Autodesk.Revit.DB.OverrideGraphicSettings()
SetColorFoundation = AcView.SetCategoryOverrides(ElementId(-2001300),OverrideFoundation)

# Override in view_floorA
collector_floor = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType()
collector_floor.ToElements()
list_floorA = []
try:
    for i in collector_floor:
        list_floorA.append(i.Id)
except:
    pass
override_graphics_in_view(AcView, list_floorA)
collector_wall = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType()
collector_wall.ToElements()
list_wallA = []
list_wallA_thick = []
try:
    for i in collector_wall:
        list_wallA.append(i.Id)
except:
    pass
override_graphics_in_view(AcView, list_wallA)
t.Commit()
      