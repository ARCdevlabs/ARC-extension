# -*- coding: utf-8 -*-
__doc__ = 'nguyenthanhson1712@gmail.com'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
import math
import traceback
import movetextdim
if module.AutodeskData():
	uidoc = __revit__.ActiveUIDocument
	doc = uidoc.Document

from Autodesk.Revit.UI.Selection import ObjectType, Selection

try:
    import width_of_text_of_dim_config
    source_width_of_text_of_dim = width_of_text_of_dim_config.load_configs()
    out_put = float(source_width_of_text_of_dim[0][0])
except:
    # print (traceback.format_exc())
    out_put = 1.8


# def normalize(vector):
#     """Hàm để chuẩn hóa một vector."""
#     norm = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
#     return XYZ(vector[0] / norm, vector[1] / norm, vector[2] / norm)

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
    
#     return XYZ(rotated_x, rotated_y, rotated_z)


# def move_dim_segment_ben_trong (list_sorted,segment, vector_cua_dim, kich_co_chu, khoang_cach_dim_toi_text, huong_phai = True):
#     total_value = 0
#     for i in list_sorted:
#         total_value = total_value + i.Value #don vi feet

#     value_segment = segment.Value
    
#     vi_tri = segment.Origin

#     cong_thuc = total_value - (value_segment)/2 + (kich_co_chu/304.8)/2 + khoang_cach_dim_toi_text
    
#     if huong_phai:
#         move = module.move_point_along_vector(vi_tri, vector_cua_dim, cong_thuc) #move theo don vi feet
#     else:
#         move = module.move_point_along_vector(vi_tri, - vector_cua_dim, cong_thuc) #move theo don vi feet
    
#     segment.TextPosition = move
#     return 


# def move_dim_segment_ben_ngoai (segment, kich_co_chu_1, vector_cua_dim, kich_co_chu_0, khoang_cach_dim_toi_text, huong_phai = True):

#     value_segment = segment.Value
    
#     vi_tri = segment.Origin

#     cong_thuc = (value_segment)/2 + (kich_co_chu_0/304.8)/2 + 2* khoang_cach_dim_toi_text + kich_co_chu_1/304.8
    
#     if huong_phai:
#         move = module.move_point_along_vector(vi_tri, vector_cua_dim, cong_thuc) #move theo don vi feet
#     else:
#         move = module.move_point_along_vector(vi_tri, -vector_cua_dim, cong_thuc) #move theo don vi feet
    
#     segment.TextPosition = move
#     return 

# def move_dim_segment_ben_trong_xuong_duoi (
#                                             segment,
#                                             kich_co_chu_trong,
#                                             kich_co_chu_ngoai,
#                                             vi_tri_text_ben_ngoai,
#                                             vector_cua_dim ,
#                                             vector_vuong_goc,
#                                             text_size,
#                                             khoang_cach_dim_toi_text,
#                                             huong_phai = True):
    
#     cong_thuc_move_xuong_duoi = -(khoang_cach_dim_toi_text + text_size)
#     cong_thuc_move_qua_phai = (kich_co_chu_trong - kich_co_chu_ngoai)/304.8/2

#     if huong_phai:
#         move_len_tren = module.move_point_along_vector(vi_tri_text_ben_ngoai, vector_vuong_goc, cong_thuc_move_xuong_duoi) #move theo don vi feet
#         move_qua_phai = module.move_point_along_vector(move_len_tren,vector_cua_dim, cong_thuc_move_qua_phai )
#     else:
#         move_len_tren = module.move_point_along_vector(vi_tri_text_ben_ngoai, vector_vuong_goc, cong_thuc_move_xuong_duoi) #move theo don vi feet
#         move_qua_phai = module.move_point_along_vector(move_len_tren,- vector_cua_dim, cong_thuc_move_qua_phai )
    
#     segment.TextPosition = move_qua_phai # Thực hiện hành động move

#     return 


# '''Đây là cách để tính góc giữa 2 vector
#     Góc 2 vector = Tích vô hướng của 2 vector
#     chia cho tích độ lớn 2 vector'''
# # Hàm tính góc giữa hai vector
# def angle_between_vectors(vector1, vector2):
#     # Tích vô hướng của 2 vector
#     dot_prod = vector1.DotProduct(vector2)
#     # Tính độ lớn của hai vector
#     magnitude1 = vector1.GetLength()
#     magnitude2 = vector2.GetLength()
#     # Tính cos(theta)
#     cos_theta = dot_prod / (magnitude1 * magnitude2)
#     # Trả về góc (theo độ)
#     goc_theo_do = math.degrees(math.acos(cos_theta))

#     return goc_theo_do

# '''Biến một vector bất kì thành vector từ dưới lên trên, từ trái qua phải
#     Mục đích là để xác định hướng trái và hướng phải của vector'''
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


# def distance(point1, point2):
#     return ((point2.X - point1.X)**2 + (point2.Y - point1.Y)**2)**0.5

# def distance_from_point_to_element(point1, obj):
#     return distance(point1, obj.Origin)


# '''Xác định hướng của từng segment so với vector vuông góc với nó
# Điểm A là vị trí của segment, điểm B là điểm click vào màn hình'''
# def xac_dinh_phia(A, B, vector_giua_2_diem,view_direction):
#     vector_AB = XYZ(B.X - A.X, B.Y - A.Y, B.Z - A.Z)
#     cross_product = vector_AB.CrossProduct(vector_giua_2_diem)
#     # Xác định hướng dựa trên dấu của cross product
#     '''Kiểm tra tích vô hướng của 2 vector 
#     (dotproduct của vector tích có hướng và view direction
#     Nếu 2 vector này cùng hướng thì dotproduct > 0, dotproduct < 0 thì ngược hướng,
#     còn != 0 thì không song song với nhau '''
#     dot_prod = view_direction.DotProduct(cross_product)
#     if dot_prod > 0: 
#         ket_qua = "Bên trái"
#     elif dot_prod < 0:
#         ket_qua = "Bên phải"
#     else:
#         ket_qua= "Thẳng hàng"        
#     return ket_qua


# def sort_seg_by_distance(A, seg_list):
#     # Sắp xếp các điểm trong list dựa trên khoảng cách từ xa đến gần điểm A
#     sorted_points = sorted(seg_list, key=lambda obj: distance_from_point_to_element(A, obj), reverse=True)
#     return sorted_points

try:
    t0 = Transaction(doc,"Set Work Plane")
    t0.Start()        
    current_view = uidoc.ActiveView
    try:
        module.set_work_plane_for_view (current_view)
    except:
        # print(traceback.format_exc())
        pass
    t0.Commit() 

    current_selection = module.get_selected_elements(uidoc,doc, False)

    if current_selection == False:
        collector = FilteredElementCollector(uidoc.Document, current_view.Id).OfCategory(BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType()
        pick = uidoc.Selection.PickObject(ObjectType.Element)
        element = doc.GetElement(pick.ElementId)
    else:
        element = current_selection[0]

    return_point = module.pick_point_with_nearest_snap(uidoc)

    dim_type = doc.GetElement(element.GetTypeId())

    text_size_para = module.get_builtin_parameter_by_name(dim_type, DB.BuiltInParameter.TEXT_SIZE)
    text_size_value = text_size_para.AsDouble()
    text_size_in_view = text_size_value * current_view.Scale
    # print return_point
    t = Transaction(doc,"Modify Text's Position of Dimension")
    t.Start() 

    '''Dòng này dùng để bật hoặc tắt leader line
       Đối với cách move dim type 3 và 4 thì cần bật leader line'''
    
    # Tat leader line
    para_leader_line = module.get_builtin_parameter_by_name(element, DB.BuiltInParameter.DIM_LEADER)
    para_leader_line.Set(int(0))

    seg_phai = []
    seg_trai = []
    none_segment = []
    view_direction = current_view.ViewDirection

    dim_line = element.Curve

    vector_of_dim = dim_line.Direction

    vector_da_chuan_hoa = movetextdim.chuan_hoa_vector(vector_of_dim, current_view)

    kich_thuoc_moi_chu = out_put

    kick_thuoc_tu_dim_toi_text = 1

    quy_doi_theo_ty_le = (kick_thuoc_tu_dim_toi_text * current_view.Scale) /304.8

    number_of_segments =  element.NumberOfSegments
    if number_of_segments != 0:
        segments = element.Segments
        for seg in segments:
            text_ori = seg.Origin
            value = (seg.Value) * 304.8 #Don vi dang la mm
            kich_co = module.xac_dinh_kich_co_chu(current_view, value, kich_thuoc_moi_chu)
            xoay_vector_90_do = movetextdim.rotate_vector_around_axis(vector_da_chuan_hoa, view_direction, 90)

            phia = movetextdim.xac_dinh_phia(text_ori, return_point, xoay_vector_90_do,view_direction)

            if phia == "Bên phải":
                seg_phai.append(seg)
            if phia == "Bên trái":
                seg_trai.append(seg)

        if round(float(vector_of_dim.Z),3) == 0:
            sorted_phai =  module.sort_seg_by_distance_mat_bang(return_point,seg_phai) #Sort segment xa nhất tới gần nhất tính tình point đã click
            sorted_trai =  module.sort_seg_by_distance_mat_bang(return_point,seg_trai) #Sort segment xa nhất tới gần nhất tính tình point đã click
        else:
            sorted_phai =  module.sort_seg_by_distance_mat_cat(return_point,seg_phai) #Sort segment xa nhất tới gần nhất tính tình point đã click
            sorted_trai =  module.sort_seg_by_distance_mat_cat(return_point,seg_trai) #Sort segment xa nhất tới gần nhất tính tình point đã click     

        '''Move text ben phai'''     

        if len(sorted_phai) == 2:
 
            segment_phai_0 = sorted_phai[0]
            value_seg_phai_0 = (segment_phai_0.Value) * 304.8
            kich_co_chu_phai_0 = module.xac_dinh_kich_co_chu(current_view, value_seg_phai_0, kich_thuoc_moi_chu)
            module.move_segment_xa_nhat(sorted_phai, vector_da_chuan_hoa, kich_co_chu_phai_0 ,quy_doi_theo_ty_le, huong_phai = True)
            vi_tri_text_ben_ngoai_phai = segment_phai_0.TextPosition

            segment_phai_1 = sorted_phai[1]
            value_seg_phai_1 = (segment_phai_1.Value) * 304.8
            kich_co_chu_phai_1 = module.xac_dinh_kich_co_chu(current_view, value_seg_phai_1, kich_thuoc_moi_chu)
            movetextdim.move_dim_segment_ben_trong_xuong_duoi (segment_phai_1,kich_co_chu_phai_1, kich_co_chu_phai_0, vi_tri_text_ben_ngoai_phai, vector_da_chuan_hoa , xoay_vector_90_do, text_size_in_view, quy_doi_theo_ty_le, huong_phai = True)

        if len(sorted_phai) == 1:
            segment_phai_0 = sorted_phai[0]
            value_seg_phai_0 = (segment_phai_0.Value) * 304.8
            kich_co_chu_phai_0 = module.xac_dinh_kich_co_chu(current_view, value_seg_phai_0, kich_thuoc_moi_chu)
            module.move_segment_xa_nhat(sorted_phai, vector_da_chuan_hoa,kich_co_chu_phai_0,quy_doi_theo_ty_le, huong_phai = True)
        
        
        '''Move text ben trai'''     

        if len(sorted_trai) == 2:
 
            segment_trai_0 = sorted_trai[0]
            value_seg_trai_0 = (segment_trai_0.Value) * 304.8
            kich_co_chu_trai_0 = module.xac_dinh_kich_co_chu(current_view, value_seg_trai_0, kich_thuoc_moi_chu)
            module.move_segment_xa_nhat(sorted_trai, vector_da_chuan_hoa, kich_co_chu_trai_0 ,quy_doi_theo_ty_le, huong_phai = False)
            vi_tri_text_ben_ngoai_trai = segment_trai_0.TextPosition

            segment_trai_1 = sorted_trai[1]
            value_seg_trai_1 = (segment_trai_1.Value) * 304.8
            kich_co_chu_trai_1 = module.xac_dinh_kich_co_chu(current_view, value_seg_trai_1, kich_thuoc_moi_chu)
            movetextdim.move_dim_segment_ben_trong_xuong_duoi (segment_trai_1,kich_co_chu_trai_1, kich_co_chu_trai_0, vi_tri_text_ben_ngoai_trai, vector_da_chuan_hoa , xoay_vector_90_do, text_size_in_view, quy_doi_theo_ty_le, huong_phai = False)

        if len(sorted_trai) == 1:
            segment_trai_0 = sorted_trai[0]
            value_seg_trai_0 = (segment_trai_0.Value) * 304.8
            kich_co_chu_trai_0 = module.xac_dinh_kich_co_chu(current_view, value_seg_trai_0, kich_thuoc_moi_chu)
            module.move_segment_xa_nhat(sorted_trai, vector_da_chuan_hoa,kich_co_chu_trai_0,quy_doi_theo_ty_le, huong_phai = False)

    t.Commit()
except:
    # print(traceback.format_exc())
    pass




