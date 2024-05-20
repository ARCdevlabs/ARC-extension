# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
from Autodesk.Revit.UI.Selection import ObjectType
import math
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

def disallow_join_at_end(element):
    Autodesk.Revit.DB.Structure.StructuralFramingUtils.DisallowJoinAtEnd(element, 0)
    Autodesk.Revit.DB.Structure.StructuralFramingUtils.DisallowJoinAtEnd(element, 1)
def allow_join_at_end(element):
    Autodesk.Revit.DB.Structure.StructuralFramingUtils.AllowJoinAtEnd(element, 0)
    Autodesk.Revit.DB.Structure.StructuralFramingUtils.AllowJoinAtEnd(element, 1)




uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
active_view = module.Active_view(doc)
ele = module.get_selected_elements(uidoc,doc)
if len(ele) == 0:
    import sys
    from Autodesk.Revit.UI import TaskDialog
    dialog = TaskDialog("Thông báo")
    dialog.MainContent = "Phải chọn trước các dầm cần chỉnh đô dốc, sau đó chạy tool và chọn refplane mà muốn dầm host theo (chọn refplane trên mặt cắt)"
    dialog.Show()
    sys.exit()
pick = uidoc.Selection.PickObject(ObjectType.Element)
pick_id = pick.ElementId
get_pick = doc.GetElement(pick_id)
ref_plane = get_pick.GetPlane()
XY_plane = Autodesk.Revit.DB.Plane.CreateByThreePoints(XYZ(0,0,0),XYZ(0,1,0), XYZ(1,1,0))
degree = angle_between_planes (XY_plane,ref_plane)
radian = module.degrees_to_radians(degree)
t = Transaction (doc, "Change elevation of beam")
t.Start()
for i in ele:
    # disallow_join_at_end(i)
    beam_location = i.Location.Curve

    start_point = beam_location.GetEndPoint(0)
    distance_start = module.distance_from_point_to_plane(start_point, ref_plane)
    H_projection_start = distance_start/math.cos(radian)
    # print distance_start, H_projection_start

    get_value_start = module.get_parameter_value_by_name(i, "Start z Offset Value", is_UTF8 = False)
    to_mm_start = float(get_value_start)/304.8
    set_param_start = module.set_parameter_value_by_name(i, "Start z Offset Value", H_projection_start, is_UTF8 = False)
    end_point = beam_location.GetEndPoint(1)
    distance_end = module.distance_from_point_to_plane(end_point,ref_plane)
    H_projection_end = distance_end/math.cos(radian)
    # print distance_end, H_projection_end
    get_value_end = module.get_parameter_value_by_name(i, "End z Offset Value", is_UTF8 = False)
    to_mm_end = float(get_value_end)/304.8
    set_param_end = module.set_parameter_value_by_name(i, "End z Offset Value",H_projection_end, is_UTF8 = False)
    # allow_join_at_end(i)

t.Commit()

# t_2 = Transaction (doc, "Change elevation of beam")
# t_2.Start()
# for a in ele:
#     beam_location = a.Location.Curve

#     # start_point = beam_location.GetEndPoint(0)
#     # distance_start = module.distance_from_point_to_plane(start_point, ref_plane)
#     # H_projection_start = distance_start/math.cos(radian)
#     # set_param_start = module.set_parameter_value_by_name(i, "Start Level Offset", H_projection_start, is_UTF8 = False)

#     end_point = beam_location.GetEndPoint(1)
#     distance_end = module.distance_from_point_to_plane(end_point,ref_plane)
#     H_projection_end = distance_end/math.cos(radian)
#     print H_projection_end
#     set_param_end = module.set_parameter_value_by_name(i, "End Level Offset",H_projection_end, is_UTF8 = False)
# t_2.Commit()
