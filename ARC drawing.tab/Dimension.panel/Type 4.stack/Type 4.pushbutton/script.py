# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
from Autodesk.Revit.UI.Selection import ObjectType
import movetextdim
import nances as module
from nances import vectortransform
if module.AutodeskData():
	uidoc = __revit__.ActiveUIDocument
	doc = uidoc.Document
try:
    import width_of_text_of_dim_config
    source_width_of_text_of_dim = width_of_text_of_dim_config.load_configs()
    out_put = float(source_width_of_text_of_dim[0][0])
except:
    # print (traceback.format_exc())
    out_put = 1.8

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
            vectortransform.move_segment_xa_nhat(sorted_phai, vector_da_chuan_hoa, kich_co_chu_phai_0 ,quy_doi_theo_ty_le, huong_phai = True)
            vi_tri_text_ben_ngoai_phai = segment_phai_0.TextPosition

            segment_phai_1 = sorted_phai[1]
            value_seg_phai_1 = (segment_phai_1.Value) * 304.8
            kich_co_chu_phai_1 = module.xac_dinh_kich_co_chu(current_view, value_seg_phai_1, kich_thuoc_moi_chu)
            movetextdim.move_dim_segment_ben_trong_xuong_duoi (segment_phai_1,kich_co_chu_phai_1, kich_co_chu_phai_0, vi_tri_text_ben_ngoai_phai, vector_da_chuan_hoa , xoay_vector_90_do, text_size_in_view, quy_doi_theo_ty_le, huong_phai = True)

        if len(sorted_phai) == 1:
            segment_phai_0 = sorted_phai[0]
            value_seg_phai_0 = (segment_phai_0.Value) * 304.8
            kich_co_chu_phai_0 = module.xac_dinh_kich_co_chu(current_view, value_seg_phai_0, kich_thuoc_moi_chu)
            vectortransform.move_segment_xa_nhat(sorted_phai, vector_da_chuan_hoa,kich_co_chu_phai_0,quy_doi_theo_ty_le, huong_phai = True)
        
        
        '''Move text ben trai'''     

        if len(sorted_trai) == 2:
 
            segment_trai_0 = sorted_trai[0]
            value_seg_trai_0 = (segment_trai_0.Value) * 304.8
            kich_co_chu_trai_0 = module.xac_dinh_kich_co_chu(current_view, value_seg_trai_0, kich_thuoc_moi_chu)
            vectortransform.move_segment_xa_nhat(sorted_trai, vector_da_chuan_hoa, kich_co_chu_trai_0 ,quy_doi_theo_ty_le, huong_phai = False)
            vi_tri_text_ben_ngoai_trai = segment_trai_0.TextPosition

            segment_trai_1 = sorted_trai[1]
            value_seg_trai_1 = (segment_trai_1.Value) * 304.8
            kich_co_chu_trai_1 = module.xac_dinh_kich_co_chu(current_view, value_seg_trai_1, kich_thuoc_moi_chu)
            movetextdim.move_dim_segment_ben_trong_xuong_duoi (segment_trai_1,kich_co_chu_trai_1, kich_co_chu_trai_0, vi_tri_text_ben_ngoai_trai, vector_da_chuan_hoa , xoay_vector_90_do, text_size_in_view, quy_doi_theo_ty_le, huong_phai = False)

        if len(sorted_trai) == 1:
            segment_trai_0 = sorted_trai[0]
            value_seg_trai_0 = (segment_trai_0.Value) * 304.8
            kich_co_chu_trai_0 = module.xac_dinh_kich_co_chu(current_view, value_seg_trai_0, kich_thuoc_moi_chu)
            vectortransform.move_segment_xa_nhat(sorted_trai, vector_da_chuan_hoa,kich_co_chu_trai_0,quy_doi_theo_ty_le, huong_phai = False)

    t.Commit()
except:

    pass




