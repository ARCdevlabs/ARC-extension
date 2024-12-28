# -*- coding: utf-8 -*-
import Autodesk
import Autodesk.Revit.DB as DB
import math
import clr
clr.AddReference("VectorTransform241227.dll")
import VectorTransform241227 #Load Assembly

# def move_point_along_vector(point, vector, distance):
#     new_point = point + vector.Normalize() * distance
#     return new_point

def move_point_along_vector(point, vector, distance):
    new_point = VectorTransform241227.move_point_along_vector(point, vector, distance)
    return new_point

# def normalize(vector):
#     """Hàm để chuẩn hóa một vector."""
#     norm = math.sqrt(sum(x ** 2 for x in vector))
#     return tuple(x / norm for x in vector)

def normalize(vector):
    norm = VectorTransform241227.normalize(vector)
    return norm

# def dot_product(v1, v2):
#     """Hàm để tính tích vô hướng của hai vector."""
#     return sum(x * y for x, y in zip(v1, v2))

def dot_product(v1, v2):
    """Hàm để tính tích vô hướng của hai vector."""
    tich_vo_huong = VectorTransform241227.dot_product(v1, v2)
    return tich_vo_huong

# def cross_product(v1, v2):
#     """Hàm để tính tích có hướng của hai vector."""
#     return (
#         v1[1] * v2[2] - v1[2] * v2[1],
#         v1[2] * v2[0] - v1[0] * v2[2],
#         v1[0] * v2[1] - v1[1] * v2[0]
#     )

def cross_product(v1, v2):
    """Hàm để tính tích có hướng của hai vector."""
    tich_co_huong = VectorTransform241227.cross_product(v1, v2)
    return tich_co_huong

# def rotate_vector(vector_A, vector_B, angle_degrees):
#     """
#     Xoay vector_A quanh vector_B một góc tùy chỉnh.

#     Args:
#     vector_A (tuple): Vector cần xoay.
#     vector_B (tuple): Vector trục xoay.
#     angle_degrees (float): Góc xoay tính bằng độ.

#     Returns:
#     tuple: Vector đã được xoay.
#     """
#     # Chuyển vector thành tuple nếu cần
#     if not isinstance(vector_A, tuple):
#         vector_A = (vector_A.X, vector_A.Y, vector_A.Z)
#     if not isinstance(vector_B, tuple):
#         vector_B = (vector_B.X, vector_B.Y, vector_B.Z)

#     # Chuẩn hóa vector_B để đảm bảo nó là vector đơn vị
#     B = normalize(vector_B)
    
#     # Chuyển đổi góc từ độ sang radian
#     angle_radians = math.radians(angle_degrees)
    
#     cos_angle = math.cos(angle_radians)
#     sin_angle = math.sin(angle_radians)
    
#     dot = dot_product(vector_A, B)
#     cross = cross_product(B, vector_A)
    
#     rotated_vector_list = (
#         cos_angle * vector_A[0] + sin_angle * cross[0] + (1 - cos_angle) * dot * B[0],
#         cos_angle * vector_A[1] + sin_angle * cross[1] + (1 - cos_angle) * dot * B[1],
#         cos_angle * vector_A[2] + sin_angle * cross[2] + (1 - cos_angle) * dot * B[2]
#     )

#     rotated_vector = DB.XYZ(rotated_vector_list[0],rotated_vector_list[1],rotated_vector_list[2])

#     return rotated_vector

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
    rotated_vector = VectorTransform241227.rotate_vector(vector_A, vector_B, angle_degrees)
    return rotated_vector

'''Biến một vector bất kì thành vector từ dưới lên trên, từ trái qua phải
    Mục đích là để xác định hướng trái và hướng phải của vector'''

# def chuan_hoa_vector(vector, view): #vector tu trai qua phai, tu duoi len tren
#     # view_direction = view.ViewDirection
#     view_updirection = view.UpDirection
#     view_rightdirection = view.RightDirection

#     xac_dinh_goc_voi_vector_right = angle_between_vectors(vector, view_rightdirection)
#     xac_dinh_goc_voi_vector_up = angle_between_vectors(vector, view_updirection)
#     if xac_dinh_goc_voi_vector_right <= 45:
#         if xac_dinh_goc_voi_vector_up <= 135:
#             return vector
#         else: 
#             return -vector
#     elif xac_dinh_goc_voi_vector_right > 45 and xac_dinh_goc_voi_vector_right < 135:
#         if xac_dinh_goc_voi_vector_up <= 45:
#             return vector
#         else:
#             return -vector
#     else:
#         return -vector
    
def chuan_hoa_vector(vector, view): #vector tu trai qua phai, tu duoi len tren
    # view_direction = view.ViewDirection
    return_vector = VectorTransform241227.chuan_hoa_vector(vector, view)
    return return_vector


# '''Cách chuẩn hóa vector mặt bằng, mặt cắt hơi nông dân, hãy dùng hàm 
# chuan_hoa_vector(vector, view)'''

# def chuan_hoa_vector_mat_cat(vector): #vector tu trai qua phai, tu duoi len tren
#     point_start = DB.XYZ(0,0,0)
#     point_end = move_point_along_vector(point_start, vector, 1)

#     if abs(vector.Z) < abs(vector.Y):
#         if point_start.Y < point_end.Y:
#             return vector          
#         else:
#             return - vector
#     elif point_start.Z < point_end.Z:
#         return vector 
#     else: 
#         return - vector

'''Cách chuẩn hóa vector mặt bằng, mặt cắt hơi nông dân, hãy dùng hàm 
chuan_hoa_vector(vector, view)'''

def chuan_hoa_vector_mat_cat(vector): #vector tu trai qua phai, tu duoi len tren
    return_vector = VectorTransform241227.chuan_hoa_vector_mat_cat(vector)
    return return_vector

# def chuan_hoa_vector_mat_bang(vector): #vector tu trai qua phai, tu duoi len tren 
#     point_start = DB.XYZ(0,0,0)
#     point_end = move_point_along_vector(point_start, vector, 1)

#     if abs(vector.X) < abs(vector.Y):
#         if point_start.Y < point_end.Y:
#             return vector          
#         else:
#             return - vector
#     elif point_start.X < point_end.X:
#         return vector 
#     else: 
#         return - vector

def chuan_hoa_vector_mat_bang(vector): #vector tu trai qua phai, tu duoi len tren 
    return_vector = VectorTransform241227.chuan_hoa_vector_mat_bang(vector)
    return return_vector
    
    
# def move_segment_xa_nhat (list_sorted, vector_cua_dim, kich_co_chu, khoang_cach_dim_toi_text, huong_phai = True):

#     seg_xa_nhat= list_sorted[0]

#     value_segment = seg_xa_nhat.Value
    
#     vi_tri = seg_xa_nhat.Origin

#     cong_thuc = ((kich_co_chu/304.8)/2) + ((value_segment)/2) + khoang_cach_dim_toi_text
#     if huong_phai:
#         move = move_point_along_vector(vi_tri, vector_cua_dim, cong_thuc) #move theo don vi feet
#     else:
#         move = move_point_along_vector(vi_tri, -vector_cua_dim, cong_thuc) #move theo don vi feet
    
#     seg_xa_nhat.TextPosition = move

#     return 

def move_segment_xa_nhat (list_sorted, vector_cua_dim, kich_co_chu, khoang_cach_dim_toi_text, huong_phai = True):
    if huong_phai:
        VectorTransform241227.move_segment_xa_nhat(list_sorted, vector_cua_dim, kich_co_chu, khoang_cach_dim_toi_text, huong_phai = True)
    else: 
        VectorTransform241227.move_segment_xa_nhat(list_sorted, vector_cua_dim, kich_co_chu, khoang_cach_dim_toi_text, huong_phai = False)
    return 

def distance_mat_bang(point1, point2):
    return ((point2.X - point1.X)**2 + (point2.Y - point1.Y)**2)**0.5

def distance_mat_cat(point1, point2):
    return ((point2.Z - point1.Z)**2 + (point2.Y - point1.Y)**2)**0.5

# def orientation_mat_cat(A, B, vector):
#     C = move_point_along_vector(B, vector, 1)
#     # Chuyển đổi tọa độ thành tuple
#     # Vector AB
#     vector_AB = (B.Z - A.Z, B.Y - A.Y)
#     # Vector BC
#     vector_BC = (C.Z - B.Z, C.Y - B.Y)
#     # Tính cross product
#     cross_product = vector_AB[0] * vector_BC[1] - vector_AB[1] * vector_BC[0]
#     # Xác định hướng dựa trên dấu của cross product
#     if cross_product > 0:
#         ket_qua = "Bên trái"
#     elif cross_product < 0:
#         ket_qua = "Bên phải"
#     else:
#         ket_qua= "Thẳng hàng"        
#     return ket_qua

def orientation_mat_cat(A, B, vector):
    ket_qua = VectorTransform241227.orientation_mat_cat(A, B, vector)
    return ket_qua

# def orientation_mat_bang(A, B, vector):
#     C = move_point_along_vector(B, vector, 1)
#     # Chuyển đổi tọa độ thành tuple
#     # Vector AB
#     vector_AB = (B.X - A.X, B.Y - A.Y)
#     # Vector BC
#     vector_BC = (C.X - B.X, C.Y - B.Y)
#     # Tính cross product
#     cross_product = vector_AB[0] * vector_BC[1] - vector_AB[1] * vector_BC[0]
#     # Xác định hướng dựa trên dấu của cross product
#     if cross_product > 0:
#         ket_qua = "Bên trái"
#     elif cross_product < 0:
#         ket_qua = "Bên phải"
#     else:
#         ket_qua= "Thẳng hàng"        
#     return ket_qua

def orientation_mat_bang(A, B, vector):
    ket_qua = VectorTransform241227.orientation_mat_bang(A, B, vector)
    return ket_qua

def distance_2_point(point , reference_point):
    distance = point.DistanceTo(reference_point)
    return distance

# def get_nearest_point(points, reference_point):
#     min_distance = float('inf')
#     nearest_point = None
    
#     for point in points:
#         distance = point.DistanceTo(reference_point)
#         if distance < min_distance:
#             min_distance = distance
#             nearest_point = point
#     return nearest_point

def get_nearest_point(points, reference_point):
    nearest_point = get_nearest_point(points, reference_point)
    return nearest_point


# def angle_between_planes(plane1, plane2):
#     import math
#     normal1 = plane1.Normal
#     normal2 = plane2.Normal
#     dot_product = normal1.DotProduct(normal2)
#     magnitude1 = normal1.GetLength()
#     magnitude2 = normal2.GetLength()
    
#     if magnitude1 == 0 or magnitude2 == 0:
#         return None    
#     cos_angle = dot_product / (magnitude1 * magnitude2)
#     angle_rad = math.acos(cos_angle)
#     angle_deg = math.degrees(angle_rad)
#     return angle_deg

def angle_between_planes(plane1, plane2):
    angle_deg = VectorTransform241227.angle_between_planes(plane1, plane2)
    return angle_deg    


def degrees_to_radians(degrees):
    import math
    radians = degrees * (math.pi / 180)
    return radians


def distance_from_point_to_plane(point, plane):
    distance = plane.Normal.DotProduct(point - plane.Origin)
    return distance


# def distance_between_parallel_planes(plane1, plane2):
#     point_on_plane = DB.XYZ(0, 0, 0)
#     distance1 = abs(distance_from_point_to_plane(point_on_plane, plane1))
#     distance2 = abs(distance_from_point_to_plane(point_on_plane, plane2))
#     distance = (distance1 - distance2)
#     return distance

def distance_between_parallel_planes(plane1, plane2):
    distance = VectorTransform241227.distance_between_parallel_planes(plane1, plane2)
    return distance

# def create_plane_follow_line (line):
#     start_point = line.GetEndPoint(0)
#     end_point = line.GetEndPoint(1)
#     mid_point = line.Evaluate(0.5, True)
#     offset_mid_point = DB.XYZ(start_point.X, start_point.Y, mid_point.Z +10000)
#     point1 = start_point
#     point2 = end_point
#     point3 =offset_mid_point
#     vector1 = point2 - point1
#     vector2 = point3 - point1
#     normal_vector = vector1.CrossProduct(vector2).Normalize()
#     plane = DB.Plane.CreateByNormalAndOrigin(normal_vector, mid_point)
#     return plane

def create_plane_follow_line (line):
    plane = VectorTransform241227.create_plane_follow_line (line)
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

# def rotate_vector_around_axis(vector, axis, angle_degrees):
#     """Hàm để xoay một vector quanh một trục cho trước một góc nhất định."""
#     # Chuyển đổi góc từ độ sang radian
#     angle_radians = math.radians(angle_degrees)
    
#     # Chuẩn hóa trục xoay
#     axis = normalize(axis)
    
#     # Các thành phần của trục xoay
#     u = axis.X
#     v = axis.Y
#     w = axis.Z
    
#     # Các thành phần của vector gốc
#     x = vector.X
#     y = vector.Y
#     z = vector.Z
    
#     # Công thức xoay vector quanh trục (rotation matrix)
#     cos_angle = math.cos(angle_radians)
#     sin_angle = math.sin(angle_radians)
#     one_minus_cos = 1 - cos_angle
    
#     # Ma trận xoay
#     rotated_x = (u*u*one_minus_cos + cos_angle)*x + (u*v*one_minus_cos - w*sin_angle)*y + (u*w*one_minus_cos + v*sin_angle)*z
#     rotated_y = (v*u*one_minus_cos + w*sin_angle)*x + (v*v*one_minus_cos + cos_angle)*y + (v*w*one_minus_cos - u*sin_angle)*z
#     rotated_z = (w*u*one_minus_cos - v*sin_angle)*x + (w*v*one_minus_cos + u*sin_angle)*y + (w*w*one_minus_cos + cos_angle)*z
    
#     return DB.XYZ(rotated_x, rotated_y, rotated_z)


def rotate_vector_around_axis(vector, axis, angle_degrees):
    """Hàm để xoay một vector quanh một trục cho trước một góc nhất định."""
    return_XYZ = VectorTransform241227.rotate_vector_around_axis(vector, axis, angle_degrees)   
    return return_XYZ

def angle_between_vectors(vector1, vector2):
    # Tích vô hướng của 2 vector
    dot_prod = vector1.DotProduct(vector2)
    # Tính độ lớn của hai vector
    magnitude1 = vector1.GetLength()
    magnitude2 = vector2.GetLength()
    # Tính cos(theta)
    cos_theta = dot_prod / (magnitude1 * magnitude2)
    # Trả về góc (theo độ)
    goc_theo_do = math.degrees(math.acos(cos_theta))
    return goc_theo_do


# '''Tìm điểm giao nhau giữa một line và một plane (lưu ý là line chứ không phải curve bởi vì curve không có thể cong)
# line_point: là một điểm thuộc line => Chắc là lấy Line.EndPoint(0) được
# line_direction: là vector của line => Line.Direction
# plane_point: là một điểm thuộc plane => Plane.Origin()
# plane_normal: là vector pháp tuyến của plane => Plane.Normalize()
# '''
# def line_plane_intersection(line_point, line_direction, plane_point, plane_normal):
#     # Vector từ điểm trên mặt phẳng đến điểm trên đường thẳng
#     vector_plane_to_line = [
#         line_point[0] - plane_point[0],
#         line_point[1] - plane_point[1],
#         line_point[2] - plane_point[2]
#     ]
    
#     # Tính dot product giữa plane_normal và line_direction
#     dot_product = (
#         plane_normal[0] * line_direction[0] +
#         plane_normal[1] * line_direction[1] +
#         plane_normal[2] * line_direction[2]
#     )
    
#     # Kiểm tra nếu dot_product bằng 0, line và plane là song song, không có giao điểm
#     if dot_product == 0:
#         return None  # Không có giao điểm

#     # Tính toán tham số t cho điểm giao nhau
#     t = -(
#         plane_normal[0] * vector_plane_to_line[0] +
#         plane_normal[1] * vector_plane_to_line[1] +
#         plane_normal[2] * vector_plane_to_line[2]
#     ) / dot_product
    
#     # Tọa độ giao điểm
#     intersection = [
#         line_point[0] + t * line_direction[0],
#         line_point[1] + t * line_direction[1],
#         line_point[2] + t * line_direction[2]
#     ]
#     return_point = DB.XYZ(intersection[0],intersection[1],intersection[2])

#     return return_point

'''Tìm điểm giao nhau giữa một line và một plane (lưu ý là line chứ không phải curve bởi vì curve không có thể cong)
line_point: là một điểm thuộc line => Chắc là lấy Line.EndPoint(0) được
line_direction: là vector của line => Line.Direction
plane_point: là một điểm thuộc plane => Plane.Origin()
plane_normal: là vector pháp tuyến của plane => Plane.Normalize()
'''
def line_plane_intersection(line_point, line_direction, plane_point, plane_normal):
    # Vector từ điểm trên mặt phẳng đến điểm trên đường thẳng
    return_point = VectorTransform241227.line_plane_intersection(line_point, line_direction, plane_point, plane_normal)
    return return_point

# '''Cho 2 điểm start point, end point và một điểm bất kỳ A, tìm xem điểm start point và end point điểm nào gần điểm A hơn'''
# def nearest_point(point_goc, point_muc_tieu_1, point_muc_tieu_2):
#     string_1 = "StartPoint"
#     string_2 = "EndPoint"
#     distance_1 = distance_2_point(point_goc,point_muc_tieu_1)
#     distance_2 = distance_2_point(point_goc,point_muc_tieu_2)
#     if distance_1 < distance_2:
#         return string_1
#     elif distance_1 > distance_2:
#         return string_2

'''Cho 2 điểm start point, end point và một điểm bất kỳ A, tìm xem điểm start point và end point điểm nào gần điểm A hơn'''
def nearest_point(point_goc, point_muc_tieu_1, point_muc_tieu_2):
    ket_qua = VectorTransform241227.nearest_point(point_goc, point_muc_tieu_1, point_muc_tieu_2)
    return ket_qua
    
# '''Transform giống như một vector, có thể lấy bằng cách element.GetTransform() hoặc element.GetTotalTransform(), 
# (chưa tìm hiểu sự khác nhau giữa 2 phương thức)
# Cách dịch chuyển một line là hãy dịch chuyển 2 point của 2 đầu của Line ban đầu => tạo lại Line mới là được '''
# def transform_line(transform, line):
#     start_point = line.GetEndPoint(0)  # Điểm đầu của Line
#     end_point = line.GetEndPoint(1)    # Điểm cuối của Line
#     # Áp dụng Transform cho cả điểm đầu và điểm cuối
#     new_start_point = transform.OfPoint(start_point)
#     new_end_point = transform.OfPoint(end_point)
#     # Tạo Line mới từ các điểm đã dịch chuyển
#     transformed_line = DB.Line.CreateBound(new_start_point, new_end_point)
#     return transformed_line

'''Transform giống như một vector, có thể lấy bằng cách element.GetTransform() hoặc element.GetTotalTransform(), 
(chưa tìm hiểu sự khác nhau giữa 2 phương thức)
Cách dịch chuyển một line là hãy dịch chuyển 2 point của 2 đầu của Line ban đầu => tạo lại Line mới là được '''
def transform_line(transform, line):
    transformed_line = VectorTransform241227.transform_line(transform, line)
    return transformed_line

def distance_point_to_plane(point, plane):
    distance = plane.Normal.DotProduct(point - plane.Origin)
    return distance