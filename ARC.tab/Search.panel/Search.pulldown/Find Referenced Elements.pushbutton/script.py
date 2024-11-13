# -*- coding: utf-8 -*-
#pylint: disable=import-error,invalid-name
from pyrevit import script
from pyrevit import revit, DB
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

    def get_dependent (idoc, element):
        get_dependent_element = element.GetDependentElements(None)
        data = []  
        for tung_nhom_doi_tuong in get_dependent_element:
            ele_id = tung_nhom_doi_tuong
            get_element = idoc.GetElement(ele_id)
            element_link = output.linkify(ele_id)
            get_type = get_element.GetType().Name
            if hasattr(get_element, "OwnerViewId"):
                owner_view = idoc.GetElement(get_element.OwnerViewId)
                if hasattr(owner_view, "Name"):
                    owner_view_name = owner_view.Name
                    view_link = output.linkify(owner_view.Id)
                else:
                    view_link = "None"
                    owner_view_name = "None"
            else:
                view_link = "None"
                owner_view_name = "None"

            if isinstance(element, DB.FamilyInstance):
                data.append((element_link, ("Type: {}".format(get_type)), view_link , owner_view_name))
            else:
                data.append((element_link, ("Type: {}".format(get_type)), view_link , owner_view_name))

        output.print_table(table_data=data,
                        title="List Reference Elements",
                        columns=["Element Id", "Type", "Owner View Id", "View Name"],
                        formats=['', '','',''])
        return

    output = script.get_output()

    element = []

    selected_element = get_selected_elements(uidoc,doc)

    if len(selected_element) == 0:
        from rpw.ui.forms import SelectFromList
        value = SelectFromList('Select Option', ['Pick Element','Active View'])
        if value == "Active View":
            element.append(active_view)
        else:
            with forms.WarningBar(title="Pick 1 Element"):
                try:
                    pick = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element)
                    element.append(doc.GetElement(pick.ElementId))
                except:
                    sys.exit(0) 
    else:
        element = selected_element

    for tung_element in element:
        get_dependent (doc, tung_element)


