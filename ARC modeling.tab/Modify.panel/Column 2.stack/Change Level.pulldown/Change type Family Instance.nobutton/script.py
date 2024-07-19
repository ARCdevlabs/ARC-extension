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
        import pickle
        from pyrevit.coreutils import appdata
        from pyrevit.framework import List
        from pyrevit import revit, DB


    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    def ChangeType(element, typeId):
        try:
            element.ChangeTypeId(typeId)
            return element
        except:
            pass

    try:
        Ele = module.get_elements(uidoc,doc, "Select Element to Change Type", noti = False)
        t = Transaction (doc, "Change type 2")
        t.Start()
        for i in Ele:
            ChangeType(i, element_ids[0])
        t.Commit()
    except:
        pass
except:
    pass