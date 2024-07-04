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
from System.Collections.Generic import *
from Autodesk.Revit.UI.Selection import ObjectType
from nances import forms
import sys
import traceback
import math
if module.AutodeskData():

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

    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    active_view = module.Active_view(doc)


    Ele = module.get_elements(uidoc,doc, "Pick Beams", noti = False)

    if Ele: 
        with forms.WarningBar(title='Pick the reference plane'):
            try:
                pick = uidoc.Selection.PickObject(ObjectType.Element)
            except:
                sys.exit()

        pick_id = pick.ElementId
        get_pick = doc.GetElement(pick_id)
        if hasattr(get_pick, "GetPlane"):
            ref_plane = get_pick.GetPlane()
            XY_plane = Autodesk.Revit.DB.Plane.CreateByThreePoints(XYZ(0,0,0),XYZ(0,1,0), XYZ(1,1,0))
            degree = angle_between_planes (XY_plane,ref_plane)
            radian = module.degrees_to_radians(degree)

            t = Transaction (doc, "Change elevation of beam")
            t.Start()
            for i in Ele:
                try:
                    beam_location = i.Location.Curve
                    start_point = beam_location.GetEndPoint(0)
                    distance_start = module.distance_from_point_to_plane(start_point, ref_plane)
                    H_projection_start = distance_start/math.cos(radian)

                    get_value_start = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)

                    to_mm_start = get_value_start.AsDouble()

                    set_param_start = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION).Set(H_projection_start + to_mm_start)

                    end_point = beam_location.GetEndPoint(1)
                    distance_end = module.distance_from_point_to_plane(end_point,ref_plane)
                    H_projection_end = distance_end/math.cos(radian)

                    get_value_end = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION)
                    to_mm_end = get_value_end.AsDouble()

                    set_param_end = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION).Set(H_projection_end + to_mm_end)
                except:
                    pass
            t.Commit()
        else:
            module.message_box("Please select Reference Plane")

