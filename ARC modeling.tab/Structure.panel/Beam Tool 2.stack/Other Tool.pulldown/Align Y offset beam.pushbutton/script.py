# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
import traceback
from nances import forms
import math
import sys
if module.AutodeskData():

    def check_huong_dam(dam):
        start_point = dam.Location.Curve.GetEndPoint(0)
        end_point = dam.Location.Curve.GetEndPoint(1)
        new_line = Line.CreateBound(start_point,end_point)
        vector = new_line.Direction
        if abs(vector.X) < abs(vector.Y):
            if start_point.Y < end_point.Y:
                return True            
            else:
                return False
        elif start_point.X < end_point.X:
            return True 
        else: 
            return False

    def angle_between_planes(plane1, plane2):
        import math
        normal1 = plane1.Normal
        normal2 = plane2.Normal
        dot_product = normal1.DotProduct(normal2)
        magnitude1 = normal1.GetLength()
        magnitude2 = normal2.GetLength()
        
        if magnitude1 == 0 or magnitude2 == 0:
            return None    
        cos_angle = dot_product / (magnitude1 * magnitude2)
        angle_rad = math.acos(cos_angle)
        angle_deg = math.degrees(angle_rad)
        return angle_deg

    def degrees_to_radians(degrees):
        import math
        radians = degrees * (math.pi / 180)
        return radians

    def plane_from_element(element):
        location_detail_line = element.Location.Curve
        start_point = location_detail_line.GetEndPoint(0)
        end_point = location_detail_line.GetEndPoint(1)
        XYZ_plane = Autodesk.Revit.DB.Plane.CreateByThreePoints(
                                                                XYZ(start_point.X,start_point.Y,start_point.Z - 1324.123)
                                                                ,XYZ(end_point.X,end_point.Y,end_point.Z - 1324.123),
                                                                XYZ(end_point.X,end_point.Y,2234.234)
                                                                )
        return XYZ_plane
    try:
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        active_view = module.Active_view(doc)
        try:
            pick_edge = uidoc.Selection.PickObject(ObjectType.Edge)
        except:
            module.message_box("Please pick the edge of Beam")
            sys.exit()
        if pick_edge:
            beam = doc.GetElement(pick_edge)
            if beam.Category.Name == "Structural Framing" or beam.Category.Name == "構造フレーム":
                edge = beam.GetGeometryObjectFromReference(pick_edge)
                edge_curve = edge.AsCurve()
                start_point_edge_curve = edge_curve.GetEndPoint(0)
                end_point_edge_curve = edge_curve.GetEndPoint(1)
            else:
                module.message_box("Please select edge of beam")
                sys.exit()
        if beam: 
            try:
                detail_line = module.get_element(uidoc,doc, "Pick Detail Line", noti = False)
            except:
                module.message_box("Please pick the detail line on plan view")
                sys.exit()
            detail_line_plane = plane_from_element(detail_line[0])
            if detail_line[0].Category.Name not in "Lines, 線分 ":
                module.message_box("Please pick Detail Line")
                sys.exit()
            beam_plane = plane_from_element(beam)
            location_beam = beam.Location.Curve
            start_point = location_beam.GetEndPoint(0)
            end_point = location_beam.GetEndPoint(1)
            degree = angle_between_planes (detail_line_plane,beam_plane)
            radian = module.degrees_to_radians(degree)
            start_distance = module.distance_from_point_to_plane(start_point,detail_line_plane)
            start_distance_from_edge = module.distance_from_point_to_plane(start_point_edge_curve,beam_plane)

            end_distance = module.distance_from_point_to_plane(end_point,detail_line_plane)
            end_distance_from_edge = module.distance_from_point_to_plane(end_point_edge_curve,beam_plane)

            t = Transaction (doc, "Align Beam")
            t.Start()
            try:
                yz_jus = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.YZ_JUSTIFICATION)
                yz_jus.Set(1)
                get_para_start = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.START_Y_OFFSET_VALUE)
                if get_para_start.AsDouble() != 0:
                    module.message_box("Please set start y offset = 0")
                    sys.exit()
                get_para_end = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.END_Y_OFFSET_VALUE)
                if get_para_end.AsDouble() != 0:
                    module.message_box("Please set end y offset = 0")
                    sys.exit()

                if beam.HasModifiedGeometry():
                    dieu_kien_1 = check_huong_dam(beam) and check_huong_dam(detail_line[0])
                    dieu_kien_2 = not check_huong_dam(beam) and not check_huong_dam(detail_line[0])
                    dieu_kien_3 = check_huong_dam(beam) and not check_huong_dam(detail_line[0])
                    dieu_kien_4 = not check_huong_dam(beam) and check_huong_dam(detail_line[0])
                    if dieu_kien_1 or dieu_kien_2:
                        gia_tri_start = (start_distance + start_distance_from_edge )/math.cos(radian)
                        gia_tri_end = (end_distance + end_distance_from_edge)/math.cos(radian)
                        # print ("true, trường hợp tổng 1"),  (start_distance*304.8), (start_distance_from_edge*304.8), (gia_tri_start*304.8), math.cos(radian)

                    elif dieu_kien_3 or dieu_kien_4:
                        gia_tri_start = (start_distance - start_distance_from_edge )/math.cos(radian)
                        gia_tri_end = (end_distance - end_distance_from_edge)/math.cos(radian)
                        # print ("true, trường hợp tổng 2"),  (start_distance*304.8), (start_distance_from_edge*304.8), (gia_tri_start*304.8), math.cos(radian)

                    get_para_start = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.START_Y_OFFSET_VALUE)
                    
                    if gia_tri_start > 50 or gia_tri_end > 50 :
                        module.message_box("Please try again")
                    else:
                        get_para_start.Set(gia_tri_start)

                        get_para_end = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.END_Y_OFFSET_VALUE)

                        get_para_end.Set(gia_tri_end)
                else:
                    module.message_box("Please try to cut geometry the beam with other beam")
            except:
                # print(traceback.format_exc())
                pass
            t.Commit()
    except:
        pass