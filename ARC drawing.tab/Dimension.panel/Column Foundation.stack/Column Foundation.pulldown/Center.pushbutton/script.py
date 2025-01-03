# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import Line
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
from pyrevit import revit
import nances as module
from nances import geometry
from nances import vectortransform
from Autodesk.Revit.DB import *
import tim_reference_column


if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Currentview = doc.ActiveView
    view_scale = Currentview.Scale
    Curve = []


    def get_all_grid(doc, active_view):
        collector = FilteredElementCollector(doc, active_view.Id).OfClass(Grid)
        visible_grids = [grid for grid in collector if not grid.ViewSpecific]
        return visible_grids

    def get_all_geometry_of_grids(grid, DatumExtentType = DatumExtentType.ViewSpecific):
        all_geometry = []
        DatumExtentType = DatumExtentType.ViewSpecific
        geometry_element = grid.GetCurvesInView(DatumExtentType,Currentview)
        all_geometry.append(geometry_element)
        return all_geometry

    def get_Y_vector(column):
        Y_orient = column.FacingOrientation
        return Y_orient

    def get_X_vector(column):
        X_orient = column.HandOrientation
        return X_orient

    def line_for_dim_Y (column):
        point = column.Location.Point
        Y_vector = get_Y_vector(column)
        point_Y_2 = vectortransform.move_point_along_vector(point,Y_vector,20)
        line_Y = Line.CreateBound(point,point_Y_2)
        return line_Y

    def line_for_dim_X (column):
        point = column.Location.Point
        X_vector =get_X_vector(column)
        point_X_2 = vectortransform.move_point_along_vector(point,X_vector,20)
        line_X = Line.CreateBound(point,point_X_2)
        return line_X

    def translate_line (line, vector, distance):
        start_point = line.GetEndPoint(0)
        end_point = line.GetEndPoint(1)
        new_start_point = vectortransform.move_point_along_vector(start_point,vector ,distance)
        new_end_point = vectortransform.move_point_along_vector(end_point, vector,distance)
        new_line= Line.CreateBound(new_start_point,new_end_point)
        return new_line

    def detail_line (doc, view, line):
        detail_line= doc.Create.NewDetailCurve(view,line)
        return detail_line

    Ele = module.get_elements(uidoc,doc, "Select Foundation or Columns", noti = False)
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
                        cut_geometry = module.cut_geometry_all(doc, list_can_not_dim, first_item_list_comprehension)
    except:
        pass
    if Ele:
        with revit.Transaction("Column Dimension", swallow_errors=True):
            for column in Ele:
                has_modified_geo = column.HasModifiedGeometry()
                if has_modified_geo:
                    try:
                        point_location = column.Location.Point
                        geo = geometry.get_geometry(column)
                        faces = geometry.get_face(geo)
                        X_vector =get_X_vector(column)
                        Y_vector = get_Y_vector(column)
                        Y_plane = Plane.CreateByNormalAndOrigin(X_vector, point_location)
                        X_plane = Plane.CreateByNormalAndOrigin(Y_vector, point_location)
                        list_distance_Y = []
                        list_distance_X = []
                        list_outer_face_Y = []
                        list_outer_face_X = []
                        unique_id = column.UniqueId
                        call_class_tim_reference = tim_reference_column.ClassTimReference(faces, X_vector, Y_vector, X_plane, Y_plane, vectortransform)
                        result = call_class_tim_reference.tim_reference_column()
                        ref_face_min = result.ref_face_min
                        ref_face_max = result.ref_face_max
                        ref_face_min_X = result.ref_face_min_X
                        ref_face_max_X = result.ref_face_max_X
                        max_value = result.max_value_Y
                        max_value_X = result.max_value_X

                        try:
                            line_Y = line_for_dim_Y(column)
                            new_line_for_dim_center = translate_line(line_Y, X_vector, max_value_X + (view_scale/50)*1.5)
                            new_line_for_dim_total = translate_line(line_Y, X_vector, max_value_X + (view_scale/50)*2.5)

                            line_X = line_for_dim_X(column)
                            new_line_for_dim_center_X = translate_line(line_X, Y_vector, max_value + (view_scale/50)*1.5)
                            new_line_for_dim_total_X = translate_line(line_X, Y_vector, max_value + (view_scale/50)*2.5)
                        except:
                            # import traceback
                            # print(traceback.format_exc())
                            pass

                        # Cai nay de dim 
                        wall_reference = ReferenceArray()
                        list_wall_refererence = []
                        wall_reference_center_X = ReferenceArray()
                        wall_reference_total = ReferenceArray()
                        wall_reference_total_X = ReferenceArray()    
                        ref_beam = Reference(column)

                        all_grid = get_all_grid(doc,Currentview)
                        for grid in all_grid:
                            list_grid_ref_Y = []
                            geo_all_grid = get_all_geometry_of_grids(grid, DatumExtentType)
                            for one_grid_curve in geo_all_grid:
                                for two_grid_curve in one_grid_curve:
                                    grid_plane = vectortransform.create_plane_follow_line(two_grid_curve)
                                    check_pararel_beam_with_grid = vectortransform.are_planes_parallel(Y_vector,grid_plane.Normal)
                                    if check_pararel_beam_with_grid:
                                        distance_grid_with_beam =  abs(vectortransform.distance_between_parallel_planes(grid_plane, X_plane))
                                        if distance_grid_with_beam < max_value:
                                            ref_grid = Reference(grid)
                                            wall_reference.Append(ref_grid)
                                            list_grid_ref_Y.append(ref_grid)
                                            list_wall_refererence.append(ref_grid)
                            if len(list_grid_ref_Y) > 0:
                                break

                        for grid_X in all_grid:
                            list_grid_ref_X = []
                            geo_all_grid_X = get_all_geometry_of_grids(grid_X, DatumExtentType)
                            for one_grid_curve_X in geo_all_grid_X:
                                for two_grid_curve_X in one_grid_curve_X:
                                    grid_plane_X = vectortransform.create_plane_follow_line(two_grid_curve_X)
                                    check_pararel_beam_with_grid_X = vectortransform.are_planes_parallel(X_vector,grid_plane_X.Normal)
                                    if check_pararel_beam_with_grid_X:
                                        distance_grid_with_beam_X =  abs(vectortransform.distance_between_parallel_planes(grid_plane_X, Y_plane))
                                        if distance_grid_with_beam_X < max_value_X:
                                            ref_grid_X = Reference(grid_X)
                                            list_grid_ref_X.append(grid_X)
                                            wall_reference_center_X.Append(ref_grid_X)
                            if len(list_grid_ref_X) > 0:
                                break
                        try:            
                            wall_reference.Append(ref_face_max)
                            wall_reference.Append(ref_face_min)
                            list_wall_refererence.append(ref_face_max)
                            list_wall_refererence.append(ref_face_min)
                            wall_reference_total.Append(ref_face_max)
                            wall_reference_total.Append(ref_face_min)
                        except:
                            pass
                        try: 
                            wall_reference_center_X.Append(ref_face_max_X)
                            wall_reference_center_X.Append(ref_face_min_X)
                            wall_reference_total_X.Append(ref_face_max_X)
                            wall_reference_total_X.Append(ref_face_min_X)    
                        except:
                            pass
                        check_grid_and_beam = []
                        check_grid_and_beam_X = []
                        try:
                            for check_ref_grid in wall_reference:
                                if ref_grid == check_ref_grid:
                                    check_grid_and_beam.append(True)
                        except:
                            pass

                        try:
                            for check_ref_grid_X in wall_reference_center_X:
                                if ref_grid_X == check_ref_grid_X:
                                    check_grid_and_beam_X.append(True)
                        except:
                            pass

                        if wall_reference.Size > 2:
                            dim_center = doc.Create.NewDimension(Currentview, new_line_for_dim_center, wall_reference)
                        else:
                            dim_center = 0
                        # dim_total = doc.Create.NewDimension(Currentview, new_line_for_dim_total, wall_reference_total)
                        if wall_reference_center_X.Size > 2:
                            dim_center_X = doc.Create.NewDimension(Currentview, new_line_for_dim_center_X, wall_reference_center_X)
                        else: 
                            dim_center_X = 0
                        # dim_total_X = doc.Create.NewDimension(Currentview, new_line_for_dim_total_X, wall_reference_total_X)

                        def move_text_of_dim(dim, view):
                            curve_dim_direction = dim.Curve.Direction
                            seg_1_position = dim.Segments.Item[0].TextPosition 
                            seg_2_position = dim.Segments.Item[1].TextPosition
                            seg_1_value = float(dim.Segments.Item[0].Value * 304.8)
                            seg_2_value = float(dim.Segments.Item[1].Value * 304.8)
                            round_format_value_1 = round(seg_1_value,2)
                            round_format_value_2 = round(seg_2_value,2)
                            formatted_value_1 = str(round_format_value_1).rstrip('0').rstrip('.')
                            formatted_value_2 = str(round_format_value_2).rstrip('0').rstrip('.')
                            len_formatted_value_1 = len(formatted_value_1)
                            len_formatted_value_2 = len(formatted_value_2)
                            one_unit_width = 1.83 #Chieu rong 1 don vi text
                            khoang_cach_tu_dim = 0.5 * (view.Scale)
                            width_text_1 = float(len_formatted_value_1 * one_unit_width * (view.Scale))
                            width_text_2 = float(len_formatted_value_2 * one_unit_width * (view.Scale))
                            total_value = seg_1_value + seg_2_value
                            ti_le_1 = seg_1_value / (total_value)
                            ti_le_2 = seg_2_value / (total_value)
                            width = total_value
                            if seg_1_value < width_text_1: 
                                width_offset_text_1 = (seg_1_value/2 + width_text_1/2 + khoang_cach_tu_dim)
                            else:
                                width_offset_text_1 = 0
                            move_seg_1 = vectortransform.move_point_along_vector(seg_1_position,curve_dim_direction, - (width_offset_text_1/304.8))

                            if seg_2_value < width_text_2: 
                                width_offset_text_2 = (seg_2_value/2 + width_text_2/2 + khoang_cach_tu_dim)
                            else:
                                width_offset_text_2 = 0            
                            move_seg_2 = vectortransform.move_point_along_vector(seg_2_position,curve_dim_direction, (width_offset_text_2/304.8))
                            dim.Segments.Item[0].TextPosition = move_seg_1
                            dim.Segments.Item[1].TextPosition = move_seg_2
                            leader_dim = dim.get_Parameter(BuiltInParameter.DIM_LEADER)
                            leader_dim.Set(False)     
                            return
                        if dim_center != 0:
                            try:
                                move_text_of_dim(dim_center, Currentview)
                            except:
                                pass  
                        if dim_center_X != 0:
                            try:
                                move_text_of_dim(dim_center_X, Currentview)
                            except:
                                pass           
                    except:
                        pass






