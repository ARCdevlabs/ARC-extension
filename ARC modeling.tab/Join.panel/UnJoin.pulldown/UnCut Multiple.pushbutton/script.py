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

Ele = module.get_selected_elements(uidoc, doc)
listele = []
t = Transaction (doc, "UnCut multiple")
t.Start()
pick = Ele
dependent = []
for e in Ele:
    get_cutting_solid = Autodesk.Revit.DB.SolidSolidCutUtils.GetCuttingSolids(e)
    get_cutting_void = Autodesk.Revit.DB.InstanceVoidCutUtils.GetCuttingVoidInstances(e)
    if len(get_cutting_solid) > 0:
        for element_Id in get_cutting_solid:
            ele_cutting = doc.GetElement(element_Id)
            remove_cut = Autodesk.Revit.DB.SolidSolidCutUtils.RemoveCutBetweenSolids(doc,e, ele_cutting)
    if len(get_cutting_void) > 0:
        for element_Id_2 in get_cutting_void:
            ele_cutting_2 = doc.GetElement(element_Id_2)
            remove_cut_2 = Autodesk.Revit.DB.InstanceVoidCutUtils.RemoveInstanceVoidCut(doc,e, ele_cutting_2)
    else:
        pass
t.Commit()