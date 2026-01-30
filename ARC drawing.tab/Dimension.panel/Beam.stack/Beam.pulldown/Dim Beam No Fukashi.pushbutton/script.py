# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import Reference
import Autodesk.Revit.DB as DB
import math
from nances import revit
import Autodesk
from Autodesk.Revit.DB import *
import nances as module
from nances import vectortransform,geometry
from System.Collections.Generic import *
import tim_reference_beam 
import traceback

if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Currentview = doc.ActiveView
    view_scale = Currentview.Scale
    Curve = []

    def get_geometry(element):
        option = Options()
        option.ComputeReferences = True
        geo_ref =  element.get_Geometry(option)
        return geo_ref


    def get_face(geometry):
        list_faces =[]
        for geometry_object in geometry:
            if hasattr(geometry_object, "Faces"):
                for face in geometry_object.Faces:
                    if str(type(face)) == "<type 'PlanarFace'>":
                        list_faces.append(face)
        return list_faces

    
    def get_all_grid():
        collector = FilteredElementCollector(doc).OfClass(Grid)
        grids = collector.ToElements()
        return grids
    
    def get_all_geometry_of_grids(grid, DatumExtentType = DatumExtentType.ViewSpecific):
        all_geometry = []
        DatumExtentType = DatumExtentType.ViewSpecific
        try:
            geometry_element = grid.GetCurvesInView(DatumExtentType,Currentview)
            all_geometry.append(geometry_element)
        except:
            pass
        return all_geometry

    def check_hide_isolate(view, element):
        view_mode = TemporaryViewMode.TemporaryHideIsolate
        boolean = view.IsElementVisibleInTemporaryViewMode(view_mode, element.Id)
        return boolean
    
    def check_hidden(element, view):
        boolean = element.IsHidden(view)
        not_boolean = not(boolean)
        return not_boolean

    Ele = module.get_elements(uidoc,doc, "Select Beams", noti = False)

    if Ele:

        try:
            with revit.Transaction("Chuẩn bị Dim", swallow_errors=True):
                list_can_not_dim = []
                for column in Ele:
                    has_modified_geo = column.HasModifiedGeometry()
                    if has_modified_geo == False:
                        list_can_not_dim.append(column)
                        list_comprehension = [item for item in Ele if item not in list_can_not_dim]
                        first_item_list_comprehension=[]
                        first_item_list_comprehension.append(list_comprehension[0])
                        cut_geometry = module.cut_geometry_all(doc, list_can_not_dim, first_item_list_comprehension)
        except:
            print(traceback.format_exc())
            pass

        t = Transaction(doc,"Dimension beam (centered)")
        t.Start()
        dim_tong = True
        for tung_beam in Ele:
            try:
                geo = (geometry.get_geometry(tung_beam))
                faces = geometry.get_face(geo)
                if len(faces) == 0:
                    faces = geometry.get_face(geo)
                center_plane = vectortransform.get_center_plane(tung_beam)
                center_plane_normal = center_plane.Normal
                center_point = center_plane.Origin
                list_distance = []
                list_outer_face = []
                call_class_tim_reference = tim_reference_beam.ClassTimReference(faces,center_plane, vectortransform)                
                result = call_class_tim_reference.tim_reference_beam()
                ref_face_min = result.ref_face_min
                ref_face_max = result.ref_face_max
                max_value = result.max_value


                '''Code copy từ code dim có fukashi'''
                location_line = tung_beam.Location.Curve

                flat_location_line = vectortransform.project_line_to_plane (location_line, Currentview) 

                flat_location_line_direction = flat_location_line.Direction

                chuan_hoa_vector_kieu_nguoc = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_duoi_len_tren(flat_location_line_direction,Currentview)

                #Thông thường parameter "Dimension Line Snap Distance" có giá trị là 5mm
                snap_dim_mm = 5 #tính bằng mm
                
                snap_dim_feet = snap_dim_mm  / 304.8  #tính bằng feet

                line_combo_2 = vectortransform.get_rotate_90_location_line(location_line,Currentview)
                
                line_combo_1 = vectortransform.move_line_theo_vector_theo_ty_le_view(chuan_hoa_vector_kieu_nguoc, line_combo_2, snap_dim_feet, Currentview)

                # line_combo_3 = vectortransform.move_line_theo_vector_theo_ty_le_view(-chuan_hoa_vector_kieu_nguoc, line_combo_2, snap_dim_feet, Currentview)


                tung_beam_reference = ReferenceArray()
                tung_beam_reference_dim_tong = ReferenceArray()


                list_tung_beam_reference =[]

                ref_beam_chinh_giua = Reference(tung_beam)

                all_grid = get_all_grid()
                for grid in all_grid:
                    list_grid_ref = []
                    get_hide_isolate = check_hide_isolate(Currentview, grid)
                    get_hidden_element = check_hidden(grid,Currentview)
                    if get_hide_isolate and get_hidden_element:
                        geo_all_grid = get_all_geometry_of_grids(grid, DatumExtentType)
                        for one_grid_curve in geo_all_grid:
                            for two_grid_curve in one_grid_curve:
                                grid_plane = vectortransform.create_plane_follow_line(two_grid_curve)
                                check_pararel_beam_with_grid = vectortransform.are_planes_parallel(center_plane_normal,grid_plane.Normal)
                                if check_pararel_beam_with_grid:
                                    distance_grid_with_beam =  abs(vectortransform.distance_between_parallel_planes(grid_plane, center_plane))
                                    if distance_grid_with_beam < max_value:
                                        ref_grid = Reference(grid)
                                        tung_beam_reference.Append(ref_grid)
                                        list_grid_ref.append(ref_grid)
                                        list_tung_beam_reference.append(ref_grid)
                    if len(list_grid_ref) > 0:
                        break

                tung_beam_reference.Append(ref_face_max)
                tung_beam_reference.Append(ref_face_min)
                tung_beam_reference_dim_tong.Append(ref_face_max)
                tung_beam_reference_dim_tong.Append(ref_face_min)

                list_tung_beam_reference.append(ref_face_max)
                list_tung_beam_reference.append(ref_face_min)

                check_grid_and_beam = []
                try:
                    for check_ref_grid in tung_beam_reference:
                        if ref_grid == check_ref_grid:
                            check_grid_and_beam.append(True)
                    if len(check_grid_and_beam) == 0:
                        tung_beam_reference.Append(ref_beam_chinh_giua)
                        list_tung_beam_reference.append(ref_beam_chinh_giua)
                except:
                    tung_beam_reference.Append(ref_beam_chinh_giua)
                    list_tung_beam_reference.append(ref_beam_chinh_giua)
                    pass

                dim_chia_tam = doc.Create.NewDimension(Currentview, line_combo_2, tung_beam_reference)

                if dim_tong:

                    dim_tong = doc.Create.NewDimension(Currentview, line_combo_1, tung_beam_reference_dim_tong)

                curve_dim_direction = dim_chia_tam.Curve.Direction
                seg_1_position = dim_chia_tam.Segments.Item[0].TextPosition 
                seg_2_position = dim_chia_tam.Segments.Item[1].TextPosition
                seg_1_value = float(dim_chia_tam.Segments.Item[0].Value * 304.8)
                seg_2_value = float(dim_chia_tam.Segments.Item[1].Value * 304.8)
                round_format_value_1 = round(seg_1_value,2)
                round_format_value_2 = round(seg_2_value,2)
                formatted_value_1 = str(round_format_value_1).rstrip('0').rstrip('.')
                formatted_value_2 = str(round_format_value_2).rstrip('0').rstrip('.')
                len_formatted_value_1 = len(formatted_value_1)
                len_formatted_value_2 = len(formatted_value_2)
                one_unit_width = 2 #Chieu rong 1 don vi text
                width_text_1 = float(len_formatted_value_1 * one_unit_width * (Currentview.Scale))
                width_text_2 = float(len_formatted_value_2 * one_unit_width * (Currentview.Scale))
                total_value = seg_1_value + seg_2_value
                ti_le_1 = seg_1_value / (total_value)
                ti_le_2 = seg_2_value / (total_value)
                width_1 = total_value
                khoang_cach_tu_dim = 1.5 * (Currentview.Scale)
                if seg_1_value < width_text_1: 
                    width_offset_text_1 = (seg_1_value/2 + khoang_cach_tu_dim + width_text_1/2 ) 
                else:
                    width_offset_text_1 = 0
                
                if seg_2_value < width_text_2: 
                    width_offset_text_2 = (seg_2_value/2 + khoang_cach_tu_dim + width_text_2/2 )
                else:
                    width_offset_text_2 = 0

                move_seg_1 = vectortransform.move_point_along_vector(seg_1_position,curve_dim_direction, - (width_offset_text_1/304.8))
                move_seg_2 = vectortransform.move_point_along_vector(seg_2_position,curve_dim_direction, (width_offset_text_2/304.8))
                dim_chia_tam.Segments.Item[0].TextPosition = move_seg_1
                dim_chia_tam.Segments.Item[1].TextPosition = move_seg_2
                leader_dim = dim_chia_tam.get_Parameter(BuiltInParameter.DIM_LEADER)
                leader_dim.Set(False) 
            except:
                # print(traceback.format_exc())
                pass
        t.Commit()




