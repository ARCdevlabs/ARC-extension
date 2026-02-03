# -*- coding: utf-8 -*-
import Autodesk
import Autodesk.Revit.DB as DB
import math
import importdll
import_class = importdll.ImportDLL()
import_def = import_class.get_dll()


def move_point_along_vector(point, vector, distance):
    try:
        new_point = import_def.LibARC_VectorMath.MovePointAlongVector(point, vector, distance)
        return new_point
    except:
        pass
        return

def normalize(vector): #thuần toán học
    """Hàm để chuẩn hóa một vector."""
    norm = math.sqrt(sum(x ** 2 for x in vector))
    return tuple(x / norm for x in vector)

def normalize_revit(vector): #trả về vector trong Revit
    """Hàm để chuẩn hóa một vector."""
    norm = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
    return DB.XYZ(vector[0] / norm, vector[1] / norm, vector[2] / norm)

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



'''Biến một vector bất kì thành vector từ dưới lên trên, từ trái qua phải
    Mục đích là để xác định hướng trái và hướng phải của vector'''
def chuan_hoa_vector(vector, view): #vector tu trai qua phai, tu duoi len tren
    # view_direction = view.ViewDirection
    view_updirection = view.UpDirection
    view_rightdirection = view.RightDirection

    xac_dinh_goc_voi_vector_right = angle_between_vectors(vector, view_rightdirection)
    xac_dinh_goc_voi_vector_up = angle_between_vectors(vector, view_updirection)
    if xac_dinh_goc_voi_vector_right <= 45:
        if xac_dinh_goc_voi_vector_up <= 135:
            return vector
        else: 
            return -vector
    elif xac_dinh_goc_voi_vector_right > 45 and xac_dinh_goc_voi_vector_right < 135:
        if xac_dinh_goc_voi_vector_up <= 45:
            return vector
        else:
            return -vector
    else:
        return -vector
    
def chuan_hoa_vector_tu_trai_qua_phai_duoi_len_tren (vector, view): #vector tu trai qua phai, tu tren xuong duoi
    # view_direction = view.ViewDirection
    view_updirection = view.UpDirection
    view_rightdirection = view.RightDirection

    xac_dinh_goc_voi_vector_right = angle_between_vectors(vector, view_rightdirection)
    xac_dinh_goc_voi_vector_up = angle_between_vectors(vector, view_updirection)
    if xac_dinh_goc_voi_vector_right <= 45:
        if xac_dinh_goc_voi_vector_up <= 135:
            return vector
        else: 
            return -vector
    elif xac_dinh_goc_voi_vector_right > 45 and xac_dinh_goc_voi_vector_right < 135:
        if xac_dinh_goc_voi_vector_up <= 45:
            return -vector
        else:
            return vector
    else:
        return -vector    
    
'''Cách chuẩn hóa vector mặt bằng, mặt cắt hơi nông dân, hãy dùng hàm 
chuan_hoa_vector(vector, view)'''

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
    distance = import_def.LibARC_VectorMath.DistanceFromPointToPlane(point, plane)
    return distance

def distance_between_parallel_planes(plane1, plane2):
    point_on_plane = DB.XYZ(-54321, -54321, 0)
    distance1 = abs(distance_from_point_to_plane(point_on_plane, plane1))
    distance2 = abs(distance_from_point_to_plane(point_on_plane, plane2))
    distance = (distance1 - distance2)
    return distance

def create_plane_follow_line (line): #Chỉ tạo plane song song với mặt phẳng Z = 0
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

def create_plane_follow_line_in_view (line,view):
    start_point = line.GetEndPoint(0)
    end_point = line.GetEndPoint(1)
    mid_point = line.Evaluate(0.5, True)
    view_direction = view.ViewDirection
    offset_mid_point = move_point_along_vector(mid_point,view_direction,1)
    point1 = start_point
    point2 = end_point
    point3 =offset_mid_point
    vector1 = point2 - point1
    vector2 = point3 - point1
    normal_vector = vector1.CrossProduct(vector2).Normalize()
    plane = DB.Plane.CreateByNormalAndOrigin(normal_vector, mid_point)
    return plane

def create_plane_from_point_and_normal(point, normal): #Đây là mặt phẳng của Autodesk
    plane = DB.Plane.CreateByNormalAndOrigin(normal, point)
    return plane


def are_planes_parallel(normal1, normal2):
    return import_def.LibARC_VectorMath.ArePlanesParallel(normal1, normal2)

def distance_between_planes(normal1, point_on_plane1, normal2):
    vector_between_planes = point_on_plane1 - (point_on_plane1.DotProduct(normal2) - normal2.DotProduct(normal1)) / normal1.DotProduct(normal2) * normal1
    distance = vector_between_planes.GetLength()
    return distance

def rotate_vector_around_axis(vector, axis, angle_degrees): #vector đầu vào là vector toán học
    import math
    """Hàm để xoay một vector quanh một trục cho trước một góc nhất định."""
    # Chuyển đổi góc từ độ sang radian
    angle_radians = math.radians(angle_degrees)
    
    # Chuẩn hóa trục xoay
    axis = normalize(axis)
    
    # Các thành phần của trục xoay
    u = axis.X
    v = axis.Y
    w = axis.Z
    
    # Các thành phần của vector gốc
    x = vector.X
    y = vector.Y
    z = vector.Z
    
    # Công thức xoay vector quanh trục (rotation matrix)
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)
    one_minus_cos = 1 - cos_angle
    
    # Ma trận xoay
    rotated_x = (u*u*one_minus_cos + cos_angle)*x + (u*v*one_minus_cos - w*sin_angle)*y + (u*w*one_minus_cos + v*sin_angle)*z
    rotated_y = (v*u*one_minus_cos + w*sin_angle)*x + (v*v*one_minus_cos + cos_angle)*y + (v*w*one_minus_cos - u*sin_angle)*z
    rotated_z = (w*u*one_minus_cos - v*sin_angle)*x + (w*v*one_minus_cos + u*sin_angle)*y + (w*w*one_minus_cos + cos_angle)*z
    
    return DB.XYZ(rotated_x, rotated_y, rotated_z)

def rotate_vector_around_axis_revit(vector_revit, axis, angle_degrees): #vector đầu vào là vector revit
    import math
    """Hàm để xoay một vector quanh một trục cho trước một góc nhất định."""
    # Chuyển đổi góc từ độ sang radian
    angle_radians = math.radians(angle_degrees)
    
    # Chuẩn hóa trục xoay
    axis = normalize_revit(axis)
    
    # Các thành phần của trục xoay
    u = axis.X
    v = axis.Y
    w = axis.Z
    
    # Các thành phần của vector gốc
    x = vector_revit.X
    y = vector_revit.Y
    z = vector_revit.Z
    
    # Công thức xoay vector quanh trục (rotation matrix)
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)
    one_minus_cos = 1 - cos_angle
    
    # Ma trận xoay
    rotated_x = (u*u*one_minus_cos + cos_angle)*x + (u*v*one_minus_cos - w*sin_angle)*y + (u*w*one_minus_cos + v*sin_angle)*z
    rotated_y = (v*u*one_minus_cos + w*sin_angle)*x + (v*v*one_minus_cos + cos_angle)*y + (v*w*one_minus_cos - u*sin_angle)*z
    rotated_z = (w*u*one_minus_cos - v*sin_angle)*x + (w*v*one_minus_cos + u*sin_angle)*y + (w*w*one_minus_cos + cos_angle)*z
    
    return DB.XYZ(rotated_x, rotated_y, rotated_z)

def angle_between_vectors(vector1, vector2): #góc cũng phụ thuộc vào hướng của vector
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

'''Tìm điểm giao nhau giữa một line và một plane (lưu ý là line chứ không phải curve bởi vì curve không có thể cong)
line_point: là một điểm thuộc line => Chắc là lấy Line.EndPoint(0) được
line_direction: là vector của line => Line.Direction
plane_point: là một điểm thuộc plane => Plane.Origin()
plane_normal: là vector pháp tuyến của plane => Plane.Normalize()
'''
def line_plane_intersection(line_point, line_direction, plane_point, plane_normal):
    # Vector từ điểm trên mặt phẳng đến điểm trên đường thẳng
    vector_plane_to_line = [
        line_point[0] - plane_point[0],
        line_point[1] - plane_point[1],
        line_point[2] - plane_point[2]
    ]
    
    # Tính dot product giữa plane_normal và line_direction
    dot_product = (
        plane_normal[0] * line_direction[0] +
        plane_normal[1] * line_direction[1] +
        plane_normal[2] * line_direction[2]
    )
    
    # Kiểm tra nếu dot_product bằng 0, line và plane là song song, không có giao điểm
    if dot_product == 0:
        return None  # Không có giao điểm

    # Tính toán tham số t cho điểm giao nhau
    t = -(
        plane_normal[0] * vector_plane_to_line[0] +
        plane_normal[1] * vector_plane_to_line[1] +
        plane_normal[2] * vector_plane_to_line[2]
    ) / dot_product
    
    # Tọa độ giao điểm
    intersection = [
        line_point[0] + t * line_direction[0],
        line_point[1] + t * line_direction[1],
        line_point[2] + t * line_direction[2]
    ]
    return_point = DB.XYZ(intersection[0],intersection[1],intersection[2])

    return return_point

'''Cho 2 điểm start point, end point và một điểm bất kỳ A, tìm xem điểm start point và end point điểm nào gần điểm A hơn'''
def nearest_point(point_goc, point_muc_tieu_1, point_muc_tieu_2):
    string_1 = "StartPoint"
    string_2 = "EndPoint"
    distance_1 = distance_2_point(point_goc,point_muc_tieu_1)
    distance_2 = distance_2_point(point_goc,point_muc_tieu_2)
    if distance_1 < distance_2:
        return string_1
    elif distance_1 > distance_2:
        return string_2
    
'''Transform giống như một vector, có thể lấy bằng cách element.GetTransform() hoặc element.GetTotalTransform(), 
(chưa tìm hiểu sự khác nhau giữa 2 phương thức)
Cách dịch chuyển một line là hãy dịch chuyển 2 point của 2 đầu của Line ban đầu => tạo lại Line mới là được '''
def transform_line(transform, line):
    start_point = line.GetEndPoint(0)  # Điểm đầu của Line
    end_point = line.GetEndPoint(1)    # Điểm cuối của Line
    # Áp dụng Transform cho cả điểm đầu và điểm cuối
    new_start_point = transform.OfPoint(start_point)
    new_end_point = transform.OfPoint(end_point)
    # Tạo Line mới từ các điểm đã dịch chuyển
    transformed_line = DB.Line.CreateBound(new_start_point, new_end_point)
    return transformed_line

def distance_point_to_plane(point, plane):
    distance = plane.Normal.DotProduct(point - plane.Origin)
    return distance

def co_phai_phuong_ngang_tuyet_doi(line,view):
    right = view.RightDirection.Normalize()
    up = view.UpDirection.Normalize()

    dir_line = line.Direction.Normalize()

    # độ song song
    dot_right = abs(dir_line.DotProduct(right))
    dot_up = abs(dir_line.DotProduct(up))

    TOL = 0.99  # ngưỡng song song

    if dot_right > TOL:
        result = True
    elif dot_up > TOL:
        result = False
    else:
        result = "không ngang / dọc rõ ràng"
    return result

def co_phai_phuong_ngang_dai_khai(line, view): #tính là phương ngang nếu góc từ -45~45 và từ 135~225
    right = view.RightDirection.Normalize()
    up = view.UpDirection.Normalize()

    dir_line = line.Direction.Normalize()

    # tọa độ của vector line trong hệ view
    x = dir_line.DotProduct(right)
    y = dir_line.DotProduct(up)

    # góc có hướng (độ), range: (-180, 180]
    angle = math.degrees(math.atan2(y, x))

    # phương ngang nếu trong các khoảng này
    if (-45.0 <= angle <= 45.0) or (angle >= 135.0 or angle <= -135.0):
        return True
    else:
        return False
    
def project_point_to_plane_by_view(point, plane, view):
    #Gióng point lên plane theo hướng NGƯỢC ViewDirection
    P = point
    D = -view.ViewDirection.Normalize()   # hướng gióng

    P0 = plane.Origin
    N = plane.Normal.Normalize()

    denom = D.DotProduct(N)
    if abs(denom) < 1e-9:
        return None  # song song → không cắt plane

    t = (P0 - P).DotProduct(N) / denom
    projected_point = P + D.Multiply(t)

    return projected_point

def rotate_line_around_view_direction(line, view, angle_deg):
    """
    Xoay line quanh ViewDirection một góc angle_deg (độ)
    """
    # điểm xoay (lấy midpoint)
    P = (line.GetEndPoint(0) + line.GetEndPoint(1)) / 2

    # trục xoay
    axis_dir = view.ViewDirection.Normalize()
    axis = DB.Line.CreateUnbound(P, axis_dir)

    # transform xoay
    angle_rad = math.radians(angle_deg)
    transform = DB.Transform.CreateRotationAtPoint(axis_dir, angle_rad, P)

    # line mới sau khi xoay
    new_line = line.CreateTransformed(transform)

    return new_line

def tao_plane_man_hinh (view):
    origin = view.Origin
    vector_direction = view.ViewDirection
    plane_man_hinh = create_plane_from_point_and_normal(origin,vector_direction)
    return plane_man_hinh

def project_line_to_plane (line, view): #mục đích tạo 1 line phẳng trên view màn hình
    view_direction = view.ViewDirection
    start = line.GetEndPoint(0)
    end = line.GetEndPoint(1)
    plane_man_hinh = create_plane_from_point_and_normal(start,view_direction)
    flat_start = project_point_to_plane_by_view(start,plane_man_hinh,view)
    flat_end = project_point_to_plane_by_view(end,plane_man_hinh,view)
    flat_line =  DB.Line.CreateBound(flat_start,flat_end)
    return flat_line

def get_rotate_90_location_line(line, view):
    start = line.GetEndPoint(0)
    end = line.GetEndPoint(1)
    view_direction = view.ViewDirection
    plane_man_hinh = create_plane_from_point_and_normal(start,view_direction) #mặt phẳng đại diện cho màn hình.
    flat_start = project_point_to_plane_by_view(start,plane_man_hinh,view)
    flat_end = project_point_to_plane_by_view(end,plane_man_hinh,view)
    flat_line =  DB.Line.CreateBound(flat_start,flat_end)
    rotate_line = rotate_line_around_view_direction(flat_line, view, 90)
    return rotate_line


def get_center_plane (wall):
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

def move_line_theo_vector_theo_ty_le_view(vector_de_move_line, line, snap_dim, view):
    start = line.GetEndPoint(0)
    end = line.GetEndPoint(1)
    view_scale = view.Scale
    khoang_cach_move = snap_dim * view_scale #khoang cach tren ty le 1:1 (don vi feet) VD: 5/ 304.8
    move_start_point = move_point_along_vector(start, vector_de_move_line, khoang_cach_move)
    move_end_point = move_point_along_vector(end, vector_de_move_line, khoang_cach_move)
    new_line = DB.Line.CreateBound(move_start_point, move_end_point)
    return new_line

def move_line_theo_vector(vector_de_move_line, line, distance): 
    start_point = line.GetEndPoint(0)
    end_point = line.GetEndPoint(1)
    new_start_point = move_point_along_vector(start_point,vector_de_move_line ,distance)
    new_end_point = move_point_along_vector(end_point, vector_de_move_line,distance)
    new_line= DB.Line.CreateBound(new_start_point,new_end_point)
    return new_line

def get_Y_vector(column):
    Y_orient = column.FacingOrientation
    return Y_orient

def get_X_vector(column):
    X_orient = column.HandOrientation
    return X_orient

def line_for_dim_Y (column,view):
    point = column.Location.Point
    Y_vector = get_Y_vector(column)
    vector_chuan_hoa = chuan_hoa_vector_tu_trai_qua_phai_duoi_len_tren(Y_vector,view)
    point_Y_2 = move_point_along_vector(point,vector_chuan_hoa,1)
    line_Y = DB.Line.CreateBound(point,point_Y_2)
    return line_Y

def line_for_dim_X (column,view):
    point = column.Location.Point
    X_vector =get_X_vector(column)
    vector_chuan_hoa = chuan_hoa_vector_tu_trai_qua_phai_duoi_len_tren(X_vector,view)
    point_X_2 = move_point_along_vector(point,vector_chuan_hoa,1)
    line_X = DB.Line.CreateBound(point,point_X_2)
    return line_X

def tinh_toan_line_dim_cot_1_2_3 (line_ngay_tam_cot, vector ,nua_chieu_rong_cot, view):

    view_scale = view.Scale

    khoang_cach_dim_3 = (9 / 304.8)

    snap_dim =  (5 / 304.8)

    tinh_toan_dim_3 = nua_chieu_rong_cot/view_scale + (khoang_cach_dim_3)

    tinh_toan_dim_2 = nua_chieu_rong_cot/view_scale + (khoang_cach_dim_3 + snap_dim)

    tinh_toan_dim_1 = nua_chieu_rong_cot/view_scale + (khoang_cach_dim_3 + snap_dim + snap_dim)

    line_dim_3 = move_line_theo_vector_theo_ty_le_view(vector, line_ngay_tam_cot, tinh_toan_dim_3, view)

    line_dim_2 = move_line_theo_vector_theo_ty_le_view(vector, line_ngay_tam_cot, tinh_toan_dim_2, view)

    line_dim_1 = move_line_theo_vector_theo_ty_le_view(vector, line_ngay_tam_cot, tinh_toan_dim_1, view)

    return line_dim_3,line_dim_2,line_dim_1