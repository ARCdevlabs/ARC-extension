__doc__ = 'nguyenthanhson1712@gmail.com'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib

ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
# def get_parameter_value_by_name(element, name, is_UTF8 = False)

# def set_parameter_value_by_name(element, name, value, is_UTF8 = False)
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Ele = module.get_selected_elements(uidoc,doc)
    t = Transaction (doc, "Base 2F Top 2F")
    t.Start()
    level_2 = ElementId(2924453)
    level_3 = ElementId(2924442)
    for i in Ele:
        base_level = module.get_parameter_value_by_name(i, "Base Level", is_UTF8 = False)
        base_offset = module.get_parameter_value_by_name(i, "Base Offset", is_UTF8 = False)
        top_level = module.get_parameter_value_by_name(i, "Top Level", is_UTF8 = False)
        top_offset = module.get_parameter_value_by_name(i, "Top Offset", is_UTF8 = False)
        top = module.get_parameter_by_name(i, "Top Level", is_UTF8 = False)
        top.Set(level_2)
        base = module.get_parameter_by_name(i, "Base Level", is_UTF8 = False)
        base.Set(level_2)
        top_offset = module.set_parameter_value_by_name(i, "Top Offset", (6700 + float(top_offset))/304.8 ,is_UTF8 = False)
    t.Commit()        
