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
from nances import forms
try:
    if module.AutodeskData():
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        Currentview = doc.ActiveView

        def ChangeType(element, typeId):
            element.ChangeTypeId(typeId)
            return element

        def main():
            with forms.WarningBar(title="Select First Element"):
                first_pick = uidoc.Selection.PickObject(ObjectType.Element)
                first_id = first_pick.ElementId
                first_ele = doc.GetElement(first_id)
                while True:
                    try:
                        with forms.WarningBar(title="Select Second Element"):
                            second_pick = uidoc.Selection.PickObject(ObjectType.Element)
                            second_id = second_pick.ElementId
                            second_ele = doc.GetElement(second_id)
                            try:
                                t = Transaction(doc, "Change type same category")
                                t.Start()
                                try:
                                    ChangeType(second_ele, first_ele.GetTypeId())
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
except:
    pass