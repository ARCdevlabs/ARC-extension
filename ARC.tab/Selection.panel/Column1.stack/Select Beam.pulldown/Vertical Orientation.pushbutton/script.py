# -*- coding: utf-8 -*-
import string
import codecs
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *

if module.AutodeskData():
    import sys
    import clr
    clr.AddReference("System.Windows.Forms")
    from System.Windows.Forms import Application, Form, TextBox, Button, FormStartPosition, ComboBox
    from System.Drawing import Point, Size
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    ele = module.get_elements(uidoc,doc, 'string_warning_bar', noti = False)
    t = Transaction (doc, "Chọn dầm theo phương dọc ")
    t.Start()
    # def xac_dinh_phuong_doc_ngang(element):
    #     list_ngang = []
    #     list_doc = []
    #     for ii in element:
    #         try:
    #             cur = ii.Location.Curve.Direction
    #             if abs(cur.X) < abs(cur.Y):
    #                 list_doc.append(ii)            
    #             else:
    #                 list_ngang.append(ii)
    #         except:
    #             pass
    #     return list_doc, list_ngang
    # # beam = module.get_all_elements_of_OST(doc, BuiltInCategory.OST_StructuralFraming)
    # beam = module.get_all_elements_of_OST_in_current_view(doc, BuiltInCategory.OST_StructuralFraming)

    # chon_dam = xac_dinh_phuong_doc_ngang(beam)
    phuong_doc = []
    for tung_ele in ele:
            facing_orient =  tung_ele.FacingOrientation
            y_orient = facing_orient.Y
            kiem_tra = abs(y_orient)
            if kiem_tra >= 0.55:
                phuong_doc.append(tung_ele)
     
    select = module.get_current_selection(uidoc,phuong_doc)
    t.Commit()      
