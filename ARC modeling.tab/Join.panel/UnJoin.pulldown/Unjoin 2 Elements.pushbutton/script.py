__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import*
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Element
from System.Collections.Generic import *
import math
from rpw import ui
from rpw.ui.forms import Alert
# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import traceback
import nances
if nances.AutodeskData():
    #Get UIDocument
    uidoc = __revit__.ActiveUIDocument
    #Get Document 
    doc = uidoc.Document
    Currentview = doc.ActiveView
    def get_selected_elements():
        selection = uidoc.Selection
        selection_ids = selection.GetElementIds()
        elements = []
        for element_id in selection_ids:
            elements.append(doc.GetElement(element_id))
        return elements
    Ele = module.get_selected_elements(uidoc, doc, noti = True)
    listele = []
    try:
        if Ele:
            t = Transaction (doc, "Unjoin 2 elements")
            t.Start()
            try:
                pick = Ele
                for i in pick:     
                    listele.append(doc.GetElement(i.Id)) 
                if len(listele) !=2:
                    Alert('You must select 2 elements',title="Warning",header= "Something wrong")
                else:
                    if JoinGeometryUtils.AreElementsJoined(doc, listele[1], listele[0]):
                        JoinGeometryUtils.UnjoinGeometry(doc, listele[1], listele[0])
                    else:
                        Alert('These elements have not joined yet',title="Warning",header= "Something wrong")
            except:
                pass
            t.Commit()
    except:
        pass