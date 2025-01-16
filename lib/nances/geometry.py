# -*- coding: utf-8 -*-
import Autodesk.Revit.DB as DB
import importdll
import_class = importdll.ImportDLL()
import_def = import_class.get_dll()

#get_geometry_non_reference: Sẽ lấy geometry nhưng không có những Reference để có thể áp dụng vào việc tạo dimension.
def get_geometry_non_reference(element):
    all_gemetry = []
    try:
        geo_opt = DB.Options()
        geometry =  element.get_Geometry(geo_opt)
        for instance_geometry in geometry:
            element_geometry = instance_geometry.GetInstanceGeometry()
            for tung_geometry in element_geometry:
                if isinstance(tung_geometry, DB.Solid) and tung_geometry.Volume > 0:
                    all_gemetry.append(tung_geometry)
        return all_gemetry #Trả về dạng list các solid
    except:
        return all_gemetry

#get_geometry: Sẽ lấy geometry và có những Reference để có thể áp dụng vào việc tạo dimension.
#Phương pháp này chỉ áp dụng được với các đối tượng với HasModifiedGeometry() == True
# def get_geometry(element):
#     option = DB.Options()
#     option.ComputeReferences = True
#     geo_ref = element.get_Geometry(option)
#     return geo_ref


def get_geometry(element):
    geo_ref = import_def.LibARC_Geometry.GetGeometry(element)
    return geo_ref

# find_intersect_elements: Lọc các đối tượng giao nhau với 1 đối tượng đầu vào.
def find_intersect_elements(idoc, element_A, list_element_B):
    result_element = []
    try:
        list_solid = get_geometry_non_reference(element_A)
        list_element_id_dau_vao = []
        for tung_element_dau_vao in list_element_B:
            list_element_id_dau_vao.append(tung_element_dau_vao.Id)
        for tung_solid in list_solid:
            tat_ca_intersect_elements = DB.FilteredElementCollector(idoc).WherePasses(DB.ElementIntersectsSolidFilter(tung_solid))
            for tung_element in tat_ca_intersect_elements:
                if tung_element.Id in list_element_id_dau_vao:
                    result_element.append(tung_element)
        return result_element #Trả về dạng list các element
    except:
        return result_element

# get_face:Lấy tất cả các face của một geometry. 
# def get_face(geometry):
#     list_faces =[]
#     for geometry_object in geometry:
#         if hasattr(geometry_object, "Faces"):
#             for face in geometry_object.Faces:
#                 list_faces.append(face)
#     return list_faces
def get_face(geometry):
    list_faces =[]
    faces = import_def.LibARC_Geometry.GetFaces(geometry)
    for face in faces:
        list_faces.append(face)
    return list_faces

def get_center_plane_of_wall (wall):
    wall_location = wall.Location
    wall_location_curve = wall_location.Curve
    start_point = wall_location_curve.GetEndPoint(0)
    endpoint = wall_location_curve.GetEndPoint(1)
    mid_point = wall_location_curve.Evaluate(0.5, True)
    offset_mid_point = DB.XYZ(start_point.X, start_point.Y, mid_point.Z +10000)
    point1 = start_point
    point2 = endpoint
    point3 =offset_mid_point
    vector1 = point2 - point1
    vector2 = point3 - point1
    normal_vector = vector1.CrossProduct(vector2).Normalize()
    plane = DB.Plane.CreateByNormalAndOrigin(normal_vector, mid_point)
    return plane 