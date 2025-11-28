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
    phuong_doc = []
    for tung_ele in ele:
            try:
                facing_orient =  tung_ele.FacingOrientation
                y_orient = facing_orient.Y
                kiem_tra = abs(y_orient)
                if kiem_tra >= 0.55:
                    phuong_doc.append(tung_ele)
            except:
                pass
    select = module.get_current_selection(uidoc,phuong_doc)
    t.Commit()      
