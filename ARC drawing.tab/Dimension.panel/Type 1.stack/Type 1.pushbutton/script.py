# -*- coding: utf-8 -*-
"""Activates selection tool that picks a specific type of element.

Shift-Click:
Pick favorites from all available categories
"""
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
    out_put = 1.8

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
        pick = module.pick_dimension_element(uidoc,doc)
        element = pick
        # element = doc.GetElement(pick.ElementId)
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
        if len(sorted_phai) > 0:
            value_phai_0 = (sorted_phai[0].Value) * 304.8 
            kich_co_phai_0 = module.xac_dinh_kich_co_chu(current_view, value_phai_0, kich_thuoc_moi_chu)
            module.move_segment_xa_nhat(sorted_phai, vector_da_chuan_hoa, kich_co_phai_0,quy_doi_theo_ty_le, huong_phai = True)
        if len(sorted_trai) > 0:
            value_trai_0 = (sorted_trai[0].Value) * 304.8 
            kich_co_trai_0 = module.xac_dinh_kich_co_chu(current_view, value_trai_0, kich_thuoc_moi_chu)
            module.move_segment_xa_nhat(sorted_trai, vector_da_chuan_hoa,kich_co_trai_0,quy_doi_theo_ty_le, huong_phai = False)
    else:
        seg = element
        none_segment.append(seg)
        text_ori = seg.Origin
        value = (seg.Value) * 304.8 #Don vi dang la mm
        kich_co = module.xac_dinh_kich_co_chu(current_view, value, kich_thuoc_moi_chu)
        xoay_vector_90_do = movetextdim.rotate_vector_around_axis(vector_da_chuan_hoa, view_direction, 90)
        phia = movetextdim.xac_dinh_phia(text_ori, return_point, xoay_vector_90_do,view_direction)
        if phia == "Bên trái":
            module.move_segment_xa_nhat(none_segment, vector_da_chuan_hoa, kich_co,quy_doi_theo_ty_le, huong_phai = True)
        else:
            module.move_segment_xa_nhat(none_segment, vector_da_chuan_hoa,kich_co,quy_doi_theo_ty_le, huong_phai = False)
    t.Commit()
except:
    pass




