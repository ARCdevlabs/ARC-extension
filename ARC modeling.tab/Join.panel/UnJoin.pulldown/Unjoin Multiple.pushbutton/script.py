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
from rpw import ui
from rpw.ui.forms import Alert
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
Currentview = doc.ActiveView

Ele = module.get_elements(uidoc,doc, "Select Elements to UnJoin Geometry", noti = False)
listele = []
t = Transaction (doc, "Unjoin multiple")
t.Start()
try:
    pick = Ele
    dependent = []
    for i in pick:
        pickid = i.Id
        listele.append(doc.GetElement(pickid)) 
    for e in listele:
        dependent.append (JoinGeometryUtils.GetJoinedElements(doc,e))
        for a in dependent:
            for b in a:
                eleb = doc.GetElement(b)
                if JoinGeometryUtils.AreElementsJoined(doc, e, eleb):
                    JoinGeometryUtils.UnjoinGeometry(doc, e, eleb)
except:
    pass
t.Commit()