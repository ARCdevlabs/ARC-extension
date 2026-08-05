# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import Reference
import Autodesk.Revit.DB as DB
import math
from nances import revit
import Autodesk
from Autodesk.Revit.DB import *
import nances as module
from nances import vectortransform,geometry,allinone,selection
from System.Collections.Generic import *
import tim_reference_beam 
import traceback

if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Currentview = doc.ActiveView
    view_scale = Currentview.Scale
    Curve = []


    def get_all_grid():
        collector = FilteredElementCollector(doc).OfClass(Grid)
        grids = collector.ToElements()
        return grids
    
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
        list_new_dim = []
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

                chuan_hoa_vector_kieu_nguoc = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_tren_xuong_duoi(flat_location_line_direction,Currentview)

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
                        geo_all_grid = geometry.get_all_geometry_of_grids(grid, DatumExtentType)
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
                list_new_dim.append(dim_chia_tam)

                if dim_tong:

                    dim_tong = doc.Create.NewDimension(Currentview, line_combo_1, tung_beam_reference_dim_tong)
                    list_new_dim.append(dim_tong)

                allinone.move_text_dim (dim_chia_tam, Currentview, leader_dim = False)

            except:
                # print(traceback.format_exc())
                pass
        t.Commit()

    try:
        selection.select_sau_khi_chay_tool(list_new_dim,uidoc)
    except:
        pass


