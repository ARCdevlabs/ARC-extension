# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FailuresAccessor
from Autodesk.Revit.DB import Line
from Autodesk.Revit.Creation import ItemFactoryBase
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
from pyrevit import revit
import math
from rpw import ui
from rpw.ui.forms import Alert
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
import sys
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
if module.AutodeskData():
    Currentview = doc.ActiveView
    view_scale = Currentview.Scale
    Curve = []
    def flatten_list(input_list):
        flat_list = [item for sublist in input_list for item in sublist]
        return flat_list
    def get_selected_elements():
        selection = uidoc.Selection
        selection_ids = selection.GetElementIds()
        elements = []
        for element_id in selection_ids:

            elements.append(doc.GetElement(element_id))
        return elements

    def create_plane_from_point_and_normal(point, normal):
        plane = Plane(normal, point)
        return plane

    def are_planes_parallel(normal1, normal2):
        tolerance=0.0000001
        cross_product = normal1.CrossProduct(normal2)
        return cross_product.GetLength() < tolerance

    def distance_between_planes(normal1, point_on_plane1, normal2):
        vector_between_planes = point_on_plane1 - (point_on_plane1.DotProduct(normal2) - normal2.DotProduct(normal1)) / normal1.DotProduct(normal2) * normal1
        distance = vector_between_planes.GetLength()
        return distance
    def get_point_at_center_line(wall):
        wall_location = wall.Location
        wall_location_curve = wall_location.Curve
        start_point = wall_location_curve.GetEndPoint(0)
        return start_point
    def get_center_plane (wall):
        wall_location = wall.Location
        wall_location_curve = wall_location.Curve
        start_point = wall_location_curve.GetEndPoint(0)
        endpoint = wall_location_curve.GetEndPoint(1)
        mid_point = wall_location_curve.Evaluate(0.5, True)
        offset_mid_point = XYZ(start_point.X, start_point.Y, mid_point.Z +10000)
        point1 = start_point
        point2 = endpoint
        point3 =offset_mid_point
        vector1 = point2 - point1
        vector2 = point3 - point1
        normal_vector = vector1.CrossProduct(vector2).Normalize()
        plane = Plane.CreateByNormalAndOrigin(normal_vector, mid_point)
        return plane

    def create_plane_follow_line (curve):
        start_point = curve.GetEndPoint(0)
        endpoint = curve.GetEndPoint(1)
        mid_point = curve.Evaluate(0.5, True)
        offset_mid_point = XYZ(start_point.X, start_point.Y, mid_point.Z +10000)
        point1 = start_point
        point2 = endpoint
        point3 =offset_mid_point
        vector1 = point2 - point1
        vector2 = point3 - point1
        normal_vector = vector1.CrossProduct(vector2).Normalize()
        plane = Plane.CreateByNormalAndOrigin(normal_vector, mid_point)
        return plane

            
    def get_geometry(element):
        option = Options()
        option.ComputeReferences = True
        geo_ref =  element.get_Geometry(option)
        return geo_ref
    def get_geometry_2(element):
        options = Options()
        options.ComputeReferences = True
        options.IncludeNonVisibleObjects = False
        options.DetailLevel = Autodesk.Revit.DB.ViewDetailLevel.Fine
        geometryElement = element.get_Geometry(options)
        return geometryElement


    def get_face(geometry):
        list_faces =[]
        for geometry_object in geometry:
            # print geometry_object
            if hasattr(geometry_object, "Faces"):
                for face in geometry_object.Faces:
                    list_faces.append(face)
        return list_faces
    def distance_to_plane(point, plane):
        distance = plane.Normal.DotProduct(point - plane.Origin)
        return distance
    def distance_between_parallel_planes(plane1, plane2):
        point_on_plane = XYZ(-54321, -54321, 0)
        distance1 = abs(distance_to_plane(point_on_plane, plane1))
        distance2 = abs(distance_to_plane(point_on_plane, plane2))
        distance = (distance1 - distance2)
        return distance

    def contains_string(string, symbol):
        lowercase_input = string.lower()
        return symbol in lowercase_input

    def get_rotate_90_location_wall (wall):
        from Autodesk.Revit.DB import Line, BuiltInParameter
        wall_location = wall.Location
        wall_location_curve = wall_location.Curve
        start = wall_location_curve.GetEndPoint(0)
        end = wall_location_curve.GetEndPoint(1)
        flat_start = XYZ(start.X,start.Y, start.Z)
        flat_end =  XYZ(end.X,end.Y, start.Z)
        flat_line =  Line.CreateBound(flat_start,flat_end)
        mid_point = flat_line.Evaluate(0.5, True)
        Z_point = XYZ(mid_point.X, mid_point.Y, mid_point.Z + 10)
        Z_axis = Line.CreateBound(mid_point, Z_point)
        curve_of_location_curve = Line.CreateBound(flat_start,flat_end)
        detail_curve_of_location_curve = doc.Create.NewDetailCurve(Currentview,curve_of_location_curve)
        locate_detail_curve_of_location_curve = detail_curve_of_location_curve.Location
        rotate_locate_detail_curve_of_location_curve = locate_detail_curve_of_location_curve.Rotate(Z_axis, 2 * math.pi / 4)
        direction_of_wall = flat_line.Direction
        Scale = Currentview.Scale
        Snap_dim = 4.5 * 0.0032808 #1mm bang 0.0032808feet
        Vector_for_scale = Snap_dim * Scale *direction_of_wall
        move_detail_curve = locate_detail_curve_of_location_curve.Move(Vector_for_scale)
        return detail_curve_of_location_curve

    def get_wall_reference_by_magic(uid,index):
        format = "{0}:{1}:{2}"
        nine = -9999
        refString = str.Format(format,uid,nine,index)
        return refString


    def get_wall_reference_by_type(uid,index):
        from Autodesk.Revit.DB import Reference
        format = "{0}:{1}:{2}"
        type = 'SURFACE'
        refString = str.Format(format,uid,index,type)
        return refString

    def move_point_along_vector(point, vector, distance):
        new_point = point + vector.Normalize() * distance
        return new_point


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

    def move_point_along_vector(point, vector, distance):
        new_point = point + vector.Normalize() * distance
        return new_point

    def line_for_dim_Y (column):
        point = column.Location.Point
        Y_vector = get_Y_vector(column)
        point_Y_2 = move_point_along_vector(point,Y_vector,20)
        line_Y = Line.CreateBound(point,point_Y_2)
        return line_Y

    def line_for_dim_X (column):
        point = column.Location.Point
        X_vector =get_X_vector(column)
        point_X_2 = move_point_along_vector(point,X_vector,20)
        line_X = Line.CreateBound(point,point_X_2)
        return line_X

    def translate_line (line, vector, distance):
        start_point = line.GetEndPoint(0)
        end_point = line.GetEndPoint(1)
        new_start_point = move_point_along_vector(start_point,vector ,distance)
        new_end_point = move_point_along_vector(end_point, vector,distance)
        new_line= Line.CreateBound(new_start_point,new_end_point)
        return new_line

    def detail_line (doc, view, line):
        detail_line= doc.Create.NewDetailCurve(view,line)
        return detail_line

    def move_text_of_dim(dim, view):
        curve_dim_direction = dim.Curve.Direction
        seg_1_position = dim.Segments.Item[0].TextPosition 
        seg_2_position = dim.Segments.Item[1].TextPosition
        seg_1_value = float(dim.Segments.Item[0].Value * 304.8)
        seg_2_value = float(dim.Segments.Item[1].Value * 304.8)
        value_string_1 = dim.Segments.Item[0].ValueString
        value_string_2 = dim.Segments.Item[1].ValueString
        round_format_value_1 = round(seg_1_value,2)
        round_format_value_2 = round(seg_2_value,2)
        # formatted_value_1 = str(round_format_value_1).rstrip('0').rstrip('.')
        # formatted_value_2 = str(round_format_value_2).rstrip('0').rstrip('.').
        len_formatted_value_1 = len(value_string_1)
        len_formatted_value_2 = len(value_string_2)
        one_unit_width = 1.83 #Chieu rong 1 don vi text
        khoang_cach_tu_dim = 0.5 * (view.Scale)
        width_text_1 = float(len_formatted_value_1 * one_unit_width * (view.Scale))
        width_text_2 = float(len_formatted_value_2 * one_unit_width * (view.Scale))
        total_value = seg_1_value + seg_2_value
        # ti_le_1 = seg_1_value / (total_value)
        # ti_le_2 = seg_2_value / (total_value)
        # width = total_value
        if seg_1_value < width_text_1: 
            width_offset_text_1 = (seg_1_value/2 + width_text_1/2 + khoang_cach_tu_dim)
        else:
            width_offset_text_1 = 0
        move_seg_1 = move_point_along_vector(seg_1_position,curve_dim_direction, - (width_offset_text_1/304.8))

        if seg_2_value < width_text_2: 
            width_offset_text_2 = (seg_2_value/2 + width_text_2/2 + khoang_cach_tu_dim)
        else:
            width_offset_text_2 = 0       
        # print width_offset_text_1, width_offset_text_2    
        move_seg_2 = move_point_along_vector(seg_2_position,curve_dim_direction, (width_offset_text_2/304.8))
        dim.Segments.Item[0].TextPosition = move_seg_1
        dim.Segments.Item[1].TextPosition = move_seg_2
        leader_dim = dim.get_Parameter(BuiltInParameter.DIM_LEADER)
        leader_dim.Set(False)     
        return
    Ele = module.get_elements(uidoc,doc, "Select Foundation or Columns", noti = False)
    # if not Ele:
    #     import sys
    #     sys.exit()
    if Ele:
        with revit.TransactionGroup("Dim Total and Center Column"):     
            try:
                list_can_not_dim = []       
                with revit.Transaction("Prepair for Dim", swallow_errors=True):  
                    for column in Ele:
                        try:
                            has_modified_geo = column.HasModifiedGeometry()
                            if has_modified_geo == False:
                                list_can_not_dim.append(column)
                                if len(list_can_not_dim) > 0 and len(Ele) < 2 :
                                    dialog = Autodesk.Revit.UI.TaskDialog("ARC")
                                    dialog.MainContent = "Try With 2 or More Elements"
                                    dialog.TitleAutoPrefix = False
                                    dialog.Show() 
                                else:
                                    list_comprehension = [item for item in Ele if item not in list_can_not_dim]
                                    first_item_list_comprehension=[]
                                    first_item_list_comprehension.append(list_comprehension[0])      
                                    cut_geometry = module.cut_geometry_all(doc, list_can_not_dim, first_item_list_comprehension)
                        except:
                            pass
            except:
                pass


            with revit.Transaction("Dim total center", swallow_errors=True):
                for column in Ele:
                    has_modified_geo = column.HasModifiedGeometry()
                    if has_modified_geo:
                        try:
                            point_location = column.Location.Point
                            geo = (get_geometry_2(column))
                            faces = get_face(geo)
                            X_vector =get_X_vector(column)
                            Y_vector = get_Y_vector(column)
                            Y_plane = Plane.CreateByNormalAndOrigin(X_vector, point_location)
                            X_plane = Plane.CreateByNormalAndOrigin(Y_vector, point_location)
                            list_distance_Y = []
                            list_distance_X = []
                            list_outer_face_Y = []
                            list_outer_face_X = []
                            unique_id = column.UniqueId
                            # Dim doc theo phuong X
                            for face in faces:
                                try:
                                    face_origin = face.Origin
                                    face_normal = face.FaceNormal
                                    face_to_plane = Plane.CreateByNormalAndOrigin(face_normal, face_origin)
                                    # face_to_plane_X = Plane.CreateByNormalAndOrigin(face_normal, face_origin)
                                    normal_face_to_plane = face_to_plane.Normal
                                    check_pararel_Y = are_planes_parallel(Y_vector,face_normal)
                                    if check_pararel_Y == False:
                                        check_pararel_X = are_planes_parallel(X_vector,face_normal)

                                    if check_pararel_Y == True: 
                                        distance_Y =  distance_between_parallel_planes(face_to_plane, X_plane)
                                        list_distance_Y.append(distance_Y)
                                        list_outer_face_Y.append(face.Reference)

                                    else:
                                        if check_pararel_X == True:
                                            distance_X =  distance_between_parallel_planes(face_to_plane, Y_plane)
                                            list_distance_X.append(distance_X)
                                            list_outer_face_X.append(face.Reference)
                                except:
                                    pass

                            try:
                                max_value = max(list_distance_Y)
                                max_index = list_distance_Y.index(max_value)
                                min_value = min(list_distance_Y)
                                min_index = list_distance_Y.index(min_value)
                                ref_face_max = list_outer_face_Y[max_index]
                                ref_face_min = list_outer_face_Y[min_index]
                            except:
                                # import traceback
                                # print(traceback.format_exc())
                                pass

                            try:
                                max_value_X = max(list_distance_X)
                                max_index_X = list_distance_X.index(max_value_X)
                                min_value_X = min(list_distance_X)
                                min_index_X = list_distance_X.index(min_value_X)
                                ref_face_max_X = list_outer_face_X[max_index_X]
                                ref_face_min_X = list_outer_face_X[min_index_X]
                            except:
                                # import traceback
                                # print(traceback.format_exc())
                                pass

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
                                        grid_plane = create_plane_follow_line(two_grid_curve)
                                        check_pararel_beam_with_grid = are_planes_parallel(Y_vector,grid_plane.Normal)
                                        if check_pararel_beam_with_grid:
                                            distance_grid_with_beam =  abs(distance_between_parallel_planes(grid_plane, X_plane))
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
                                        grid_plane_X = create_plane_follow_line(two_grid_curve_X)
                                        check_pararel_beam_with_grid_X = are_planes_parallel(X_vector,grid_plane_X.Normal)
                                        if check_pararel_beam_with_grid_X:
                                            distance_grid_with_beam_X =  abs(distance_between_parallel_planes(grid_plane_X, Y_plane))
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

                            # if len(check_grid_and_beam) == 0:
                            #     wall_reference.Append(ref_beam)
                            #     list_wall_refererence.append(ref_beam)

                            # if len(check_grid_and_beam_X) == 0:
                            #     wall_reference_center_X.Append(ref_beam)
                            # new_wall_reference = ReferenceArray()
                            # for b in list_wall_refererence:
                            #     convert = b.ConvertToStableRepresentation(doc)
                            #     if contains_string(convert, "surface"):
                            #         new_wall_reference.Append(b)
                            #     else:
                            #         ref_type = FamilyInstanceReferenceType.CenterFrontBack
                            #         get_ref_by_type = column.GetReferences(ref_type)
                                    
                                    # print dir(get_ref_by_type)
                                    # new_wall_reference.Append(ref)
                            if wall_reference.Size > 2:
                                dim_center = doc.Create.NewDimension(Currentview, new_line_for_dim_center, wall_reference)
                            else:
                                dim_center = 0
                            dim_total = doc.Create.NewDimension(Currentview, new_line_for_dim_total, wall_reference_total)
                            if wall_reference_center_X.Size > 2:
                                dim_center_X = doc.Create.NewDimension(Currentview, new_line_for_dim_center_X, wall_reference_center_X)
                            else: 
                                dim_center_X = 0
                            dim_total_X = doc.Create.NewDimension(Currentview, new_line_for_dim_total_X, wall_reference_total_X)

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
                # Tao detail line de kiem chung
                            # create_detail_line = detail_line(doc, Currentview, new_line_for_dim_center)
                            # create_detail_line = detail_line(doc, Currentview, new_line_for_dim_total)
                            # create_detail_line = detail_line(doc, Currentview, new_line_for_dim_center_X)
                            # create_detail_line = detail_line(doc, Currentview, new_line_for_dim_total_X)            
                        except:
                            # import traceback
                            # print(traceback.format_exc())
                            pass


