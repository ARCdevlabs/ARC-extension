# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FailuresAccessor
from Autodesk.Revit.DB import Line
from Autodesk.Revit.Creation import ItemFactoryBase
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
import math
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
import sys
import string
import importlib
import traceback
# print(traceback.format_exc())
try:
    ARC = string.ascii_lowercase
    begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
    module = importlib.import_module(str(begin))
    import Autodesk
    from Autodesk.Revit.DB import *
    from System.Collections.Generic import *
    if module.AutodeskData():
        Currentview = doc.ActiveView
        view_scale = Currentview.Scale
except:
    sys.exit()

def move_point_along_vector(point, vector, distance):
    new_point = point + vector.Normalize() * distance
    return new_point

try:
    Ele = module.get_selected_elements(uidoc,doc)
    t = Transaction (doc, "Hiển thị hướng của dầm")
    t.Start()
    for i in Ele:
        try:
            location_curve = i.Location.Curve
            direction = location_curve.Direction
            start_point = location_curve.GetEndPoint(0)
            end_point = location_curve.GetEndPoint(1)
            mid_point = location_curve.Evaluate(0.7, True)
            flat_mid_point = XYZ(mid_point.X, mid_point.Y, 0)
            move_mid_point_z = XYZ(mid_point.X, mid_point.Y, mid_point.Z + 10)
            move_mid_point = move_point_along_vector(mid_point,direction, 5*view_scale/304.8)
            flat_move_mid_point = XYZ(move_mid_point.X,move_mid_point.Y, 0)
            z_axis = Line.CreateBound(mid_point, move_mid_point_z)
            arrow = Line.CreateBound(flat_mid_point,flat_move_mid_point)
            line_center = Line.CreateBound(XYZ(start_point.X,start_point.Y,0),XYZ(end_point.X,end_point.Y,0))
            detail_line_center = doc.Create.NewDetailCurve(Currentview,line_center)
            is_mirrored = i.Mirrored
            if is_mirrored == False:
                detail_line_1 = doc.Create.NewDetailCurve(Currentview,arrow)
                location_1 = detail_line_1.Location
                arrow_1 = location_1.Rotate(z_axis, 3.5 * math.pi / 4)
            else:
                detail_line_2 = doc.Create.NewDetailCurve(Currentview,arrow)
                location_2 = detail_line_2.Location
                arrow_2 = location_1.Rotate(z_axis, 5.5 * math.pi / 4)
        except:
            # print(traceback.format_exc())
            pass
    t.Commit()
except:
    # print(traceback.format_exc())
    pass
