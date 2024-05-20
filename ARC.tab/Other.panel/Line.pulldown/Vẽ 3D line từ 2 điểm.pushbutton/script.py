
import string
import importlib
#Get UIDocument

ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
def create_plane_from_three_points(point1, point2, point3):
    plane = Plane.CreateByThreePoints(point1, point2, point3)
    return plane
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    currentview = doc.ActiveView
    sketchloop = []
    t = Transaction (doc, "Create line from 2 point")
    t.Start()
    Ele = module.get_selected_elements(uidoc,doc)
    select = uidoc.Selection
    list_point= []
#Choose ref of floor, now is choosing Topface
    for i in Ele:
        list_point.append(i.Location.Point)
    point_1 = list_point[0]
    point_2 = list_point[1]
    Line = Autodesk.Revit.DB.Line.CreateBound(point_1,point_2)
    Offset_Line = Line.CreateOffset (1,XYZ(0.55123123123,0.123123123123155,0))
    plane = create_plane_from_three_points(point_1,point_2,Offset_Line.GetEndPoint(0))
    sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(doc,plane)
    model_line = doc.Create.NewModelCurve(Line, sketch_plane)
    t.Commit()



    