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
from Autodesk.Revit.UI.Selection import ObjectType, Selection
import traceback

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
pick_dims = module.pick_dimension_elements(uidoc,doc)

def count_decimal_places(number):
    # Chuyển đổi số thành chuỗi và loại bỏ các số 0 không có ý nghĩa ở cuối phần thập phân
    str_number = str(number).rstrip('0').rstrip('.')
    
    # Tách phần nguyên và phần thập phân
    if '.' in str_number:
        integer_part, decimal_part = str_number.split('.')
        # Đếm số chữ số trong phần thập phân
        return len(decimal_part)
    else:
        # Nếu không có phần thập phân
        return 0
    
def get_last_letter(number):
    # Chuyển đổi số thành chuỗi và loại bỏ các số 0 không có ý nghĩa ở cuối phần thập phân
    str_number = str(number).rstrip('0').rstrip('.')
    
    # Lấy giá trị cuối cùng của số
    last_digit = str_number[-1]
    
    return last_digit

select = uidoc.Selection

list_dimension_and_seg =[]
list_dim_le = []
for dimension in pick_dims:
    try:
        number_segment = dimension.NumberOfSegments
        if number_segment > 1:
            segments = dimension.Segments
            for seg in segments:
                value = seg.Value
                quy_doi_mm = value *304.8
                lam_tron = round(quy_doi_mm,2)
                dem_so_thap_phan = count_decimal_places(lam_tron)
                so_cuoi_cung = get_last_letter(quy_doi_mm)
                # print so_cuoi_cung
                # if dem_so_thap_phan > 1 and so_cuoi_cung != 0 and so_cuoi_cung != 5:
                if dem_so_thap_phan > 1:                
                    list_dim_le.append(dimension.Id)
                    # print lam_tron
        else:
            value = dimension.Value
            quy_doi_mm = value *304.8
            lam_tron = round(quy_doi_mm,3)
            dem_so_thap_phan = count_decimal_places(lam_tron)
            so_cuoi_cung = get_last_letter(quy_doi_mm)
            if dem_so_thap_phan > 1 and so_cuoi_cung != 0 and so_cuoi_cung != 5:
                list_dim_le.append(dimension.Id)
                # print lam_tron
    except:
        pass

Icollection = List[ElementId](list_dim_le)
select.SetElementIds(Icollection)