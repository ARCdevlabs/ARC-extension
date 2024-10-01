# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
import math
if module.AutodeskData():
    def normalize(vector):
        """Hàm để chuẩn hóa một vector."""
        norm = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
        return XYZ(vector[0] / norm, vector[1] / norm, vector[2] / norm)

    def rotate_vector_around_axis(vector, axis, angle_degrees):
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
        
        return XYZ(rotated_x, rotated_y, rotated_z)


    def move_dim_segment_ben_trong (list_sorted,segment, vector_cua_dim, kich_co_chu, khoang_cach_dim_toi_text, huong_phai = True):
        total_value = 0
        for i in list_sorted:
            total_value = total_value + i.Value #don vi feet

        value_segment = segment.Value
        
        vi_tri = segment.Origin

        cong_thuc = total_value - (value_segment)/2 + (kich_co_chu/304.8)/2 + khoang_cach_dim_toi_text
        
        if huong_phai:
            move = module.move_point_along_vector(vi_tri, vector_cua_dim, cong_thuc) #move theo don vi feet
        else:
            move = module.move_point_along_vector(vi_tri, - vector_cua_dim, cong_thuc) #move theo don vi feet
        
        segment.TextPosition = move
        return 


    def move_dim_segment_ben_ngoai (segment, kich_co_chu_1, vector_cua_dim, kich_co_chu_0, khoang_cach_dim_toi_text, huong_phai = True):

        value_segment = segment.Value
        
        vi_tri = segment.Origin

        cong_thuc = (value_segment)/2 + (kich_co_chu_0/304.8)/2 + 2* khoang_cach_dim_toi_text + kich_co_chu_1/304.8
        
        if huong_phai:
            move = module.move_point_along_vector(vi_tri, vector_cua_dim, cong_thuc) #move theo don vi feet
        else:
            move = module.move_point_along_vector(vi_tri, -vector_cua_dim, cong_thuc) #move theo don vi feet
        
        segment.TextPosition = move
        return 

    def move_dim_segment_ben_trong_xuong_duoi (
                                                segment,
                                                kich_co_chu_trong,
                                                kich_co_chu_ngoai,
                                                vi_tri_text_ben_ngoai,
                                                vector_cua_dim ,
                                                vector_vuong_goc,
                                                text_size,
                                                khoang_cach_dim_toi_text,
                                                huong_phai = True):
        
        cong_thuc_move_xuong_duoi = -(khoang_cach_dim_toi_text + text_size)
        cong_thuc_move_qua_phai = (kich_co_chu_trong - kich_co_chu_ngoai)/304.8/2

        if huong_phai:
            move_len_tren = module.move_point_along_vector(vi_tri_text_ben_ngoai, vector_vuong_goc, cong_thuc_move_xuong_duoi) #move theo don vi feet
            move_qua_phai = module.move_point_along_vector(move_len_tren,vector_cua_dim, cong_thuc_move_qua_phai )
        else:
            move_len_tren = module.move_point_along_vector(vi_tri_text_ben_ngoai, vector_vuong_goc, cong_thuc_move_xuong_duoi) #move theo don vi feet
            move_qua_phai = module.move_point_along_vector(move_len_tren,- vector_cua_dim, cong_thuc_move_qua_phai )
        
        segment.TextPosition = move_qua_phai # Thực hiện hành động move

        return 

    def move_dim_segment_ben_trong_len_tren (
                                            segment,
                                            kich_co_chu_trong,
                                            kich_co_chu_ngoai,
                                            vi_tri_text_ben_ngoai,
                                            vector_cua_dim ,
                                            vector_vuong_goc,
                                            text_size,
                                            khoang_cach_dim_toi_text,
                                            huong_phai = True):
    
        cong_thuc_move_len_tren = (khoang_cach_dim_toi_text + text_size)
        cong_thuc_move_qua_phai = (kich_co_chu_trong - kich_co_chu_ngoai)/304.8/2

        if huong_phai:
            move_len_tren = module.move_point_along_vector(vi_tri_text_ben_ngoai, vector_vuong_goc, cong_thuc_move_len_tren) #move theo don vi feet
            move_qua_phai = module.move_point_along_vector(move_len_tren,vector_cua_dim, cong_thuc_move_qua_phai )
        else:
            move_len_tren = module.move_point_along_vector(vi_tri_text_ben_ngoai, vector_vuong_goc, cong_thuc_move_len_tren) #move theo don vi feet
            move_qua_phai = module.move_point_along_vector(move_len_tren,- vector_cua_dim, cong_thuc_move_qua_phai )
        
        segment.TextPosition = move_qua_phai # Thực hiện hành động move

        return 

    '''Đây là cách để tính góc giữa 2 vector
        Góc 2 vector = Tích vô hướng của 2 vector
        chia cho tích độ lớn 2 vector'''
    # Hàm tính góc giữa hai vector
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


    def distance(point1, point2):
        return ((point2.X - point1.X)**2 + (point2.Y - point1.Y)**2)**0.5

    def distance_from_point_to_element(point1, obj):
        return distance(point1, obj.Origin)


    '''Xác định hướng của từng segment so với vector vuông góc với nó
    Điểm A là vị trí của segment, điểm B là điểm click vào màn hình'''
    def xac_dinh_phia(A, B, vector_giua_2_diem,view_direction):
        vector_AB = XYZ(B.X - A.X, B.Y - A.Y, B.Z - A.Z)
        cross_product = vector_AB.CrossProduct(vector_giua_2_diem)
        # Xác định hướng dựa trên dấu của cross product
        '''Kiểm tra tích vô hướng của 2 vector 
        (dotproduct của vector tích có hướng và view direction
        Nếu 2 vector này cùng hướng thì dotproduct > 0, dotproduct < 0 thì ngược hướng,
        còn != 0 thì không song song với nhau '''
        dot_prod = view_direction.DotProduct(cross_product)
        if dot_prod > 0: 
            ket_qua = "Bên trái"
        elif dot_prod < 0:
            ket_qua = "Bên phải"
        else:
            ket_qua= "Thẳng hàng"        
        return ket_qua


    def sort_seg_by_distance(A, seg_list):
        # Sắp xếp các điểm trong list dựa trên khoảng cách từ xa đến gần điểm A
        sorted_points = sorted(seg_list, key=lambda obj: distance_from_point_to_element(A, obj), reverse=True)

        return sorted_points
