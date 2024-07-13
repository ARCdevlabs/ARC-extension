# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
import traceback
try:
    if module.AutodeskData():
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        Ele = module.get_elements(uidoc,doc, "Select Elements to UnCut", noti = False)
        listele = []
        pick = Ele
        dependent = []
        t = Transaction (doc, "UnCut multiple")
        t.Start()
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
except:
    pass