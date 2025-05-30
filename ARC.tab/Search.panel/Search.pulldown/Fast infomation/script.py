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
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
Ele = module.get_selected_elements(uidoc,doc)
t = Transaction (doc, "Quick Properties")

''' Ham nay dung de in ra traceback truoc khi bo qua loi
try:
    Code
except:
    print(traceback.format_exc())
    pass
'''
# def encode_to_base64(input_string):

# def flatten_list(list):

# def get_selected_elements(tem_uidoc, tem_doc):

# def Active_view(idoc):

# def get_parameter_by_name(element, name, is_UTF8 = False)

# def get_parameter_value_by_name(element, name, is_UTF8 = False)

# def set_parameter_value_by_name(element, name, value, is_UTF8 = False)

# def get_type(idoc, element)

# def get_type_name (idoc, element)

# def all_type_of_class_and_OST (idoc, ofClass, BuiltInCategory_OST): 
    ##### vi du khi category co san Class: list_type = all_type_of_class_and_OST(doc, FloorType, BuiltInCategory.OST_Floors)
    ##### vi du ve FamilySymbol: list_type = all_type_of_class_and_OST(FamilySymbol, BuiltInCategory.OST_StructuralFraming)

# def get_all_elements_of_OST(idoc, BuiltInCategory_OST): "Vi du: floor = module.get_all_elements_of_OST(doc, BuiltInCategory.OST_Floors)"

# def get_current_selection(iuidoc,element)



# t.Start()
# list_ele = []
# for i in Ele:
#     print i.UniqueId

# # module.get_current_selection(uidoc,list_ele)
# # floor = module.get_all_elements_of_OST(doc, DB.BuiltInCategory.OST_Floors)
# t.Commit()        
