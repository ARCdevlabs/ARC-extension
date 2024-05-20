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

def move_element (idoc, element, vector):
    move = Autodesk.Revit.DB.ElementTransformUtils.MoveElement(idoc,element.Id,vector)
    return move

def tinh_toan_vector_move(line1, line2):
    # Lấy điểm đầu và điểm cuối của line1
    start_point1 = line1.Origin
    # Lấy điểm đầu và điểm cuối của line2
    end_point2 = line2.Origin
    # Tính toán vector di chuyển
    move_vector = XYZ(end_point2.X - start_point1.X, end_point2.Y - start_point1.Y, end_point2.Z - start_point1.Z)
    return move_vector

class DimensionSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
    def AllowElement(self, element):
        # Chỉ cho phép chọn đối tượng Dimension
        return isinstance(element, Dimension)

    def AllowReference(self, reference, point):
        # Không sử dụng AllowReference trong trường hợp này
        return False

# Hàm chọn một Dimension từ danh sách sử dụng ISelectionFilter
def pick_dimension_element():
    selected_dimension = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element, DimensionSelectionFilter(), "Chọn một Dimension")
    return doc.GetElement(selected_dimension.ElementId) if selected_dimension else None




def main():
    # first_pick = uidoc.Selection.PickObject(ObjectType.Element)
    # first_id = first_pick.ElementId
    # first_ele = doc.GetElement(first_id)
    first_ele =  pick_dimension_element()
    dim_1 = first_ele
    line_dim_1 = dim_1.Curve
    while True:
        try:
            # second_pick = uidoc.Selection.PickObject(ObjectType.Element)
            # second_id = second_pick.ElementId
            # second_ele = doc.GetElement(second_id)
            second_ele = pick_dimension_element()
            dim_2 = second_ele
            line_dim_2 = dim_2.Curve
            vector_move_2 = tinh_toan_vector_move (line_dim_2,line_dim_1)
            try:
                t = Transaction(doc, "Align dim")
                t.Start()
                try:
                    move_element(doc,dim_2, vector_move_2)
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


