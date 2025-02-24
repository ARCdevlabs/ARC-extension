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
import traceback
if module.AutodeskData():
    try:
        if module.AutodeskData():
            uidoc = __revit__.ActiveUIDocument
            doc = uidoc.Document
            Ele = module.get_elements(uidoc,doc, "Select Beam Need To Reverse", noti = False)
            t = Transaction (doc, "Reverse beam")
            t.Start()
            def disallow_join_at_end(element):
                Autodesk.Revit.DB.Structure.StructuralFramingUtils.DisallowJoinAtEnd(element, 0)
                Autodesk.Revit.DB.Structure.StructuralFramingUtils.DisallowJoinAtEnd(element, 1)
            def allow_join_at_end(element):
                Autodesk.Revit.DB.Structure.StructuralFramingUtils.AllowJoinAtEnd(element, 0)
                Autodesk.Revit.DB.Structure.StructuralFramingUtils.AllowJoinAtEnd(element, 1)
            for i in Ele:
                disallow_join_at_end(i)
                curve = i.Location.Curve
                curve_reverse = curve.CreateReversed()
                i.Location.Curve = curve_reverse
                allow_join_at_end(i)
            t.Commit()
            count_list_ele = len(Ele)
        from rpw.ui.forms import Alert
        Alert('Reversed ' + str(count_list_ele) + ' elements',title="ARC",header= "")
    except:
        pass