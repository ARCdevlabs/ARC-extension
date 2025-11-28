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
    list_noname_ref = []
    n = 1
    for tung_element in Ele:

        name = tung_element.Name
        list_noname_ref.append(tung_element.Id)
        sub_category = nances.get_builtin_parameter_by_name(tung_element, DB.BuiltInParameter.CLINE_SUBCATEGORY)
        sub_category_name = sub_category.AsValueString()

        ref_name_param = nances.get_builtin_parameter_by_name(tung_element, DB.BuiltInParameter.DATUM_TEXT)
        ref_name_param_name = ref_name_param.AsValueString()
        if ref_name_param_name =="":
            ref_name_param_name= "NoName"

        ref_workset_param = nances.get_builtin_parameter_by_name(tung_element, DB.BuiltInParameter.ELEM_PARTITION_PARAM)
        ref_workset_param_name = ref_workset_param.AsValueString()
        ref_group_id = tung_element.GroupId          
        print str(n) + ":"+ name + "  ID:  " + str(tung_element.Id) + "              "+ "  SubCategory:  " + str(sub_category_name) + "              "+ "  Name:  "+ str(ref_name_param_name) + "              "+ "  Workset:  "+ str(ref_workset_param_name) + "               Group ID:" + str(ref_group_id)
        n += 1
    Icollection = List[ElementId](list_noname_ref)
    selection.SetElementIds(Icollection)
