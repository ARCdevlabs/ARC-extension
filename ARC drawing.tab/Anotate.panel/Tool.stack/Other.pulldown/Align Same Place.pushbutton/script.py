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
from System.Collections.Generic import *
from Autodesk.Revit.UI.Selection  import ObjectType
from nances import forms
import traceback
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Currentview = doc.ActiveView
    Curve = []
    Ele = module.get_elements(uidoc,doc, "Select Tags", noti = False)
    try:
        pick = False
        with forms.WarningBar(title="Select Origin Tag"):
            try:
                pick = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element)
            except:
                pass
        if pick:
            idele = pick.ElementId
            OriTag = doc.GetElement(idele)
            loc = OriTag.TagHeadPosition
            t = Transaction (doc, "Move Tag Same place")
            t.Start()
            for i in Ele:
                try:
                    i.TagHeadPosition = loc
                except:
                    pass
            t.Commit()
    except:
        pass