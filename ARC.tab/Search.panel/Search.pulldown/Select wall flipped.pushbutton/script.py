# -*- coding: utf-8 -*-
import Autodesk
import nances
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Ele = nances.get_selected_elements(uidoc,doc)
    selection = uidoc.Selection
    # t = Transaction (doc, "Quick Properties")
    list_da_flip = []
    for tung_element in Ele:
        is_flip = tung_element.Flipped
        if is_flip:
            list_da_flip.append((tung_element.Id))

    Icollection = List[ElementId](list_da_flip)
    selection.SetElementIds(Icollection)
