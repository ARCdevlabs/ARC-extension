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
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Ele = module.get_selected_elements(uidoc,doc)
    list_ele = []
    for i in Ele:
        element_type = module.get_type(doc, i)
        try:
            family = element_type.Family
            list_ele.append(family)
        except:
            pass
    module.get_current_selection(uidoc,list_ele)    
