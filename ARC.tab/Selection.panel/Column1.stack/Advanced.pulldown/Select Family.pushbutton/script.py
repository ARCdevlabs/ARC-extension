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
from System.Collections.Generic import *
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
Ele = module.get_selected_elements(uidoc,doc)
# t = Transaction (doc, "Chọn type từ element")
# t.Start()
list_ele = []
for i in Ele:
    element_type = module.get_type(doc, i)
    list_ele.append(element_type)
module.get_current_selection(uidoc,list_ele)
# t.Commit()        
