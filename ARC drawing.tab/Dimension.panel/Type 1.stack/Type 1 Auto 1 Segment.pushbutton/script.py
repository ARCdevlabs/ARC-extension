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
from nances import allinone
if module.AutodeskData():
	uidoc = __revit__.ActiveUIDocument
	doc = uidoc.Document
from Autodesk.Revit.UI.Selection import ObjectType, Selection

try:
    import width_of_text_of_dim_config
    source_width_of_text_of_dim = width_of_text_of_dim_config.load_configs()
    out_put = float(source_width_of_text_of_dim[0])
except:
    out_put = 1.8

'''Code da sua tu version thu cong tung dim'''
try:
    elements = module.get_elements(uidoc,doc, 'Select Dimension', noti = False)
    trans_group = TransactionGroup(doc, 'Move text dim 1 segment(auto)')
    trans_group.Start()
    t0 = Transaction(doc,"Set Work Plane")
    t0.Start()        
    current_view = uidoc.ActiveView
    try:
        module.set_work_plane_for_view (current_view)
    except:
        pass
    t0.Commit() 

    for element in elements:
        try:

            t = Transaction(doc,"Modify Text's Position of Dimension")
            t.Start() 
            # Tat leader line
    
            allinone.reset_text_position(element)

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

            diem_trung_binh = element.Origin

            return_point = module.move_point_along_vector(diem_trung_binh, vector_da_chuan_hoa, -0.01)

            if number_of_segments == 0:
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
            t.RollBack()
            pass
    trans_group.Assimilate()
except:
    pass


