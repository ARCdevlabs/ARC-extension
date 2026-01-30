# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import Line
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
from pyrevit import revit
import nances
from nances import geometry
from nances import vectortransform, allinone
from Autodesk.Revit.DB import *
import tim_reference_column
import traceback

if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    current_view = doc.ActiveView
    view_scale = current_view.Scale
    Curve = []

    def get_all_grid(doc, active_view):
        collector = FilteredElementCollector(doc, active_view.Id).OfClass(Grid)
        visible_grids = [grid for grid in collector if not grid.ViewSpecific]
        return visible_grids

    def get_Y_vector(column):
        Y_orient = column.FacingOrientation
        return Y_orient

    def get_X_vector(column):
        X_orient = column.HandOrientation
        return X_orient

    def line_for_dim_Y (column,view):
        point = column.Location.Point
        Y_vector = get_Y_vector(column)
        vector_chuan_hoa = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_duoi_len_tren(Y_vector,view)
        point_Y_2 = vectortransform.move_point_along_vector(point,vector_chuan_hoa,1)
        line_Y = Line.CreateBound(point,point_Y_2)
        return line_Y

    def line_for_dim_X (column,view):
        point = column.Location.Point
        X_vector =get_X_vector(column)
        vector_chuan_hoa = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_duoi_len_tren(X_vector,view)
        point_X_2 = vectortransform.move_point_along_vector(point,vector_chuan_hoa,1)
        line_X = Line.CreateBound(point,point_X_2)
        return line_X

    def detail_line (doc, view, line):
        detail_line= doc.Create.NewDetailCurve(view,line)
        return detail_line
    
    def tinh_toan_line_dim_cot_1_2_3 (line_ngay_tam_cot, vector ,nua_chieu_rong_cot, view):

        view_scale = view.Scale

        khoang_cach_dim_3 = (9 / 304.8)

        snap_dim =  (5 / 304.8)

        tinh_toan_dim_3 = nua_chieu_rong_cot/view_scale + (khoang_cach_dim_3)

        tinh_toan_dim_2 = nua_chieu_rong_cot/view_scale + (khoang_cach_dim_3 + snap_dim)

        tinh_toan_dim_1 = nua_chieu_rong_cot/view_scale + (khoang_cach_dim_3 + snap_dim + snap_dim)

        line_dim_3 = vectortransform.move_line_theo_vector_theo_ty_le_view(vector, line_ngay_tam_cot, tinh_toan_dim_3, current_view)

        line_dim_2 = vectortransform.move_line_theo_vector_theo_ty_le_view(vector, line_ngay_tam_cot, tinh_toan_dim_2, current_view)

        line_dim_1 = vectortransform.move_line_theo_vector_theo_ty_le_view(vector, line_ngay_tam_cot, tinh_toan_dim_1, current_view)

        return line_dim_3,line_dim_2,line_dim_1
    
    Ele = nances.get_elements(uidoc,doc, "Select Foundation or Columns", noti = False)
    try:
        list_can_not_dim = []
        if Ele:
            with revit.Transaction("Prepair for Dim", swallow_errors=True):
                for column in Ele:
                    has_modified_geo = column.HasModifiedGeometry()
                    if has_modified_geo == False:
                        list_can_not_dim.append(column)
                        list_comprehension = [item for item in Ele if item not in list_can_not_dim]
                        first_item_list_comprehension=[]
                        first_item_list_comprehension.append(list_comprehension[0])
                        cut_geometry = nances.cut_geometry_all(doc, list_can_not_dim, first_item_list_comprehension)
    except:
        pass
    if Ele:
        with revit.Transaction("Dim total center", swallow_errors=True):

            for column in Ele:

                has_modified_geo = column.HasModifiedGeometry()

                if has_modified_geo:

                    try:

                        point_location = column.Location.Point

                        geo = geometry.get_geometry(column)

                        faces = geometry.get_face(geo)

                        X_vector_chua_chuan_hoa =get_X_vector(column)

                        Y_vector_chua_chuan_hoa = get_Y_vector(column)

                        X_vector = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_duoi_len_tren(X_vector_chua_chuan_hoa,current_view)

                        Y_vector = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_duoi_len_tren(Y_vector_chua_chuan_hoa,current_view)

                        Y_plane = Plane.CreateByNormalAndOrigin(X_vector, point_location)

                        X_plane = Plane.CreateByNormalAndOrigin(Y_vector, point_location)

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
                            line_Y = line_for_dim_Y(column,current_view)

                            tong_hop_line_Y = tinh_toan_line_dim_cot_1_2_3 (line_Y,X_vector,max_value_X, current_view)

                            line_Y_2 = tong_hop_line_Y[1]

                            line_Y_1 = tong_hop_line_Y[2]

                            line_X = line_for_dim_X(column,current_view)

                            new_line_for_dim_center_Y = line_Y_2

                            new_line_for_dim_total_Y = line_Y_1

                            tong_hop_line_X = tinh_toan_line_dim_cot_1_2_3 (line_X,Y_vector,max_value_Y, current_view)

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

                        all_grid = get_all_grid(doc,current_view)
                        
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

                            dim_center = doc.Create.NewDimension(current_view, new_line_for_dim_center_Y, column_reference)

                        else:

                            dim_center = 0

                        dim_total = doc.Create.NewDimension(current_view, new_line_for_dim_total_Y, column_reference_total)

                        if column_reference_center_X.Size > 2:

                            dim_center_X = doc.Create.NewDimension(current_view, new_line_for_dim_center_X, column_reference_center_X)

                        else: 

                            dim_center_X = 0

                        dim_total_X = doc.Create.NewDimension(current_view, new_line_for_dim_total_X, column_reference_total_X)                        

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


