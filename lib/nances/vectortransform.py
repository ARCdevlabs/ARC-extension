# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"

import Autodesk
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
from Autodesk.Revit.UI.Selection import ObjectType
import math


def move_point_along_vector(point, vector, distance):
    new_point = point + vector.Normalize() * distance
    return new_point


def normalize(vector):
    """Hàm để chuẩn hóa một vector."""
    norm = math.sqrt(sum(x ** 2 for x in vector))
    return tuple(x / norm for x in vector)

def dot_product(v1, v2):
    """Hàm để tính tích vô hướng của hai vector."""
    return sum(x * y for x, y in zip(v1, v2))

def cross_product(v1, v2):
    """Hàm để tính tích có hướng của hai vector."""
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    )

def rotate_vector(vector_A, vector_B, angle_degrees):
    """
    Xoay vector_A quanh vector_B một góc tùy chỉnh.

    Args:
    vector_A (tuple): Vector cần xoay.
    vector_B (tuple): Vector trục xoay.
    angle_degrees (float): Góc xoay tính bằng độ.

    Returns:
    tuple: Vector đã được xoay.
    """
    # Chuyển vector thành tuple nếu cần
    if not isinstance(vector_A, tuple):
        vector_A = (vector_A.X, vector_A.Y, vector_A.Z)
    if not isinstance(vector_B, tuple):
        vector_B = (vector_B.X, vector_B.Y, vector_B.Z)

    # Chuẩn hóa vector_B để đảm bảo nó là vector đơn vị
    B = normalize(vector_B)
    
    # Chuyển đổi góc từ độ sang radian
    angle_radians = math.radians(angle_degrees)
    
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)
    
    dot = dot_product(vector_A, B)
    cross = cross_product(B, vector_A)
    
    rotated_vector_list = (
        cos_angle * vector_A[0] + sin_angle * cross[0] + (1 - cos_angle) * dot * B[0],
        cos_angle * vector_A[1] + sin_angle * cross[1] + (1 - cos_angle) * dot * B[1],
        cos_angle * vector_A[2] + sin_angle * cross[2] + (1 - cos_angle) * dot * B[2]
    )

    rotated_vector = DB.XYZ(rotated_vector_list[0],rotated_vector_list[1],rotated_vector_list[2])

    return rotated_vector



def chuan_hoa_vector_mat_cat(vector): #vector tu trai qua phai, tu duoi len tren
    point_start = DB.XYZ(0,0,0)
    point_end = move_point_along_vector(point_start, vector, 1)

    if abs(vector.Z) < abs(vector.Y):
        if point_start.Y < point_end.Y:
            return vector          
        else:
            return - vector
    elif point_start.Z < point_end.Z:
        return vector 
    else: 
        return - vector


def chuan_hoa_vector_mat_bang(vector): #vector tu trai qua phai, tu duoi len tren
    point_start = DB.XYZ(0,0,0)
    point_end = move_point_along_vector(point_start, vector, 1)

    if abs(vector.X) < abs(vector.Y):
        if point_start.Y < point_end.Y:
            return vector          
        else:
            return - vector
    elif point_start.X < point_end.X:
        return vector 
    else: 
        return - vector
    
def move_segment_xa_nhat (list_sorted, vector_cua_dim, kich_co_chu, khoang_cach_dim_toi_text, huong_phai = True):

    seg_xa_nhat= list_sorted[0]

    value_segment = seg_xa_nhat.Value
    
    vi_tri = seg_xa_nhat.Origin

    cong_thuc = ((kich_co_chu/304.8)/2) + ((value_segment)/2) + khoang_cach_dim_toi_text
    if huong_phai:
        move = move_point_along_vector(vi_tri, vector_cua_dim, cong_thuc) #move theo don vi feet
    else:
        move = move_point_along_vector(vi_tri, -vector_cua_dim, cong_thuc) #move theo don vi feet
    
    seg_xa_nhat.TextPosition = move

    return 

def distance_mat_bang(point1, point2):
    return ((point2.X - point1.X)**2 + (point2.Y - point1.Y)**2)**0.5

def distance_mat_cat(point1, point2):
    return ((point2.Z - point1.Z)**2 + (point2.Y - point1.Y)**2)**0.5

def orientation_mat_cat(A, B, vector):
    C = move_point_along_vector(B, vector, 1)
    # Chuyển đổi tọa độ thành tuple
    # Vector AB
    vector_AB = (B.Z - A.Z, B.Y - A.Y)
    # Vector BC
    vector_BC = (C.Z - B.Z, C.Y - B.Y)
    # Tính cross product
    cross_product = vector_AB[0] * vector_BC[1] - vector_AB[1] * vector_BC[0]
    # Xác định hướng dựa trên dấu của cross product
    if cross_product > 0:
        ket_qua = "Bên trái"
    elif cross_product < 0:
        ket_qua = "Bên phải"
    else:
        ket_qua= "Thẳng hàng"        
    return ket_qua


def orientation_mat_bang(A, B, vector):
    C = move_point_along_vector(B, vector, 1)
    # Chuyển đổi tọa độ thành tuple
    # Vector AB
    vector_AB = (B.X - A.X, B.Y - A.Y)
    # Vector BC
    vector_BC = (C.X - B.X, C.Y - B.Y)
    # Tính cross product
    cross_product = vector_AB[0] * vector_BC[1] - vector_AB[1] * vector_BC[0]
    # Xác định hướng dựa trên dấu của cross product
    if cross_product > 0:
        ket_qua = "Bên trái"
    elif cross_product < 0:
        ket_qua = "Bên phải"
    else:
        ket_qua= "Thẳng hàng"        
    return ket_qua



def distance_2_point(point , reference_point):
    distance = point.DistanceTo(reference_point)
    return distance


def get_nearest_point(points, reference_point):

    min_distance = float('inf')
    nearest_point = None
    
    for point in points:
        distance = point.DistanceTo(reference_point)
        if distance < min_distance:
            min_distance = distance
            nearest_point = point
    return nearest_point

def angle_between_planes(plane1, plane2):
    import math
    normal1 = plane1.Normal
    normal2 = plane2.Normal
    dot_product = normal1.DotProduct(normal2)
    magnitude1 = normal1.GetLength()
    magnitude2 = normal2.GetLength()
    
    if magnitude1 == 0 or magnitude2 == 0:
        return None    
    cos_angle = dot_product / (magnitude1 * magnitude2)
    angle_rad = math.acos(cos_angle)
    angle_deg = math.degrees(angle_rad)
    return angle_deg


def degrees_to_radians(degrees):
    import math
    radians = degrees * (math.pi / 180)
    return radians


def distance_from_point_to_plane(point, plane):
    distance = plane.Normal.DotProduct(point - plane.Origin)
    return distance


def distance_between_parallel_planes(plane1, plane2):
    point_on_plane = DB.XYZ(0, 0, 0)
    distance1 = abs(distance_from_point_to_plane(point_on_plane, plane1))
    distance2 = abs(distance_from_point_to_plane(point_on_plane, plane2))
    distance = (distance1 - distance2)
    return distance

def create_plane_follow_line (line):
    start_point = line.GetEndPoint(0)
    end_point = line.GetEndPoint(1)
    mid_point = line.Evaluate(0.5, True)
    offset_mid_point = DB.XYZ(start_point.X, start_point.Y, mid_point.Z +10000)
    point1 = start_point
    point2 = end_point
    point3 =offset_mid_point
    vector1 = point2 - point1
    vector2 = point3 - point1
    normal_vector = vector1.CrossProduct(vector2).Normalize()
    plane = DB.Plane.CreateByNormalAndOrigin(normal_vector, mid_point)
    return plane


def create_plane_from_point_and_normal(point, normal):
    plane = Autodesk.Revit.DB.Plane(normal, point)
    return plane

def are_planes_parallel(normal1, normal2):
    tolerance=0.0000001
    cross_product = normal1.CrossProduct(normal2)
    return cross_product.GetLength() < tolerance

def distance_between_planes(normal1, point_on_plane1, normal2):
    vector_between_planes = point_on_plane1 - (point_on_plane1.DotProduct(normal2) - normal2.DotProduct(normal1)) / normal1.DotProduct(normal2) * normal1
    distance = vector_between_planes.GetLength()
    return distance