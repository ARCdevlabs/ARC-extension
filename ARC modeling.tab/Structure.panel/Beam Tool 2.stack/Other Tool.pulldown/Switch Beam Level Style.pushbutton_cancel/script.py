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
from Autodesk.Revit.UI.Selection import ObjectType
from nances import forms
import sys
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

    def pick_top_bot_beams(iuidoc, idoc):
        '''
        Tạo mặt phẳng từ 3 điểm: Start dầm chọn trước, 
        End dầm chọn trước, và cuối cùng là Start dầm chọn sau
        Có kiểm tra đang chỉnh bằng Z offset hay không
        '''

        pick_1 = iuidoc.Selection.PickObject(ObjectType.Element)
        get_pick_1 = idoc.GetElement(pick_1.ElementId)
        location_curve_1 = get_pick_1.Location.Curve
        start_point_1 = location_curve_1.GetEndPoint(0)
        end_point_1 = location_curve_1.GetEndPoint(1)
        pick_2 = uidoc.Selection.PickObject(ObjectType.Element)
        get_pick_2 = doc.GetElement(pick_2.ElementId)
        location_curve_2 = get_pick_2.Location.Curve
        start_point_2 = location_curve_2.GetEndPoint(0)

        #Check z offset beam thứ nhất
        yz_jus_1 = module.get_builtin_parameter_by_name(get_pick_1, DB.BuiltInParameter.YZ_JUSTIFICATION)
        if yz_jus_1.AsInteger() == 0:
            z_offset_1 = module.get_builtin_parameter_by_name(get_pick_1,BuiltInParameter.Z_OFFSET_VALUE).AsDouble()
            last_start_point_1 = XYZ(start_point_1.X, start_point_1.Y, start_point_1.Z+ z_offset_1)
            last_end_point_1 = XYZ(end_point_1.X, end_point_1.Y, end_point_1.Z+ z_offset_1)
        elif yz_jus_1.AsInteger() == 1:
            get_para_start = module.get_builtin_parameter_by_name(get_pick_1, DB.BuiltInParameter.START_Z_OFFSET_VALUE).AsDouble()
            get_para_end = module.get_builtin_parameter_by_name(get_pick_1, DB.BuiltInParameter.END_Z_OFFSET_VALUE).AsDouble()
            last_start_point_1 = XYZ(start_point_1.X, start_point_1.Y, start_point_1.Z+ get_para_start)
            last_end_point_1 = XYZ(end_point_1.X, end_point_1.Y, end_point_1.Z+ get_para_end)

        #Check z offset beam thứ hai
        yz_jus_2 = module.get_builtin_parameter_by_name(get_pick_2, DB.BuiltInParameter.YZ_JUSTIFICATION)
        if yz_jus_2.AsInteger() == 0:
            z_offset_2 = module.get_builtin_parameter_by_name(get_pick_2,BuiltInParameter.Z_OFFSET_VALUE).AsDouble()
            last_start_point_2 = XYZ(start_point_2.X, start_point_2.Y, start_point_2.Z+ z_offset_2)

        elif yz_jus_2.AsInteger() == 1:
            get_para_start_2 = module.get_builtin_parameter_by_name(get_pick_2, DB.BuiltInParameter.START_Z_OFFSET_VALUE).AsDouble()
            last_start_point_2 = XYZ(start_point_2.X, start_point_2.Y, start_point_2.Z+ get_para_start_2)
        
        XYZ_plane = Autodesk.Revit.DB.Plane.CreateByThreePoints(last_start_point_1,last_end_point_1, last_start_point_2)
        return XYZ_plane

    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    active_view = module.Active_view(doc)
    
    Ele = module.get_elements(uidoc,doc, "Pick Beams Need To Modify", noti = False)

    from rpw.ui.forms import SelectFromList
    value = SelectFromList('Z Offset or Start End Level Offset?', ['Z Offset','Start End Level Offset'])
    # if value == "Z Offset":
    # if value == "Start End Offset":    

    if Ele: 

        trans_group = TransactionGroup(doc, 'Switch Beam Level Style')
        trans_group.Start()
        try:
            for i in Ele:  
                t = Transaction (doc, "Start and End Offset")
                t.Start()          
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
                
                try:
                    start_z_offset = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.START_Z_OFFSET_VALUE).Set(0)
                except:
                    pass
                try:
                    end_z_offset = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.END_Z_OFFSET_VALUE).Set(0)
                except:
                    pass
                try:
                    all_z_offset = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.Z_OFFSET_VALUE).Set(0)
                except:
                    pass

                t.Commit()
            except:
                t.RollBack()  

                if value == "Z Offset":
                    t2 = Transaction (doc, "Change to YZ dependent")
                    t2.Start()
                    set_yz_dependent = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.YZ_JUSTIFICATION).Set(1)
                    t2.Commit()
                    t3 = Transaction (doc, "Change to Z offset")
                    t3.Start()
                    get_value_start = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION).AsDouble()
                    get_value_end = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION).AsDouble()
                    start_z_offset = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.START_Z_OFFSET_VALUE).Set(get_value_start)
                    end_z_offset = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.END_Z_OFFSET_VALUE).Set(get_value_end)
                    module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION).Set(0)
                    module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION).Set(0)
                    t3.Commit()
            
            trans_group.Assimilate()
        except:
            trans_group.RollBack()