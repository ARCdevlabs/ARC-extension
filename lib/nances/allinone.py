# -*- coding: utf-8 -*-
import nances
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
import math
from nances import geometry,vectortransform,selection
if nances.AutodeskData():

    def move_dim_segment_ben_trong (list_sorted,segment, vector_cua_dim, kich_co_chu, khoang_cach_dim_toi_text, huong_phai = True):
        total_value = 0
        for i in list_sorted:
            total_value = total_value + i.Value #don vi feet

        value_segment = segment.Value
        
        vi_tri = segment.Origin

        cong_thuc = total_value - (value_segment)/2 + (kich_co_chu/304.8)/2 + khoang_cach_dim_toi_text
        
        if huong_phai:
            move = nances.move_point_along_vector(vi_tri, vector_cua_dim, cong_thuc) #move theo don vi feet
        else:
            move = nances.move_point_along_vector(vi_tri, - vector_cua_dim, cong_thuc) #move theo don vi feet
        
        segment.TextPosition = move
        return 


    def move_dim_segment_ben_ngoai (segment, kich_co_chu_1, vector_cua_dim, kich_co_chu_0, khoang_cach_dim_toi_text, huong_phai = True):

        value_segment = segment.Value
        
        vi_tri = segment.Origin

        cong_thuc = (value_segment)/2 + (kich_co_chu_0/304.8)/2 + 2* khoang_cach_dim_toi_text + kich_co_chu_1/304.8
        
        if huong_phai:
            move = nances.move_point_along_vector(vi_tri, vector_cua_dim, cong_thuc) #move theo don vi feet
        else:
            move = nances.move_point_along_vector(vi_tri, -vector_cua_dim, cong_thuc) #move theo don vi feet
        
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
            move_len_tren = nances.move_point_along_vector(vi_tri_text_ben_ngoai, vector_vuong_goc, cong_thuc_move_xuong_duoi) #move theo don vi feet
            move_qua_phai = nances.move_point_along_vector(move_len_tren,vector_cua_dim, cong_thuc_move_qua_phai )
        else:
            move_len_tren = nances.move_point_along_vector(vi_tri_text_ben_ngoai, vector_vuong_goc, cong_thuc_move_xuong_duoi) #move theo don vi feet
            move_qua_phai = nances.move_point_along_vector(move_len_tren,- vector_cua_dim, cong_thuc_move_qua_phai )
        
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
            move_len_tren = nances.move_point_along_vector(vi_tri_text_ben_ngoai, vector_vuong_goc, cong_thuc_move_len_tren) #move theo don vi feet
            move_qua_phai = nances.move_point_along_vector(move_len_tren,vector_cua_dim, cong_thuc_move_qua_phai )
        else:
            move_len_tren = nances.move_point_along_vector(vi_tri_text_ben_ngoai, vector_vuong_goc, cong_thuc_move_len_tren) #move theo don vi feet
            move_qua_phai = nances.move_point_along_vector(move_len_tren,- vector_cua_dim, cong_thuc_move_qua_phai )
        
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


    def get_average_point(point_list):
        if not point_list:
            return None
        
        total_x = 0
        total_y = 0
        total_z = 0
        count = len(point_list)
        
        for point in point_list:
            total_x += point.X
            total_y += point.Y
            total_z += point.Z
            
        return XYZ(total_x/count, total_y/count, total_z/count)
    
    def get_all_segment_position (dimension):
        all_segment_position = []
        number_of_segments =  dimension.NumberOfSegments
        if number_of_segments != 0:
            segments = dimension.Segments
            for seg in segments:
                text_ori = seg.Origin
                all_segment_position.append(text_ori)
        return all_segment_position
    

    def set_work_plane(uidoc,doc):
        import nances
        t0 = Transaction(doc,"Set Work Plane")
        t0.Start()        
        current_view = uidoc.ActiveView
        try:
            nances.set_work_plane_for_view (current_view)
        except:
            pass
        t0.Commit() 




    def move_text_dim (dim, view, leader_dim = False):
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
            one_unit_width = 2 #Chieu rong 1 don vi text
            width_text_1 = float(len_formatted_value_1 * one_unit_width * (view.Scale))
            width_text_2 = float(len_formatted_value_2 * one_unit_width * (view.Scale))
            khoang_cach_tu_dim = 1.5 * (view.Scale)
            if seg_1_value < width_text_1: 
                width_offset_text_1 = (seg_1_value/2 + khoang_cach_tu_dim + width_text_1/2 ) 
            else:
                width_offset_text_1 = 0
            
            if seg_2_value < width_text_2: 
                width_offset_text_2 = (seg_2_value/2 + khoang_cach_tu_dim + width_text_2/2 )
            else:
                width_offset_text_2 = 0

            move_seg_1 = vectortransform.move_point_along_vector(seg_1_position,curve_dim_direction, - (width_offset_text_1/304.8))
            move_seg_2 = vectortransform.move_point_along_vector(seg_2_position,curve_dim_direction, (width_offset_text_2/304.8))
            dim.Segments.Item[0].TextPosition = move_seg_1
            dim.Segments.Item[1].TextPosition = move_seg_2
            leader_dim_param = dim.get_Parameter(BuiltInParameter.DIM_LEADER)
            leader_dim_param.Set(leader_dim)