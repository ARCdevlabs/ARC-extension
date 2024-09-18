
# -*- coding: utf-8 -*-
import string
import importlib
import Autodesk.Revit
import Autodesk.Revit.DB
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
import System as system
from System.Collections.Generic import *
import traceback
import sys
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    active_view = module.Active_view(doc)


    def distance_3d(point1, point2):
        import math
        return math.sqrt(
            (point2.X - point1.X) ** 2 +
            (point2.Y - point1.Y) ** 2 +
            (point2.Z - point1.Z) ** 2)
    
    def merge_lines_into_longest(p1, p2, p3, p4):
        # Tính khoảng cách giữa các điểm
        d1 = distance_3d(p1, p2)
        d2 = distance_3d(p1, p3)
        d3 = distance_3d(p1, p4)
        d4 = distance_3d(p2, p3)
        d5 = distance_3d(p2, p4)
        d6 = distance_3d(p3, p4)
        
        # Tìm 2 điểm xa nhau nhất
        distances = {
            d1: (p1, p2),
            d2: (p1, p3),
            d3: (p1, p4),
            d4: (p2, p3),
            d5: (p2, p4),
            d6: (p3, p4)
                    }
        # Đoạn thẳng mới với 2 điểm xa nhất
        max_distance = max(distances.keys())
        point_start, point_end = distances[max_distance]
        
        return point_start, point_end

    def are_points_collinear_3d(p1, p2, p3):
        # Tọa độ của điểm p1
        ax = p1.X
        ay = p1.Y
        az = p1.Z
        # Tọa độ của điểm p2
        bx = p2.X
        by = p2.Y
        bz = p2.Z
        # Tọa độ của điểm p3
        cx = p3.X
        cy = p3.Y
        cz = p3.Z
        # Vector A từ p1 đến p2
        vector_a_x = bx - ax
        vector_a_y = by - ay
        vector_a_z = bz - az
        
        # Vector B từ p2 đến p3
        vector_b_x = cx - bx
        vector_b_y = cy - by
        vector_b_z = cz - bz

        # Tích có hướng giữa A và B
        cross_product_X = abs(round((vector_a_y * vector_b_z - vector_a_z * vector_b_y),4))
        cross_product_Y = abs(round((vector_a_z * vector_b_x - vector_a_x * vector_b_z),4))
        cross_product_Z = abs(round((vector_a_x * vector_b_y - vector_a_y * vector_b_x),4))
        if cross_product_X == 0 and cross_product_Y == 0 and cross_product_Z == 0:
            return True
        else:
            return False

    def are_lines_collinear(line1, line2):
        p1 = line1.GetEndPoint(0)
        p2 = line1.GetEndPoint(1)
        p3 = line2.GetEndPoint(0)
        p4 = line2.GetEndPoint(1)
        return are_points_collinear_3d(p1, p2, p3) and are_points_collinear_3d(p1, p2, p4)


    def all_type_of_floor():
        all_type_of_floor = FilteredElementCollector(doc).OfClass(FloorType).OfCategory(BuiltInCategory.OST_Floors)
        return all_type_of_floor

    def get_all_element_of_category_in_view (idoc, view, builtin_category):
        category_filter = DB.ElementCategoryFilter(builtin_category)
        beam_collector = DB.FilteredElementCollector(idoc, view.Id).WherePasses(category_filter)
        return beam_collector

    def create_new_area_plan (idoc, area_scheme_id, level_id):
        new_area_plan = Autodesk.Revit.DB.ViewPlan.CreateAreaPlan(idoc, area_scheme_id, level_id)
        return new_area_plan

    def create_new_area_boundary( idoc, sketchPlane, geometryCurve, areaView):
        new_area_boundary = idoc.NewAreaBoundaryLine(sketchPlane,geometryCurve, areaView)
        return new_area_boundary

    def create_area (idoc, area_view, uv_point):
        area = idoc.Create.NewArea(area_view, uv_point)
        return area

    list_floor = all_type_of_floor()

    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                Separator, Button, CheckBox)
    components = [Label('Select type of floor:'),
                    ComboBox('combobox1', [Autodesk.Revit.DB.Element.Name.GetValue(x) for x in list_floor]),
                    Label('Height offset:'),
                    TextBox('textbox1', Text="0"),
                    Separator(),
                    Button('Create Slab')]
    form = FlexForm('ARC', components)
    form.show()
    form.values
    try:
        selected_floor_type = form.values["combobox1"]
        height_offset = form.values["textbox1"]
    except: 
        # print(traceback.format_exc())
        sys.exit()
    level_of_view = active_view.GenLevel

    id_level_of_view = level_of_view.Id

    all_area_schemes = FilteredElementCollector(doc).OfClass(AreaScheme).ToElements()

    area_scheme = all_area_schemes[0] #Lấy area scheme đầu tiên

    trans_group = TransactionGroup(doc, "Create slab")
    trans_group.Start()

    from pyrevit import revit

    with revit.Transaction("Tạo area plan và đặt area separation", swallow_errors=True):

        area_plan = create_new_area_plan(doc,area_scheme.Id,id_level_of_view)   
        
        level_plane = level_of_view.GetPlaneReference()

        sketch_plane = SketchPlane.Create(doc, level_plane)

        curve_array = Autodesk.Revit.DB.CurveArray()

        list_area_separation = []
        list_area = []

        all_beam_in_view = get_all_element_of_category_in_view (doc, active_view, BuiltInCategory.OST_StructuralFraming)

        for i in all_beam_in_view:
            try:

                beam_id = i.Id

                curve = i.Location.Curve

                start_point = curve.GetEndPoint(0)

                end_point = curve.GetEndPoint(1)

                line = Autodesk.Revit.DB.Line.CreateBound(XYZ(start_point.X,start_point.Y,0),XYZ(end_point.X,end_point.Y,0))

                curve_array.Append(line)

            except:
                # print(traceback.format_exc())
                pass

        for cur in curve_array:
            area_separation = doc.Create.NewAreaBoundaryLine(sketch_plane, cur, area_plan)
            list_area_separation.append(area_separation)

    try:
        def main():
            # Bat dau vong lap lua chon
            while True:
                try:

                    def create_slab(area, floor_type, offset, level_Id):
                        try:
                            boundaries_curve = []
                            area_boundaries = area.GetBoundarySegments(SpatialElementBoundaryOptions())

                            

                            for area_boundary in area_boundaries:
                                # area_curve_loop = CurveLoop()
                                for boundary_segment in area_boundary:
                                    curve = boundary_segment.GetCurve()
                                    # area_curve_loop.Append(curve)
                                    boundaries_curve.append(curve)
                                # curve_loop_list.Add(area_curve_loop)

                            # for index, __curve_dau_tien in enumerate(boundaries_curve):
                            #     n = 0
                            #     for __curve_con_lai in boundaries_curve:
                            #         if __curve_dau_tien is not __curve_con_lai:
                            #             check_thang_hang = are_lines_collinear(__curve_dau_tien,__curve_con_lai)
                            #             if check_thang_hang:
                            #                 __p1 = __curve_dau_tien.GetEndPoint(0)
                            #                 __p2 = __curve_dau_tien.GetEndPoint(1)
                            #                 __p3 = __curve_con_lai.GetEndPoint(0)
                            #                 __p4 = __curve_con_lai.GetEndPoint(1)
                            #                 point_xa_nhat = merge_lines_into_longest(__p1, __p2, __p3, __p4)
                                            
                            #                 merge_line = Autodesk.Revit.DB.Line.CreateBound(XYZ(point_xa_nhat[0].X,
                            #                                                                     point_xa_nhat[0].Y,point_xa_nhat[0].Z),
                            #                                                                     XYZ(point_xa_nhat[1].X,
                            #                                                                     point_xa_nhat[1].Y,point_xa_nhat[1].Z))
                            #                 doc.Create.NewDetailCurve(active_view,merge_line)
                            new_boundaries_curve = []
                            pop_log =[]
                            for i in range(len(boundaries_curve) -1):
                                for j in range(i + 1, len(boundaries_curve) -1 ):
                                    print (i, j)
                                    check_thang_hang = are_lines_collinear(boundaries_curve[i],boundaries_curve[j])
                                    if check_thang_hang:
                                        print (boundaries_curve[i],boundaries_curve[j])
                                        pop_log.append(i)
                                        pop_log.append(j)
                                        __p1 = boundaries_curve[i].GetEndPoint(0)
                                        __p2 = boundaries_curve[i].GetEndPoint(1)
                                        __p3 = boundaries_curve[j].GetEndPoint(0)
                                        __p4 = boundaries_curve[j].GetEndPoint(1)
                                        point_xa_nhat = merge_lines_into_longest(__p1, __p2, __p3, __p4)
                                        
                                        merge_line = Autodesk.Revit.DB.Line.CreateBound(XYZ(point_xa_nhat[0].X,
                                                                                            point_xa_nhat[0].Y,point_xa_nhat[0].Z),
                                                                                            XYZ(point_xa_nhat[1].X,
                                                                                            point_xa_nhat[1].Y,point_xa_nhat[1].Z))
                                        new_boundaries_curve.insert(i,merge_line)
                                        j += 1
                                        boundaries_curve.pop(i)
                                        boundaries_curve.pop(j)
                                        
                                        boundaries_curve.insert(i,merge_line)

                                        # doc.Create.NewDetailCurve(active_view,merge_line)
                                    else:
                                        new_boundaries_curve.append(boundaries_curve[i])
                                        # doc.Create.NewDetailCurve(active_view,boundaries_curve[i])

                            for tung_line in boundaries_curve:
                                doc.Create.NewDetailCurve(active_view,tung_line)                          
                            # area_curve_loop = CurveLoop()
                            # for tung_line in boundaries_curve:
                            #     doc.Create.NewDetailCurve(active_view,tung_line)
                            #     area_curve_loop.Append(tung_line)
                            # curve_loop_list  = system.Collections.Generic.List[CurveLoop]()
                            # curve_loop_list.Add(area_curve_loop)
                            

                            if curve_loop_list:

                                slab = Autodesk.Revit.DB.Floor.Create(doc, curve_loop_list, floor_type, level_Id)

                                param = slab.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)

                                param_struc = slab.get_Parameter(BuiltInParameter.FLOOR_PARAM_IS_STRUCTURAL)

                                param_struc.Set(1)

                                param.Set(offset)

                            return slab
                        except:
                            import traceback
                            print(traceback.format_exc())
                            return None
                                        
                    with revit.Transaction("tạo area khi pick vào ô dầm", swallow_errors=True):
                        try:

                            return_point = module.pick_point_with_nearest_snap(uidoc)

                        except:
                            
                            return_point = False

                        if return_point != False:
                            
                            UV_point = UV(return_point.X,return_point.Y)

                            new_area = create_area(doc,area_plan, UV_point)
                            list_area.append(new_area)

                        else:

                            new_area = None


                    list_type_floors = module.all_type_of_class_and_OST(doc, FloorType, BuiltInCategory.OST_Floors)
                    for floor in list_type_floors:
                        type_name = Autodesk.Revit.DB.Element.Name.GetValue(floor)
                        if str(type_name) == str(selected_floor_type):
                            type_floor = floor
                    type_floor_id = type_floor.Id
       
                    if new_area != None:
                        try:
                            height_offset_float = float(height_offset)/304.8
                        except:
                            height_offset_float = 0
                        with revit.Transaction("Tạo sàn từ area", swallow_errors=True):

                            create_slab (new_area, type_floor_id, height_offset_float, id_level_of_view)

                    else:
                        break

                except Exception as ex:
                    # print(traceback.format_exc())
                    if "Operation canceled by user." in str(ex):
                        break
                    else:
                        break
        main()

    except:
        # print(traceback.format_exc())
        pass
    try:
        t6 = Transaction (doc, "Xóa Area Plan")
        t6.Start()
        doc.Delete(area_plan.Id)
        for tung_area in list_area:
            try:
                doc.Delete(tung_area.Id)
            except:
                pass
        for tung_area_sp in list_area_separation:
            try:
                doc.Delete(tung_area_sp.Id)
            except:
                pass
        t6.Commit()
    except:
        pass
    trans_group.Assimilate()