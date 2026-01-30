# -*- coding: utf-8 -*-
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
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


'''2 def get_geometry và get_face hoạt động ổn định trên tool dim bằng geometry, tốt nhất đừng đụng vào'''
#get_geometry: Sẽ lấy geometry và có những Reference để có thể áp dụng vào việc tạo dimension.
#Phương pháp này chỉ áp dụng được với các đối tượng với HasModifiedGeometry() == True
def get_geometry(element): 
    geo_ref = import_def.LibARC_Geometry.GetGeometry(element)
    return geo_ref

def get_face(geometry):
    list_faces =[]
    faces = import_def.LibARC_Geometry.GetFaces(geometry)
    for face in faces:
        list_faces.append(face)
    return list_faces

'''2 def get_geometry và get_face hoạt động ổn định trên tool dim bằng geometry, tốt nhất đừng đụng vào'''

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


"""def viết thêm"""
def tinh_chieu_rong_dam(beam):
    #Lấy vector trục dầm

    # Xác định vector vuông góc với trục dầm

    # Chiếu các điểm bounding box lên vector đó

    # Lấy max – min → ra chiều rộng

    loc_curve = beam.Location.Curve
    direction_beam = (loc_curve.GetEndPoint(1) - loc_curve.GetEndPoint(0)).Normalize() #chuan hoa vector huong dam
    Z = XYZ.BasisZ
    width_direction = direction_beam.CrossProduct(Z).Normalize() #ket qua la vector

    bbox = beam.get_BoundingBox(None)
    min_pt = bbox.Min
    max_pt = bbox.Max
    points = [
    DB.XYZ(min_pt.X, min_pt.Y, min_pt.Z),
    XYZ(min_pt.X, min_pt.Y, max_pt.Z),
    XYZ(min_pt.X, max_pt.Y, min_pt.Z),
    XYZ(min_pt.X, max_pt.Y, max_pt.Z),
    XYZ(max_pt.X, min_pt.Y, min_pt.Z),
    XYZ(max_pt.X, min_pt.Y, max_pt.Z),
    XYZ(max_pt.X, max_pt.Y, min_pt.Z),
    XYZ(max_pt.X, max_pt.Y, max_pt.Z),
    ]
    projections = [p.DotProduct(width_direction) for p in points]  
    
    #Ta đổ bóng (chiếu) từng điểm point lên vector vuông góc với dầm và
    #lấy khoảng cách có dấu từ gốc tọa độ đến điểm chiếu. (khoảng cách lúc này rất lớn vì tính từ mốc 0,0,0)
  
    width = max(projections) - min(projections) #Hàm này sẽ triệt tiêu khoảng cách tính từ tọa độ.

    return width

def tinh_chieu_cao_dam(beam):
    # Vector phương thẳng đứng
    height_direction = XYZ.BasisZ  # (0,0,1)

    # Bounding box của dầm
    bbox = beam.get_BoundingBox(None)
    min_pt = bbox.Min
    max_pt = bbox.Max

    # 8 điểm của bounding box
    points = [
        XYZ(min_pt.X, min_pt.Y, min_pt.Z),
        XYZ(min_pt.X, min_pt.Y, max_pt.Z),
        XYZ(min_pt.X, max_pt.Y, min_pt.Z),
        XYZ(min_pt.X, max_pt.Y, max_pt.Z),
        XYZ(max_pt.X, min_pt.Y, min_pt.Z),
        XYZ(max_pt.X, min_pt.Y, max_pt.Z),
        XYZ(max_pt.X, max_pt.Y, min_pt.Z),
        XYZ(max_pt.X, max_pt.Y, max_pt.Z),
    ]

    # Chiếu các điểm lên trục Z
    projections = [p.DotProduct(height_direction) for p in points]

    # Chiều cao = max - min
    height = max(projections) - min(projections)

    return height


def tinh_diem_trung_tam_bounding_box(element):
    bbox = element.get_BoundingBox(None)
    min_pt = bbox.Min
    max_pt = bbox.Max
    trung_diem = (min_pt + max_pt ) /2
    return trung_diem






'''Cần kiểm chứng thêm về code này'''
def get_geometry_to_solid(element):
    options = Options()
    options.ComputeReferences = True
    options.DetailLevel = ViewDetailLevel.Fine  
    curves = CurveArray() #khong can lay curve thi bo qua
    solids = []
    all_geometry =  element.get_Geometry(options)
    for tung_loai_geometry in all_geometry: # Curve
        if isinstance(tung_loai_geometry, Curve):
            curves.Append(tung_loai_geometry)
            continue
        # Solid
        if isinstance(tung_loai_geometry, Solid):
            # loại bỏ solid rỗng
            if tung_loai_geometry.Volume > 0:
                solids.append(tung_loai_geometry)
            continue
        if isinstance(tung_loai_geometry, GeometryInstance):
            # transformed_geometry = tung_loai_geometry.GetInstanceGeometry(tung_loai_geometry.Transform)  #Dong nay khong can dung nua        
            transformed_geometry = tung_loai_geometry.GetInstanceGeometry()    
            for tung_dang_geometry in transformed_geometry:
                # loại bỏ solid rỗng
                if hasattr(tung_dang_geometry, "Volume"):
                    if tung_dang_geometry.Volume > 0:
                        solids.append(tung_dang_geometry)
    return solids #Trả về dạng list các solid

def get_face_from_solid(solid):
    list_faces =[]
    if hasattr(solid, "Faces"):
        for face in solid.Faces:
            if str(type(face)) == "<type 'PlanarFace'>":
                list_faces.append(face)
    return list_faces

'''Cần kiểm chứng thêm về code ở trên'''





def get_all_geometry_of_grids(grid, current_view, DatumExtentType = DatumExtentType.ViewSpecific):
    all_geometry = []
    DatumExtentType = DatumExtentType.ViewSpecific
    try:
        geometry_element = grid.GetCurvesInView(DatumExtentType,current_view)
        all_geometry.append(geometry_element)
    except:
        pass
    return all_geometry