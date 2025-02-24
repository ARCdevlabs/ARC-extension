# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FailuresAccessor
from Autodesk.Revit.DB import Line
from Autodesk.Revit.Creation import ItemFactoryBase
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
import math
import sys
import string
import importlib
import traceback
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document

ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
if module.AutodeskData():
    Currentview = doc.ActiveView

    def tinh_toan_phuong_align (point1,point2):
        vector = XYZ(point1.X-point2.X,point1.Y-point2.Y,point1.Z-point2.Z)
        if abs(vector.X) < abs(vector.Y):
            new_point = XYZ(point1.X,point2.Y,point2.Z)
        else:
            new_point = XYZ(point2.X,point1.Y,point2.Z)
        return new_point

    class FamilyTagSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
        def AllowElement(self, element):
            # Chỉ cho phép chọn đối tượng FamilyInstance (family tag)
            return isinstance(element, IndependentTag)

        def AllowReference(self, reference, point):
            # Không sử dụng AllowReference trong trường hợp này
            return False

    # Hàm chọn một FamilyInstance từ danh sách sử dụng ISelectionFilter
    def pick_family_tag():
        selected_family_tag = uidoc.Selection.PickObject(
            Autodesk.Revit.UI.Selection.ObjectType.Element, 
            FamilyTagSelectionFilter(), 
            "Chọn một Family Tag"
        )
        return doc.GetElement(selected_family_tag.ElementId) if selected_family_tag else None

# first_ele =  pick_family_tag()
# first_text_position = first_ele.TagHeadPosition
# print first_text_position
def main():
    # first_pick = uidoc.Selection.PickObject(ObjectType.Element)
    # first_id = first_pick.ElementId
    # first_ele = doc.GetElement(first_id)
    first_ele = pick_family_tag()
    first_text_position = first_ele.TagHeadPosition
    while True:
        try:
            second_ele = pick_family_tag()
            second_text_position = second_ele.TagHeadPosition
            move_point_2 = tinh_toan_phuong_align(first_text_position,second_text_position)
            try:
                t = Transaction(doc, "Align tag")
                t.Start()
                try:
                    second_ele.TagHeadPosition = move_point_2
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


