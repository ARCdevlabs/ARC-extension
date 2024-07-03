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
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
import sys
import string
import importlib
import traceback
# print(traceback.format_exc())
try:
    ARC = string.ascii_lowercase
    begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
    module = importlib.import_module(str(begin))
    import Autodesk
    from Autodesk.Revit.DB import *
    from System.Collections.Generic import *
    if module.AutodeskData():
        Currentview = doc.ActiveView
        view_scale = Currentview.Scale
except:
    sys.exit()

list_point = []
list_ok=[]
list_not_ok= []

Ele = module.get_all_elements_of_OST(doc, BuiltInCategory.OST_StructuralFraming)
# Ele = module.get_selected_elements(uidoc,doc)
t = Transaction(doc, "Auto check hướng dầm")
t.Start()
for i in Ele:
    try:
        cur = i.Location.Curve.Direction
        Point1 = i.Location.Curve.GetEndPoint(0)
        Point2 = i.Location.Curve.GetEndPoint(1)
        list_point.append(Point1)
        list_point.append(Point2)
        is_mirrored = i.Mirrored
        if is_mirrored:
            list_ok.append(i)
        else:
            if abs(cur.X) < abs(cur.Y):
                # if Point1.Y < Point2.Y:
                if Point1.Y < Point2.Y:
                    list_ok.append(i)            
                else:
                    list_not_ok.append(i)
            elif Point1.X < Point2.X:
                list_ok.append(i)
            else: 
                list_not_ok.append(i)
    except:
        # print(traceback.format_exc())
        pass
def TempIsolate(view, items):
    ielements = List[ElementId]([x.Id for x in items])
    view.IsolateElementsTemporary(ielements)
TempIsolate(Currentview, list_not_ok)

t.Commit()
