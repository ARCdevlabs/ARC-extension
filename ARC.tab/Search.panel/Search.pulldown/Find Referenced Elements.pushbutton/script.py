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
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    output = script.get_output()
    with forms.WarningBar(title="Pick 1 Element"):
        try:
            pick = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element)
        except:
            sys.exit(0)

    element = doc.GetElement(pick.ElementId)
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



# # from pyrevit import script

# # output = script.get_output()

# # data = [['结构', '结构', '结构结构', 80],
# #         ['结构', '结构', '结构', 45],
# #         ['row3', 'data', 'data', 45],
# #         ['结构结构', 'data', '结构', 45]]

# # # formats contains formatting strings for each column
# # # last_line_style contains css styling code for the last line
# # output.print_table(table_data=data,
# #                    title="Example Table",
# #                    columns=["Row Name", "Column 1", "Column 2", "Percentage"],
# #                    formats=['', '', '', '{}%'],
# #                    last_line_style='color:red;')





# #pylint: disable=import-error,invalid-name
# from pyrevit import script
# from pyrevit import revit, DB


# selection = revit.get_selection()
# output = script.get_output()


# if not selection.is_empty:
#     print("Searching for all objects tied to ELEMENT ID: {0}..."
#           .format(selection.first.Id))
#     with revit.DryTransaction("Search for linked elements"):
#         linked_elements_list = revit.doc.Delete(selection.first.Id)

#     for elId in linked_elements_list:
#         el = revit.doc.GetElement(elId)
#         if el and elId in selection.element_ids:
#             elid_link = output.linkify(elId)
#             print("ID: {}\t\tTYPE: {} ( selected object )"
#                   .format(elid_link, el.GetType().Name))
#         elif el:
#             elid_link = output.linkify(elId)
#             if isinstance(el, DB.FamilyInstance):
#                 family_name = revit.query.get_family_name(el)
#                 symbol_name = revit.query.get_symbol_name(el)
#                 print("ID: {}\t\tTYPE: {} ({}) --> {}:{}"
#                       .format(elid_link,
#                               el.GetType().Name,
#                               el.Category.Name,
#                               family_name,
#                               symbol_name))
#             else:
#                 print("ID: {}\t\tTYPE: {}"
#                       .format(elid_link, el.GetType().Name))
