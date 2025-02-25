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
    #Get Document 
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

    def get_rotate_90_location_wall_center (wall):
        from Autodesk.Revit.DB import Line
        wall_location = wall.Location
        wall_location_curve = wall_location.Curve
        mid_point = wall_location_curve.Evaluate(0.5, True)
        Z_point = XYZ(mid_point.X, mid_point.Y, mid_point.Z + 10)
        Z_axis = Line.CreateBound(mid_point, Z_point)
        curve_of_location_curve = Line.CreateBound(wall_location_curve.GetEndPoint(0),wall_location_curve.GetEndPoint(1))
        detail_curve_of_location_curve = doc.Create.NewDetailCurve(Currentview,curve_of_location_curve)
        locate_detail_curve_of_location_curve = detail_curve_of_location_curve.Location
        retate_locate_detail_curve_of_location_curve = locate_detail_curve_of_location_curve.Rotate(Z_axis, 2 * math.pi / 4)
        return detail_curve_of_location_curve
            
    def get_geometry(element):
        option = Options()
        option.ComputeReferences = True
        geo_ref =  element.get_Geometry(option)
        return geo_ref

    def get_face(geometry):
        for solid in geometry:
            face = solid.Faces
        return face

    def distance_to_plane(point, plane):
        distance = plane.Normal.DotProduct(point - plane.Origin)
        return distance
    def distance_between_parallel_planes(plane1, plane2):
        point_on_plane = XYZ(0, 0, 0)
        distance1 = abs(distance_to_plane(point_on_plane, plane1))
        distance2 = abs(distance_to_plane(point_on_plane, plane2))
        distance = (distance1 - distance2)
        return distance
    
    Ele = module.get_elements(uidoc,doc, "Select Walls", noti = False)
    if Ele:
        t = Transaction(doc,"Dimension wall (face to face)")
        t.Start()
        for wall in Ele:
            try:
                geo = (get_geometry(wall))
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

                detail_line = get_rotate_90_location_wall_center (wall)
                line = detail_line.Location.Curve
                wall_reference = ReferenceArray()
                wall_reference.Append(ref_face_min)
                wall_reference.Append(ref_face_max)
                dim = doc.Create.NewDimension(Currentview, line, wall_reference)
                delete_detail_curve = doc.Delete(detail_line.Id)
            except:
                pass
        t.Commit()
