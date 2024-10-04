# -*- coding: utf-8 -*-
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FailuresAccessor
from Autodesk.Revit.DB import Line
from Autodesk.Revit.Creation import ItemFactoryBase
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
import math
import sys
import traceback
import nances as module
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
Currentview = doc.ActiveView
view_scale = Currentview.Scale

def move_point_along_vector(point, vector, distance):
    new_point = point + vector.Normalize() * distance
    return new_point

def get_all_grid(doc, active_view):
    collector = FilteredElementCollector(doc, active_view.Id).OfClass(Grid)
    visible_grids = [grid for grid in collector if not grid.ViewSpecific]
    return visible_grids

def get_all_geometry_of_grids(grid, DatumExtentType = DatumExtentType.ViewSpecific):

    DatumExtentType = DatumExtentType.ViewSpecific
    geometry_element = grid.GetCurvesInView(DatumExtentType,Currentview)
    first_line = geometry_element[0]
    start_point = first_line.GetEndPoint(0)
    end_point = first_line.GetEndPoint(1)
    new_line = Line.CreateBound(start_point,end_point)
    return new_line
try:
    view_direction = Currentview.ViewDirection
    if view_direction.Z == 1 and str(Currentview.ViewType) != "ThreeD":
        Ele = get_all_grid(doc, Currentview)
        t = Transaction (doc, "Hiển thị hướng của Grid")
        t.Start()
        for i in Ele:              
            try:
                location_curve = get_all_geometry_of_grids(i)               
                direction = location_curve.Direction
                start_point = location_curve.GetEndPoint(0)
                end_point = location_curve.GetEndPoint(1)
                mid_point = location_curve.Evaluate(0.7, True)
                flat_mid_point = XYZ(mid_point.X, mid_point.Y, 0)
                move_mid_point_z = XYZ(mid_point.X, mid_point.Y, mid_point.Z + 10)
                move_mid_point = move_point_along_vector(mid_point,direction, 20 * view_scale/304.8)
                flat_move_mid_point = XYZ(move_mid_point.X,move_mid_point.Y, 0)
                z_axis = Line.CreateBound(mid_point, move_mid_point_z)
                arrow = Line.CreateBound(flat_mid_point,flat_move_mid_point)
                line_center = Line.CreateBound(XYZ(start_point.X,start_point.Y,0),XYZ(end_point.X,end_point.Y,0))
                detail_line_center = doc.Create.NewDetailCurve(Currentview,line_center)
                detail_line_1 = doc.Create.NewDetailCurve(Currentview,arrow)
                location_1 = detail_line_1.Location
                arrow_1 = location_1.Rotate(z_axis, 3.5 * math.pi / 4)
                detail_line_2 = doc.Create.NewDetailCurve(Currentview,arrow)
                location_2 = detail_line_2.Location
                arrow_2 = location_2.Rotate(z_axis, -3.5 * math.pi / 4)
            except:
                pass
        t.Commit()
    else:
        module.message_box("Please use the tool in plan view.") 
except:
    pass

