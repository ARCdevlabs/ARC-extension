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
t = Transaction (doc, "Show direction of column or foundation")
t.Start()
for i in Ele:
    Location1 = i.Location
    Point_1 = Location1.Point
    Direction1 = i.FacingOrientation
    Point_2 =  Point_1 + 7* Direction1
    Point_3 =  Point_1 + 4 * Direction1
    PlanPoint_1 = XYZ(Point_1.X, Point_1.Y, 0)
    PlanPoint_2 = XYZ(Point_2.X, Point_2.Y, 0)
    PlanPoint_3 = XYZ(Point_3.X, Point_3.Y, 0)
    Zpoint = XYZ(Point_2.X, Point_2.Y, Point_2.Z + 100)
    Zaxis = Line.CreateBound(PlanPoint_2, Zpoint)
    L1 = Line.CreateBound(PlanPoint_1,PlanPoint_2)
    L2 = Line.CreateBound(PlanPoint_2, PlanPoint_3)
    Detailline1 = doc.Create.NewDetailCurve(Currentview,L1)
    Detailline2 = doc.Create.NewDetailCurve(Currentview,L2)
    Detailline3 = doc.Create.NewDetailCurve(Currentview,L2)
    Loc1 = Detailline2.Location
    Arrow1 = Loc1.Rotate(Zaxis, 1 * math.pi / 4)
    Loc2 = Detailline3.Location
    Arrow2 = Loc2.Rotate(Zaxis, 7 * math.pi / 4)
t.Commit()


