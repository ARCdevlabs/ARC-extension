# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import CurveLoop, XYZ,TransactionGroup,Transaction
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
from nances import revit, forms
import traceback
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    active_view = module.Active_view(doc)

    def create_slabs_with_arrow(idoc, CurveLoop, floor_type, offset, level_Id, is_struc, slope_arrow, slope):
        slab = Autodesk.Revit.DB.Floor.Create(idoc, CurveLoop, floor_type, level_Id,is_struc, slope_arrow, slope)
        param = module.get_builtin_parameter_by_name(slab, DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)
        param.Set(offset)
        return slab

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

    def change_specify_of_floor (arrow):
        param_set = arrow.Parameters
        for param in param_set:
            try:
                if str(param.AsValueString()) == "Slope" or str(param.AsValueString()) == "勾配":
                    set_para = param.Set(0)
                    # 1 la slope, 0 la Height at tail
            except:
                pass
        return 

    def get_slope_arrow (idoc, slope_floor):
        sketch_id = slope_floor.SketchId
        sketch = idoc.GetElement(sketch_id)
        all_sketch = sketch.GetAllElements()
        for line_id in all_sketch:
            try:
                line = doc.GetElement(line_id)
                line_name = line.Name
                if line_name == "Slope Arrow" or line_name == "勾配矢印":
                    arrow_element = line
            except:
                pass
        return arrow_element

    ele = module.get_elements(uidoc,doc, "Select all floors need to make slope", noti = False)

    
    with forms.WarningBar(title="Select slope floor"):
        try:
            pick = uidoc.Selection.PickObject(ObjectType.Element)
        except:
            import sys
            sys.exit()
        covert_reference_to_element = []
        element_id = pick.ElementId
        slope_floor = doc.GetElement(element_id)
        XY_plane = Autodesk.Revit.DB.Plane.CreateByThreePoints(XYZ(0,0,0),XYZ(0,1,0), XYZ(1,1,0))
        ref_top_face = Autodesk.Revit.DB.HostObjectUtils.GetTopFaces(slope_floor)
        for top_face in ref_top_face:
            surface = slope_floor.GetGeometryObjectFromReference(top_face).GetSurface()
        angle = angle_between_planes (surface, XY_plane)
        radian = degrees_to_radians(180 - angle)
        sketch_id = slope_floor.SketchId
        sketch = doc.GetElement(sketch_id)
        all_sketch = sketch.GetAllElements()
        para_floor_offset = module.get_builtin_parameter_by_name(slope_floor, DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)
        floor_offset = para_floor_offset.AsDouble()
        # floor_offset = module.get_parameter_value_by_name(slope_floor, "Height Offset From Level", is_UTF8 = False)
        level_id = slope_floor.LevelId

        for line_id in all_sketch:
            line = doc.GetElement(line_id)
            line_name = line.Name
            if line_name == "Slope Arrow" or line_name == "勾配矢印":
                model_line_slope = line
                line_slope = model_line_slope.Location.Curve
                arrow_element = line
                # height_tail = module.get_parameter_value_by_name(arrow_element, 'Height Offset at Tail', is_UTF8 = False) #SLOPE_START_HEIGHT
                para_height_tail = module.get_builtin_parameter_by_name(arrow_element, DB.BuiltInParameter.SLOPE_START_HEIGHT)
                height_tail = para_height_tail.AsDouble()

                # height_head = module.get_parameter_value_by_name(arrow_element, 'Height Offset at Head', is_UTF8 = False) #SLOPE_END_HEIGHT
                para_height_head = module.get_builtin_parameter_by_name(arrow_element, DB.BuiltInParameter.SLOPE_END_HEIGHT)
                height_head = para_height_head.AsDouble()

        trans_group = TransactionGroup(doc, "Create slope floor")
        trans_group.Start()
        list_new_slab =[]
        with revit.Transaction("Tạo sàn dốc", swallow_errors=True):
            for i in ele:
                try:
                    floor_type = module.get_type(doc, i)
                    curve_loop_list   = List[CurveLoop]()
                    curve_loop = CurveLoop()
                    sketch_id = i.SketchId
                    sketch = doc.GetElement(sketch_id)
                    all_sketch = sketch.GetAllElements()
                    profile = sketch.Profile
                    curve_arr_array = profile
                    for curve_array in curve_arr_array:
                        for a in curve_array:
                            curve_loop.Append(a)
                    curve_loop_list.Add(curve_loop)
                    create_slab = create_slabs_with_arrow(doc, curve_loop_list, floor_type.Id, floor_offset, level_id, True, line_slope, - radian )
                    old_slope_arrow = get_slope_arrow (doc,create_slab)
                    change_specify_of_floor(old_slope_arrow)    
                    list_new_slab.append(create_slab)
                    

                    new_slope_arrow = get_slope_arrow (doc,create_slab)
                    param_head = module.get_builtin_parameter_by_name(new_slope_arrow, DB.BuiltInParameter.SLOPE_END_HEIGHT)
                    param_head.Set(height_head)

                    param_tail = module.get_builtin_parameter_by_name(new_slope_arrow, DB.BuiltInParameter.SLOPE_START_HEIGHT)
                    param_tail.Set(height_tail)
                except:
                    import traceback
                    # print(traceback.format_exc())
                    pass

    if len(list_new_slab) > 0:
        t1 = Transaction (doc, "Delete current floor")
        t1.Start()
        for tung_floor in ele:
            delete_current_element = doc.Delete(tung_floor.Id)
            # print delete_current_element
        t1.Commit()

    trans_group.Assimilate()
