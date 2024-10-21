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

Ele = module.get_selected_elements(uidoc, doc, noti = False)

if not Ele:
    try:
        pick_1 = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element)
        dim_1 = doc.GetElement(pick_1.ElementId)
        pick_2 = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element)
        dim_2 = doc.GetElement(pick_2.ElementId)
        t = Transaction(doc,"Đổi vị trí của 2 dim")
        t.Start()
        line_dim_1 = dim_1.Curve
        line_dim_2 = dim_2.Curve
        vector_move_1 = tinh_toan_vector_move (line_dim_1,line_dim_2)
        vector_move_2 = tinh_toan_vector_move (line_dim_2,line_dim_1)
        move_dim_1 = move_element(doc,dim_1, vector_move_1)
        move_dim_2 = move_element(doc,dim_2, vector_move_2)
        t.Commit()
    except:
        pass
else:
    if len(Ele) != 2:
        message = module.message_box("Chỉ chọn 2 dim thôi, không nhiều hơn, không ít hơn")
    else:
        dim_1 = Ele[0]
        dim_2 = Ele[1]
        t = Transaction(doc,"Đổi vị trí của 2 dim")
        t.Start()
        line_dim_1 = dim_1.Curve
        line_dim_2 = dim_2.Curve
        vector_move_1 = tinh_toan_vector_move (line_dim_1,line_dim_2)
        vector_move_2 = tinh_toan_vector_move (line_dim_2,line_dim_1)
        move_dim_1 = move_element(doc,dim_1, vector_move_1)
        move_dim_2 = move_element(doc,dim_2, vector_move_2)
        t.Commit()





