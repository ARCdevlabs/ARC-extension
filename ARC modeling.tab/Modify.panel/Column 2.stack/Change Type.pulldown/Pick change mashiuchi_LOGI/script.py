# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import *

# Get UIDocument
uidoc = __revit__.ActiveUIDocument
# Get Document
doc = uidoc.Document
Currentview = doc.ActiveView


def ChangeType(element, typeId):
    element.ChangeTypeId(typeId)
    return element
# def get_parameter_value_by_name(element, name, is_UTF8 = False)

# def set_parameter_value_by_name(element, name, value, is_UTF8 = False)

def doi_tang_cuong (element, element_second):
    tang_cuong_tren = module.get_parameter_value_by_name(element, "フカシD", is_UTF8 = False)
    tang_cuong_phai = module.get_parameter_value_by_name(element, "フカシA", is_UTF8 = False)
    tang_cuong_duoi = module.get_parameter_value_by_name(element, "フカシB", is_UTF8 = False)
    tang_cuong_trai = module.get_parameter_value_by_name(element, "フカシC", is_UTF8 = False)
    module.set_parameter_value_by_name(element_second, "フカシD", float(tang_cuong_tren)/304.8, is_UTF8 = False)
    module.set_parameter_value_by_name(element_second, "フカシA", float(tang_cuong_phai)/304.8, is_UTF8 = False)
    module.set_parameter_value_by_name(element_second, "フカシB", float(tang_cuong_duoi)/304.8, is_UTF8 = False)
    module.set_parameter_value_by_name(element_second, "フカシC", float(tang_cuong_trai)/304.8, is_UTF8 = False)
    return

def main():
    first_pick = uidoc.Selection.PickObject(ObjectType.Element)
    first_id = first_pick.ElementId
    first_ele = doc.GetElement(first_id)
    while True:
        try:
            second_pick = uidoc.Selection.PickObject(ObjectType.Element)
            second_id = second_pick.ElementId
            second_ele = doc.GetElement(second_id)
            try:
                t = Transaction(doc, "Đổi tăng cường dầm_LOGI")
                t.Start()
                try:
                    # ChangeType(second_ele, first_ele.GetTypeId())
                    doi_tang_cuong(first_ele, second_ele)
                except:
                    pass
                t.Commit()
            except:
                pass
        except Exception as ex:
            if "Operation canceled by user." in str(ex):
                break
            else:
                break
main()