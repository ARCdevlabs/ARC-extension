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
    list_noname_ref = []
    for tung_element in Ele:
        name = tung_element.Name
        if name == "Reference Plane":
            list_noname_ref.append(tung_element.Id)
            sub_category = nances.get_builtin_parameter_by_name(tung_element, DB.BuiltInParameter.CLINE_SUBCATEGORY)
            sub_category_name = sub_category.AsValueString()
            print name + "  ID:  " + str(tung_element.Id) + "    "+ str(sub_category_name)
    Icollection = List[ElementId](list_noname_ref)
    selection.SetElementIds(Icollection)
