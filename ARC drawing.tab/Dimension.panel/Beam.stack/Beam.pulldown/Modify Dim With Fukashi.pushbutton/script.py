# -*- coding: utf-8 -*-
import Autodesk
import nances
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit import script

import setup_family_beam_config

logger = script.get_logger()
my_config = script.get_config()
source_setting_family_beam = setup_family_beam_config.load_configs()

if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document

    def get_reference_by_name_in_family (instance, name):
        refp = instance.GetReferenceByName(name)
        return refp

    current_view = uidoc.ActiveView
    # pick = uidoc.Selection.PickObject(ObjectType.Element)
    Ele = nances.get_selected_elements(uidoc,doc)
    t = Transaction(doc,"Modify dim with fukashi")
    t.Start() 
    list_new_dim =[]
    for element in Ele:
        
        all_ref = ReferenceArray()
        list_all_ref =[]
        list_element =[]
        ref_array = element.References
        line = element.Curve
        huong = line.Direction
        for ref in ref_array:
            element_host = doc.GetElement(ref.ElementId)
            list_element.append(element_host)
            all_ref.Append(ref)

        type_of_ele = element_host.GetType()
        if str(type_of_ele) == "Autodesk.Revit.DB.FamilyInstance":

            tc_top = nances.get_parameter_value_by_name(element_host, source_setting_family_beam[8], is_UTF8 = False)
            tc_bot = nances.get_parameter_value_by_name(element_host, source_setting_family_beam[9], is_UTF8 = False)
            tc_trai = nances.get_parameter_value_by_name(element_host, source_setting_family_beam[10], is_UTF8 = False)
            tc_phai = nances.get_parameter_value_by_name(element_host, source_setting_family_beam[11],is_UTF8 = False)

            ref_top = get_reference_by_name_in_family(element_host,source_setting_family_beam[0])
            ref_bot = get_reference_by_name_in_family(element_host,source_setting_family_beam[1])           
            ref_trai = get_reference_by_name_in_family(element_host,source_setting_family_beam[2])
            ref_phai = get_reference_by_name_in_family(element_host,source_setting_family_beam[3])

            ref_fukashi_top = get_reference_by_name_in_family(element_host,source_setting_family_beam[4])
            ref_fukashi_bot = get_reference_by_name_in_family(element_host,source_setting_family_beam[5])           
            ref_fukashi_trai = get_reference_by_name_in_family(element_host,source_setting_family_beam[6])
            ref_fukashi_phai = get_reference_by_name_in_family(element_host,source_setting_family_beam[7])
            
        if float(tc_trai) > 0:
            all_ref.Append(ref_trai)

        if float(tc_phai) > 0:
            all_ref.Append(ref_phai)


        new_dim = doc.Create.NewDimension(current_view, line, all_ref)

        list_new_dim.append(new_dim)

        # Xoa dim cu di
        Autodesk.Revit.DB.Document.Delete(doc,element.Id)

    select = uidoc.Selection
    listid = []

    for dim in list_new_dim:
        dim_id = dim.Id
        listid.append(dim_id)
    Icollection = List[ElementId](listid)
    select.SetElementIds(Icollection)

    t.Commit()






