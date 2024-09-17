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
    output = script.get_output()
    from rpw.ui.forms import SelectFromList
    value = SelectFromList('Select Option', ['Pick Element','Active View'])
    if value == "Active View":
        element = active_view
    else:
        with forms.WarningBar(title="Pick 1 Element"):
            try:
                pick = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element)
                element = doc.GetElement(pick.ElementId)
            except:
                sys.exit(0) 
    get_dependent_element = element.GetDependentElements(None)
    data = []  
    for tung_nhom_doi_tuong in get_dependent_element:
        ele_id = tung_nhom_doi_tuong
        get_element = doc.GetElement(ele_id)
        element_link = output.linkify(ele_id)
        get_type = get_element.GetType().Name
        if hasattr(get_element, "OwnerViewId"):
            owner_view = doc.GetElement(get_element.OwnerViewId)
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

