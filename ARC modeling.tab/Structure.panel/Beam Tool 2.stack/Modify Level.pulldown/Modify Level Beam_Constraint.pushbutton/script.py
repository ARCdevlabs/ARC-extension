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
import traceback
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    try:
        Ele = module.get_elements(uidoc,doc, "Select Beams", noti = False)
        def disallow_join_at_end(element, ind):
            Autodesk.Revit.DB.WallUtils.DisallowWallJoinAtEnd(element,ind)

        def pick_point_with_nearest_snap():       
            snap_settings = UI.Selection.ObjectSnapTypes.None
            prompt = "Click"
            try:

                click_point = uidoc.Selection.PickPoint(snap_settings, prompt)
                
            except:
                # print(traceback.format_exc())
                pass
            return click_point

        def distance_2_point(point , reference_point):
            distance = point.DistanceTo(reference_point)
            return distance

        def get_nearest_point(points, reference_point):
            min_distance = float('inf')
            nearest_point = None
            
            for point in points:
                distance = point.DistanceTo(reference_point)
                if distance < min_distance:
                    min_distance = distance
                    nearest_point = point
            return nearest_point

        # point = pick_point_with_nearest_snap()
        from rpw.ui.forms import TextInput
        gia_tri_dieu_chinh = TextInput('ARC: Input value to modify offset', default="0")

        t = Transaction (doc, "Modify level of beam")
        t.Start()
        for i in Ele:
            if i.Category.Name == "Structural Framing" or i.Category.Name == "構造フレーム":
                get_para_start = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)

                get_para_value_start = get_para_start.AsDouble()

                get_para_end = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION)
                get_para_value_end = get_para_end.AsDouble()

                set_para_value_start = get_para_start.Set((float(get_para_value_start) + float(gia_tri_dieu_chinh)/304.8))

                set_para_value_end = get_para_end.Set((float(get_para_value_end) + float(gia_tri_dieu_chinh)/304.8))

        t.Commit()
    except:
        pass