# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
import traceback
import math
import nances as module
from nances import vectortransform,geometry
import tim_reference_beam

if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Currentview = doc.ActiveView
    Curve = []
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
    def get_rotate_90_location_wall (wall):
        from Autodesk.Revit.DB import Line, BuiltInParameter
        wall_location = wall.Location
        wall_location_curve = wall_location.Curve
        wall_location_curve_start_point = wall_location_curve.GetEndPoint(0)
        wall_location_curve_end_point = wall_location_curve.GetEndPoint(1)
        flat_start = XYZ(wall_location_curve_start_point.X,wall_location_curve_start_point.Y,wall_location_curve_start_point.Z)
        flat_end = XYZ(wall_location_curve_end_point.X,wall_location_curve_end_point.Y,wall_location_curve_start_point.Z)
        flat_line = Line.CreateBound(flat_start, flat_end)
        mid_point = flat_line.Evaluate(0.5, True)
        Z_point = XYZ(mid_point.X, mid_point.Y, mid_point.Z + 10)
        Z_axis = Line.CreateBound(mid_point, Z_point)
        curve_of_location_curve = Line.CreateBound(flat_start,flat_end)
        detail_curve_of_location_curve = doc.Create.NewDetailCurve(Currentview,curve_of_location_curve)
        locate_detail_curve_of_location_curve = detail_curve_of_location_curve.Location
        rotate_locate_detail_curve_of_location_curve = locate_detail_curve_of_location_curve.Rotate(Z_axis, 2 * math.pi / 4)
        direction_of_wall = wall_location_curve.Direction
        Scale = 50
        Snap_dim = 0 * 0.0032808 #1mm bang 0.0032808feet
        Vector_for_scale = Snap_dim * Scale *direction_of_wall
        move_detail_curve = locate_detail_curve_of_location_curve.Move(Vector_for_scale)
        return detail_curve_of_location_curve
            
    def get_geometry(element):
        option = Options()
        option.ComputeReferences = True
        geo_ref =  element.get_Geometry(option)
        return geo_ref

    def get_geometry_3(element, view):
        geo_opt = Options()
        geo_opt.ComputeReferences = True
        geo_opt.IncludeNonVisibleObjects = True
        geo_opt.View = view
        geo_ref =  element.get_Geometry(geo_opt)
        return geo_ref

    def get_face(geometry):
        list_faces =[]
        for geometry_object in geometry:
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

    Ele =module.get_elements(uidoc,doc, "Select Beams", noti = False)

    if Ele:
        trans_group = TransactionGroup(doc, "Dim Total Beam")
        trans_group.Start()
        try:
            from nances import revit
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
            pass

        t = Transaction(doc,"Dimension wall (face to face)")
        t.Start()
        for wall in Ele:
            try:
                geo = (get_geometry_3(wall, Currentview))
                faces = get_face(geo)
                center_plane = get_center_plane(wall)
                center_plane_normal = center_plane.Normal
                list_distance = []
                list_outer_face = []

                call_class_tim_reference = tim_reference_beam.ClassTimReference(faces,center_plane, vectortransform)                
                result = call_class_tim_reference.tim_reference_beam()
                ref_face_min = result.ref_face_min
                ref_face_max = result.ref_face_max
                max_value = result.max_value

                detail_line = get_rotate_90_location_wall (wall)
                line = detail_line.Location.Curve
                wall_reference = ReferenceArray()
                wall_reference.Append(ref_face_min)
                wall_reference.Append(ref_face_max)
                dim = doc.Create.NewDimension(Currentview, line, wall_reference)
                delete_detail_curve = doc.Delete(detail_line.Id)               
            except:
                import traceback
                print(traceback.format_exc())
                pass
        t.Commit()
        trans_group.Assimilate()


