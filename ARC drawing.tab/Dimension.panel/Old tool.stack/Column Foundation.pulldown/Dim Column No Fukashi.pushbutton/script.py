# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import Line
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
from pyrevit import revit
import nances
from pyrevit import revit,script
from nances import geometry
from nances import vectortransform, allinone,selection
from Autodesk.Revit.DB import *
import tim_reference_column
import traceback
import setup_position_of_dim_foundation_column_config

if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    current_view = doc.ActiveView
    view_scale = current_view.Scale
    Curve = []

    logger = script.get_logger()

    my_config = script.get_config()

    source_offset_of_dim = setup_position_of_dim_foundation_column_config.load_configs_setup_offset_dim()

    source_setting_position_of_dim = setup_position_of_dim_foundation_column_config.load_configs_setup_position_of_dim()
    option_top_left = source_setting_position_of_dim[0]
    option_top_right = source_setting_position_of_dim[1]
    option_bot_left = source_setting_position_of_dim[2]
    option_bot_right = source_setting_position_of_dim[3]

    offset_of_dim = float(source_offset_of_dim[0])

    list_new_dim = []

    Ele = nances.get_elements(uidoc,doc, "Select Foundation or Columns", noti = False)
    if Ele:
        trans_group = TransactionGroup(doc, 'Dim foundation/Column')
        trans_group.Start()
    try:
        list_can_not_dim = []
        if Ele:
            with revit.Transaction("Prepair for Dim", swallow_errors=True):
                for tung_column in Ele:
                    if hasattr(tung_column,"HasModifiedGeometry"):
                        has_modified_geo = tung_column.HasModifiedGeometry()
                        if has_modified_geo == False:
                            list_can_not_dim.append(tung_column)
                            list_comprehension = [item for item in Ele if item not in list_can_not_dim]
                            first_item_list_comprehension=[]
                            first_item_list_comprehension.append(list_comprehension[0])
                            cut_geometry = nances.cut_geometry_all(doc, list_can_not_dim, first_item_list_comprehension)
    except:
        pass
        
    if Ele:    
        for column in Ele:
            with revit.Transaction("Dim total center", swallow_errors=True):            
                if hasattr(column,"HasModifiedGeometry"):
                    has_modified_geo = column.HasModifiedGeometry()
                    if has_modified_geo:
                        try:
                            point_location = column.Location.Point

                            geo = geometry.get_geometry(column)

                            faces = geometry.get_face(geo)

                            X_vector_chua_chuan_hoa = vectortransform.get_X_vector(column)

                            Y_vector_chua_chuan_hoa = vectortransform.get_Y_vector(column)

                            X_vector = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_tren_xuong_duoi(X_vector_chua_chuan_hoa,current_view)

                            Y_vector = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_tren_xuong_duoi(Y_vector_chua_chuan_hoa,current_view)

                            Y_plane = Plane.CreateByNormalAndOrigin(X_vector, point_location)

                            X_plane = Plane.CreateByNormalAndOrigin(Y_vector, point_location)

                            try:                   
                                chieu_rong = geometry.tinh_chieu_rong_cot(column, Y_vector)

                                chieu_cao = geometry.tinh_chieu_rong_cot(column, X_vector)

                                #Quy ước line top là line song song với vector X, line right là line song song với vector Y

                                line_ngang_center = vectortransform.line_for_dim_X(column,current_view)

                                tong_hop_line_bot = vectortransform.tinh_toan_line_dim_cot_1_2_3 (line_ngang_center,Y_vector,chieu_cao/2, offset_of_dim, current_view)

                                line_bot_3 = tong_hop_line_bot[0]

                                line_bot_2 = tong_hop_line_bot[1]

                                line_bot_1 = tong_hop_line_bot[2]

                                line_doc_center = vectortransform.line_for_dim_Y(column,current_view)

                                tong_hop_line_right = vectortransform.tinh_toan_line_dim_cot_1_2_3 (line_doc_center,X_vector,chieu_rong/2,offset_of_dim, current_view)

                                line_right_3 = tong_hop_line_right[0]

                                line_right_2 = tong_hop_line_right[1]

                                line_right_1 = tong_hop_line_right[2]
                                
                                tong_hop_line_top = vectortransform.tinh_toan_line_dim_cot_1_2_3 (line_ngang_center,-Y_vector,chieu_cao/2,offset_of_dim, current_view)

                                line_top_3 = tong_hop_line_top[0]

                                line_top_2 = tong_hop_line_top[1]

                                line_top_1 = tong_hop_line_top[2]

                                tong_hop_line_left = vectortransform.tinh_toan_line_dim_cot_1_2_3 (line_doc_center,-X_vector,chieu_rong/2,offset_of_dim, current_view)

                                line_left_3 = tong_hop_line_left[0]

                                line_left_2 = tong_hop_line_left[1]

                                line_left_1 = tong_hop_line_left[2]

                                if option_top_left:
                                    line_ngang_1 = line_top_1
                                    line_ngang_2 = line_top_2
                                    line_ngang_3 = line_top_3

                                    line_doc_1 = line_left_1
                                    line_doc_2 = line_left_2
                                    line_doc_3 = line_left_3

                                elif option_top_right:
                                    line_ngang_1 = line_top_1
                                    line_ngang_2 = line_top_2
                                    line_ngang_3 = line_top_3

                                    line_doc_1 = line_right_1
                                    line_doc_2 = line_right_2
                                    line_doc_3 = line_right_3

                                elif option_bot_left:
                                    line_ngang_1 = line_bot_1
                                    line_ngang_2 = line_bot_2
                                    line_ngang_3 = line_bot_3

                                    line_doc_1 = line_left_1
                                    line_doc_2 = line_left_2
                                    line_doc_3 = line_left_3

                                elif option_bot_right:
                                    line_ngang_1 = line_bot_1
                                    line_ngang_2 = line_bot_2
                                    line_ngang_3 = line_bot_3

                                    line_doc_1 = line_right_1
                                    line_doc_2 = line_right_2
                                    line_doc_3 = line_right_3        
                        
                            except:
                                # print(traceback.format_exc())
                                pass                        

                            list_distance_Y = []

                            list_distance_X = []

                            list_outer_face_Y = []

                            list_outer_face_X = []

                            call_class_tim_reference = tim_reference_column.ClassTimReference (faces, X_vector, Y_vector, X_plane, Y_plane, vectortransform)

                            result = call_class_tim_reference.tim_reference_column()

                            ref_face_min_Y = result.ref_face_min #Không ghi gì thì hiểu là phương Y

                            ref_face_max_Y = result.ref_face_max #Không ghi gì thì hiểu là phương Y

                            ref_face_min_X = result.ref_face_min_X

                            ref_face_max_X = result.ref_face_max_X

                            max_value_Y = result.max_value_Y

                            max_value_X = result.max_value_X

                            try:
                                line_Y = vectortransform.line_for_dim_Y(column,current_view)

                                tong_hop_line_Y = vectortransform.tinh_toan_line_dim_cot_1_2_3 (line_Y,X_vector,max_value_X,offset_of_dim, current_view)

                                line_Y_2 = tong_hop_line_Y[1]

                                line_Y_1 = tong_hop_line_Y[2]

                                line_X = vectortransform.line_for_dim_X(column,current_view)

                                new_line_for_dim_center_Y = line_Y_2

                                new_line_for_dim_total_Y = line_Y_1

                                tong_hop_line_X = vectortransform.tinh_toan_line_dim_cot_1_2_3 (line_X,Y_vector,max_value_Y,offset_of_dim, current_view)

                                line_X_2 = tong_hop_line_X[1]

                                line_X_1 = tong_hop_line_X[2]

                                new_line_for_dim_center_X = line_X_2

                                new_line_for_dim_total_X = line_X_1
                            except:
                                print(traceback.format_exc())
                                pass

                            column_reference = ReferenceArray()
                        
                            list_column_reference = []

                            column_reference_center_X = ReferenceArray()

                            column_reference_total = ReferenceArray()

                            column_reference_total_X = ReferenceArray()   

                            ref_beam = Reference(column)

                            all_grid = selection.get_all_grid(doc,current_view)
                            
                            for grid in all_grid:

                                list_grid_ref_Y = []

                                geo_all_grid = geometry.get_all_geometry_of_grids(grid,current_view, DatumExtentType = DatumExtentType.ViewSpecific)

                                for one_grid_curve in geo_all_grid:

                                    for two_grid_curve in one_grid_curve:

                                        grid_plane = vectortransform.create_plane_follow_line(two_grid_curve)

                                        check_pararel_beam_with_grid = vectortransform.are_planes_parallel(Y_vector,grid_plane.Normal)

                                        if check_pararel_beam_with_grid:

                                            distance_grid_with_beam =  abs(vectortransform.distance_between_parallel_planes(grid_plane, X_plane))

                                            if distance_grid_with_beam < max_value_Y:

                                                ref_grid = Reference(grid)

                                                column_reference.Append(ref_grid)

                                                list_grid_ref_Y.append(ref_grid)

                                                list_column_reference.append(ref_grid)

                                if len(list_grid_ref_Y) > 0:
                                    break

                            for grid_X in all_grid:

                                list_grid_ref_X = []

                                geo_all_grid_X = geometry.get_all_geometry_of_grids(grid_X, current_view, DatumExtentType = DatumExtentType.ViewSpecific)

                                for one_grid_curve_X in geo_all_grid_X:

                                    for two_grid_curve_X in one_grid_curve_X:

                                        grid_plane_X = vectortransform.create_plane_follow_line(two_grid_curve_X)

                                        check_pararel_beam_with_grid_X = vectortransform.are_planes_parallel(X_vector,grid_plane_X.Normal)

                                        if check_pararel_beam_with_grid_X:

                                            distance_grid_with_beam_X =  abs(vectortransform.distance_between_parallel_planes(grid_plane_X, Y_plane))

                                            if distance_grid_with_beam_X < max_value_X:

                                                ref_grid_X = Reference(grid_X)

                                                list_grid_ref_X.append(grid_X)

                                                column_reference_center_X.Append(ref_grid_X)

                                if len(list_grid_ref_X) > 0:

                                    break
                            try:            
                                column_reference.Append(ref_face_max_Y)

                                column_reference.Append(ref_face_min_Y)

                                list_column_reference.append(ref_face_max_Y)

                                list_column_reference.append(ref_face_min_Y)

                                column_reference_total.Append(ref_face_max_Y)

                                column_reference_total.Append(ref_face_min_Y)

                            except:

                                pass
                            try: 
                                column_reference_center_X.Append(ref_face_max_X)

                                column_reference_center_X.Append(ref_face_min_X)

                                column_reference_total_X.Append(ref_face_max_X)

                                column_reference_total_X.Append(ref_face_min_X)    
                            except:

                                pass
                            check_grid_and_beam = []

                            check_grid_and_beam_X = []

                            try:
                                for check_ref_grid in column_reference:

                                    if ref_grid == check_ref_grid:

                                        check_grid_and_beam.append(True)

                            except:

                                pass

                            try:
                                for check_ref_grid_X in column_reference_center_X:

                                    if ref_grid_X == check_ref_grid_X:

                                        check_grid_and_beam_X.append(True)
                            except:

                                pass

                            if column_reference.Size > 2:

                                dim_center = doc.Create.NewDimension(current_view, line_doc_2, column_reference)
                                list_new_dim.append(dim_center)

                            else:

                                dim_center = 0

                            dim_total = doc.Create.NewDimension(current_view, line_doc_1, column_reference_total)
                            list_new_dim.append(dim_total)

                            if column_reference_center_X.Size > 2:

                                dim_center_X = doc.Create.NewDimension(current_view, line_ngang_2, column_reference_center_X)
                                list_new_dim.append(dim_center_X)

                            else: 

                                dim_center_X = 0

                            dim_total_X = doc.Create.NewDimension(current_view, line_ngang_1, column_reference_total_X)  
                            list_new_dim.append(dim_total_X)                      

                            if dim_center != 0:

                                try:

                                    allinone.move_text_dim(dim_center, current_view)

                                except:

                                    pass  
                                
                            if dim_center_X != 0:

                                try:

                                    allinone.move_text_dim(dim_center_X, current_view)

                                except:
                                    pass  
                # Tao detail line de kiem chung
                            # create_detail_line = detail_line(doc, current_view, new_line_for_dim_center)    
                        except:
                            # print(traceback.format_exc())
                            pass
    try:
        selection.select_sau_khi_chay_tool(list_new_dim,uidoc)
    except:
        pass
    trans_group.Assimilate()
