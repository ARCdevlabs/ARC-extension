# -*- coding: utf-8 -*-
import clr
import System
import sys
from System.Collections.Generic import List
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import Autodesk.Revit.DB as DB
import nances as module
if module.AutodeskData:
    def SolidOfElementUnion(element, view):
        solid = None
        options = Options()
        options.View = view
        options.ComputeReferences = True

        geometry_element = element.get_Geometry(options)
        if geometry_element is None:
            return solid

        for geometry_object in geometry_element:
            solid2 = geometry_object if isinstance(geometry_object, Solid) else None
            try:
                if solid2 and solid2.Volume > 0:
                    if solid is None:
                        solid = solid2
                    else:
                        solid = BooleanOperationsUtils.ExecuteBooleanOperation(solid, solid2, BooleanOperationsType.Union)
            except Exception:
                pass

        return solid

    def SolidSplit(solid, element):
        solids_list = []
        
        # Lấy LocationCurve của Element (nếu có)
        location_curve = element.Location if isinstance(element.Location, LocationCurve) else None
        if location_curve is None:
            return solids_list  # Trả về danh sách rỗng nếu không có LocationCurve
        
        curve = location_curve.Curve
        end_point1 = curve.GetEndPoint(0)
        end_point2 = curve.GetEndPoint(1)
        point3 = XYZ(end_point2.X, end_point2.Y, end_point2.Z + 3.0)

        # Tạo mặt phẳng cắt từ 3 điểm
        plane = Plane.CreateByThreePoints(end_point1, end_point2, point3)

        # Cắt khối solid bằng mặt phẳng
        solid_cut = BooleanOperationsUtils.CutWithHalfSpace(solid, plane)
        
        # Tạo phần còn lại của solid sau khi cắt
        solid_remaining = BooleanOperationsUtils.ExecuteBooleanOperation(solid, solid_cut, BooleanOperationsType.Difference)
        
        # Thêm vào danh sách kết quả
        solids_list.append(solid_cut)
        solids_list.append(solid_remaining)
        
        return solids_list

    def CurveModifyZ(curve, z):
        """
        Chỉnh sửa tọa độ Z của một đường cong (Curve) thành giá trị z mới.

        Args:
            curve (Curve): Đường cong cần chỉnh sửa.
            z (float): Giá trị Z mới.

        Returns:
            Curve: Đường cong mới với tọa độ Z đã thay đổi.
        """
        end_point1 = curve.GetEndPoint(0)
        end_point2 = curve.GetEndPoint(1)
        
        new_point1 = XYZ(end_point1.X, end_point1.Y, z)
        new_point2 = XYZ(end_point2.X, end_point2.Y, z)

        return Line.CreateBound(new_point1, new_point2)

    def XYZModifyZ(xyz, z):
        """
        Tạo một điểm mới với cùng X, Y nhưng thay đổi giá trị Z.

        Args:
            xyz (XYZ): Điểm gốc cần thay đổi tọa độ Z.
            z (float): Giá trị Z mới.

        Returns:
            XYZ: Điểm mới với tọa độ Z được thay đổi.
        """
        return XYZ(xyz.X, xyz.Y, z)
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

    def modify_slope_arrow(slope_floor_goc, new_slope_floor):

        sketch_id = slope_floor_goc.SketchId
        
        sketch = doc.GetElement(sketch_id)
        
        all_sketch = sketch.GetAllElements()
        
        # para_floor_offset = module.get_builtin_parameter_by_name(slope_floor_goc, DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)

        # floor_offset = para_floor_offset.AsDouble()

        # level_id = slope_floor_goc.LevelId
        
        for line_id in all_sketch:

            line = doc.GetElement(line_id)

            line_name = line.Name

            if line_name == "Slope Arrow" or line_name == "勾配矢印":

                model_line_slope = line

                line_slope = model_line_slope.Location.Curve

                arrow_element = line

                para_specify = module.get_builtin_parameter_by_name(arrow_element, DB.BuiltInParameter.SPECIFY_SLOPE_OR_OFFSET)
                
                para_height_tail = module.get_builtin_parameter_by_name(arrow_element, DB.BuiltInParameter.SLOPE_START_HEIGHT)

                height_tail = para_height_tail.AsDouble()

                para_level_tail = module.get_builtin_parameter_by_name(arrow_element, DB.BuiltInParameter.SLOPE_ARROW_LEVEL_START)
            
                para_height_head = module.get_builtin_parameter_by_name(arrow_element, DB.BuiltInParameter.SLOPE_END_HEIGHT)

                height_head = para_height_head.AsDouble()
            
                para_level_head = module.get_builtin_parameter_by_name(arrow_element, DB.BuiltInParameter.SLOPE_ARROW_LEVEL_END)

                para_level_head.AsElementId()
                try:
                    '''Setting mũi tên dốc theo một curve có sẵn'''
                    slope_arrow_moi = get_slope_arrow (doc,new_slope_floor)

                    slope_arrow_moi.SetGeometryCurve(line_slope,True)

                    para_specify_moi = module.get_builtin_parameter_by_name(slope_arrow_moi, DB.BuiltInParameter.SPECIFY_SLOPE_OR_OFFSET)

                    para_specify_moi.Set(para_specify.AsInteger())

                    if para_specify_moi.AsInteger() == 0:

                        para_height_tail_moi = module.get_builtin_parameter_by_name(slope_arrow_moi, DB.BuiltInParameter.SLOPE_START_HEIGHT)

                        para_height_tail_moi.Set(height_tail)

                        para_level_tail_moi = module.get_builtin_parameter_by_name(slope_arrow_moi, DB.BuiltInParameter.SLOPE_ARROW_LEVEL_START)

                        para_level_tail_moi.Set(para_level_tail.AsElementId())

                        para_height_head_moi = module.get_builtin_parameter_by_name(slope_arrow_moi, DB.BuiltInParameter.SLOPE_END_HEIGHT)

                        para_height_head_moi.Set(height_head)

                        para_level_head_moi = module.get_builtin_parameter_by_name(slope_arrow_moi, DB.BuiltInParameter.SLOPE_ARROW_LEVEL_END)

                        para_level_head_moi.Set(para_level_head.AsElementId())

                    else:

                        para_height_tail_moi = module.get_builtin_parameter_by_name(slope_arrow_moi, DB.BuiltInParameter.SLOPE_START_HEIGHT)

                        para_height_tail_moi.Set(height_tail)

                        para_level_tail_moi = module.get_builtin_parameter_by_name(slope_arrow_moi, DB.BuiltInParameter.SLOPE_ARROW_LEVEL_START)

                        para_level_tail_moi.Set(para_level_tail.AsElementId())

                        para_slope_number_moi = module.get_builtin_parameter_by_name(slope_arrow_moi, DB.BuiltInParameter.ROOF_SLOPE)

                        para_slope_number = module.get_builtin_parameter_by_name(arrow_element, DB.BuiltInParameter.ROOF_SLOPE)

                        para_slope_number_moi.Set(para_slope_number.AsDouble())
                except:
                    pass
        return new_slope_floor

    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document

    active_view = uidoc.ActiveView
    selection = uidoc.Selection
    get_element = module.get_element(uidoc,doc, 'Select Slab', noti = False)
    element = get_element[0]

    is_structural = element.get_Parameter(BuiltInParameter.FLOOR_PARAM_IS_STRUCTURAL).AsInteger()
    floor = element if isinstance(element, Floor) else None
    floor_type = floor.FloorType
    level = doc.GetElement(element.LevelId)

    try:
        element_id = selection.PickObject(Selection.ObjectType.Element).ElementId
        if element_id:
            knife = doc.GetElement(element_id)
        else:
            sys.exit()
    except:
        sys.exit()
    solid = SolidOfElementUnion(element, active_view)
    split_solids = SolidSplit(solid, knife)
    new_floors = []

    from nances import revit
    trans_group = TransactionGroup(doc, "Split Slab")
    trans_group.Start()
    with revit.Transaction('Split Slab', swallow_errors=True):
        for solid in split_solids:
            if solid and solid.Volume > 0:
                for face in solid.Faces:
                    if isinstance(face, PlanarFace):
                        if face.FaceNormal.Z == 1:
                            curve_loop_list  = List[CurveLoop]()
                            
                            curve_array = CurveArray()
                            for curve_loop in face.GetEdgesAsCurveLoops():
                                element_curve_loop = CurveLoop()
                                for curve in curve_loop:
                                    element_curve_loop.Append(curve)
                                    curve_array.Append(curve)
                                curve_loop_list.Add(element_curve_loop)
                            # new_floor = doc.Create.NewFloor(curve_array, floor_type, level, True)
                            new_floor = Floor.Create(doc, curve_loop_list, floor_type.Id, level.Id)
                            if new_floor:
                                new_floors.append(new_floor)
                        elif face.FaceNormal.Z > 0:
                            curve_loop_list  = List[CurveLoop]()
                            curve_array = CurveArray()
                            face_normal = face.FaceNormal
                            origin = face.Origin
                            z = origin.Z
                            slope_angle = face_normal.AngleTo(XYZ.BasisZ)
                            slope_value = System.Math.Tan(slope_angle)
                            xyz = origin.Add(face_normal)
                            sloped_arrow = Line.CreateBound(XYZModifyZ(origin, z), XYZModifyZ(xyz, z))
                            

                            for curve_loop in face.GetEdgesAsCurveLoops():
                                element_curve_loop = CurveLoop()
                                for curve in curve_loop:
                                    element_curve_loop.Append(CurveModifyZ(curve, z))
                                    curve_array.Append(CurveModifyZ(curve, z))
                                curve_loop_list.Add(element_curve_loop)

                            # new_floor = doc.Create.NewSlab(curve_array, level, sloped_arrow, -slope_value, True)
                            new_floor = Floor.Create(doc, curve_loop_list, floor_type.Id, level.Id, True,sloped_arrow,-slope_value )

                            sua_slope = modify_slope_arrow(element,new_floor)

                            new_floor.FloorType = floor_type
                            if new_floor:
                                new_floors.append(new_floor)

        if len(new_floors) > 1:
            doc.Delete(element.Id)

        for floor in new_floors:
            try:
                floor.get_Parameter(BuiltInParameter.FLOOR_PARAM_IS_STRUCTURAL).Set(is_structural)
            except Exception:
                pass
    trans_group.Assimilate()