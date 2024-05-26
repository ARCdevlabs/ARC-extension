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
import traceback
if module.AutodeskData():
	uidoc = __revit__.ActiveUIDocument
	doc = uidoc.Document

from Autodesk.Revit.UI.Selection import ObjectType, Selection


import width_of_text_of_dim_config

source_width_of_text_of_dim = width_of_text_of_dim_config.load_configs()

out_put = float(source_width_of_text_of_dim[0][0])


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


try:
    t0 = Transaction(doc,"Set Work Plane")
    t0.Start()        
    current_view = uidoc.ActiveView
    try:
        module.set_work_plane_for_view (current_view)
    except:
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
    # print return_point
    t = Transaction(doc,"Modify Text's Position of Dimension")
    t.Start() 
    # Tat leader line
    para_leader_line = module.get_builtin_parameter_by_name(element, DB.BuiltInParameter.DIM_LEADER)
    para_leader_line.Set(int(0))

    seg_phai = []
    seg_trai = []
    none_segment = []

    dim_line = element.Curve
    vector_of_dim = dim_line.Direction
    if round(float(vector_of_dim.Z),3) == 0:
        vector = module.chuan_hoa_vector_mat_bang(vector_of_dim)
    else:
        vector = module.chuan_hoa_vector_mat_cat(vector_of_dim)
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
            if round(float(vector_of_dim.Z),3) == 0:
                xoay_vector_90_do = XYZ(-vector.Y, vector.X, vector.Z)
                xac_dinh_phia = module.orientation_mat_bang(text_ori,return_point,xoay_vector_90_do)
            else:
                xoay_vector_90_do = XYZ(vector.X, vector.Z, -vector.Y)
                xac_dinh_phia = module.orientation_mat_cat(text_ori,return_point,xoay_vector_90_do)
            # print xac_dinh_phia
            if xac_dinh_phia == "Bên phải":
                seg_phai.append(seg)
            if xac_dinh_phia == "Bên trái":
                seg_trai.append(seg)

        if round(float(vector_of_dim.Z),3) == 0:
            sorted_phai =  module.sort_seg_by_distance_mat_bang(return_point,seg_phai) #Sort segment xa nhất tới gần nhất tính tình point đã click
            sorted_trai =  module.sort_seg_by_distance_mat_bang(return_point,seg_trai) #Sort segment xa nhất tới gần nhất tính tình point đã click
        else:
            sorted_phai =  module.sort_seg_by_distance_mat_cat(return_point,seg_phai) #Sort segment xa nhất tới gần nhất tính tình point đã click
            sorted_trai =  module.sort_seg_by_distance_mat_cat(return_point,seg_trai) #Sort segment xa nhất tới gần nhất tính tình point đã click     

        '''Move text ben phai'''     

        if len(sorted_phai) == 2:
            segment_phai_1 = sorted_phai[1]
            value_seg_phai_1 = (segment_phai_1.Value) * 304.8
            kich_co_chu_phai_1 = module.xac_dinh_kich_co_chu(current_view, value_seg_phai_1, kich_thuoc_moi_chu)
            move_dim_segment_ben_trong (sorted_phai,segment_phai_1, vector, kich_co_chu_phai_1, quy_doi_theo_ty_le, huong_phai = True)

            segment_phai_0 = sorted_phai[0]
            value_seg_phai_0 = (segment_phai_0.Value) * 304.8
            kich_co_chu_phai_0 = module.xac_dinh_kich_co_chu(current_view, value_seg_phai_0, kich_thuoc_moi_chu)
            move_dim_segment_ben_ngoai (segment_phai_0, kich_co_chu_phai_1, vector, kich_co_chu_phai_0, quy_doi_theo_ty_le, huong_phai = True)

        if len(sorted_phai) == 1:
            segment_phai_0 = sorted_phai[0]
            value_seg_phai_0 = (segment_phai_0.Value) * 304.8
            kich_co_chu_phai_0 = module.xac_dinh_kich_co_chu(current_view, value_seg_phai_0, kich_thuoc_moi_chu)            
            module.move_segment_xa_nhat(sorted_phai, vector,kich_co_chu_phai_0,quy_doi_theo_ty_le, huong_phai = True)
        
        
        '''Move text ben trai'''     
        if len(sorted_trai) == 2:
            segment_trai_1 = sorted_trai[1]
            value_seg_trai_1 = (segment_trai_1.Value) * 304.8
            kich_co_chu_trai_1 = module.xac_dinh_kich_co_chu(current_view, value_seg_trai_1, kich_thuoc_moi_chu)
            move_dim_segment_ben_trong (sorted_trai,segment_trai_1, vector, kich_co_chu_trai_1, quy_doi_theo_ty_le, huong_phai = False)

            segment_trai_0 = sorted_trai[0]
            value_seg_trai_0 = (segment_trai_0.Value) * 304.8
            kich_co_chu_trai_0 = module.xac_dinh_kich_co_chu(current_view, value_seg_trai_0, kich_thuoc_moi_chu)
            move_dim_segment_ben_ngoai (segment_trai_0, kich_co_chu_trai_1, vector, kich_co_chu_trai_0, quy_doi_theo_ty_le, huong_phai = False)

        if len(sorted_trai) == 1:
            segment_trai_0 = sorted_trai[0]
            value_seg_trai_0 = (segment_trai_0.Value) * 304.8
            kich_co_chu_trai_0 = module.xac_dinh_kich_co_chu(current_view, value_seg_trai_0, kich_thuoc_moi_chu)
            module.move_segment_xa_nhat(sorted_trai, vector,kich_co_chu_trai_0,quy_doi_theo_ty_le, huong_phai = False)

    t.Commit()
except:
    # print(traceback.format_exc())
    pass




