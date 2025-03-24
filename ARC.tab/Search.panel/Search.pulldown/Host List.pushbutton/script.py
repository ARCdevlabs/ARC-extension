# -*- coding: utf-8 -*-
from pyrevit import script
from pyrevit import revit, DB
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
from nances import forms
import traceback
import sys
import nances
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    active_view = nances.Active_view(uidoc)

    def get_selected_elements(tem_uidoc, tem_doc):
        selection = tem_uidoc.Selection
        selection_ids = selection.GetElementIds()
        elements = []     
        for element_id in selection_ids:
            elements.append(tem_doc.GetElement(element_id))
        return elements

    output = script.get_output()

    selected_element = module.get_elements(uidoc,doc, 'Select Elements', noti = False)
    list_ngoai_le =[]
    data = []
    for tung_element in selected_element:  
        try:
            id_element = tung_element.Id
            get_element_name_param= module.get_builtin_parameter_by_name(tung_element, BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM)
            get_element_name = get_element_name_param.AsValueString()

            get_host_param = module.get_builtin_parameter_by_name(tung_element, DB.BuiltInParameter.INSTANCE_FREE_HOST_PARAM)                    
            string_host = get_host_param.AsString()

            element_link = output.linkify(id_element)
            data.append((element_link,("Name of Element: {}".format(get_element_name)), ("Name of Host: {}".format(string_host))))

            print (element_link + "\t" * 3 + "Name of Element: " + str(get_element_name) + "\t" * 3 + "Name of Host: " + str(string_host))
        except:
            pass
    # output.print_table(table_data=data,
    #                 title="List Host",
    #                 columns=["Element Id","Name of Element", "Name of Host"],
    #                 formats=['', '', ''])

