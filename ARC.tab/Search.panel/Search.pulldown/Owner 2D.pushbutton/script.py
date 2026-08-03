# -*- coding: utf-8 -*-
from pyrevit import script
import Autodesk
import nances
import traceback
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
if nances.AutodeskData():
    def tim_view_chua_doi_tuong_2D (idoc, element):
        output = script.get_output()
        data = []  

        list_element_id_link = []
        list_element_name = []
        list_view_id_link = []
        list_view_name = []
        for tung_element in element:

            owner_view = tung_element.OwnerViewId
            
            view = doc.GetElement((owner_view))

            element_link = output.linkify(tung_element.Id)

            get_type_name = nances.get_builtin_parameter_by_name(tung_element,BuiltInParameter.ELEM_TYPE_PARAM).AsValueString()

            view_link = output.linkify(view.Id)

            owner_view_name = view.Name

            list_element_id_link.append(element_link)
            list_element_name.append(get_type_name)
            list_view_id_link.append(view_link)
            list_view_name.append(owner_view_name)

        data_goc = zip(list_element_id_link,list_element_name,list_view_id_link,list_view_name)            
        data = sorted(data_goc, key=lambda x: x[3])

        output.print_table(table_data=data,
                        title="List View Chứa 2D Elements",
                        columns=["Element Id", "Type Name", "Owner View Id", "View Name"],
                        formats=['', '','',''])
        return
    
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Ele = nances.get_selected_elements(uidoc,doc)
    if not Ele:
        import sys
        sys.exit()

    tim_view_chua_doi_tuong_2D (doc, Ele)


