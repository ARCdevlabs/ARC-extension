"""Pins all viewports on selected sheets.

Shift-Click:
Pin all viewports on active sheet.
"""

from pyrevit import revit, DB, EXEC_PARAMS
from pyrevit import script
from pyrevit import forms
from nances import selection

def select_viewports(sheet_list):
    list_view_port = []
    for sheet in sheet_list:
        for vportid in sheet.GetAllViewports():
            vport = revit.doc.GetElement(vportid)
            list_view_port.append(vport)
    return list_view_port

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
if EXEC_PARAMS.config_mode:
    if isinstance(revit.active_view, DB.ViewSheet):
        sel_sheets = [revit.active_view]
    else:
        forms.alert('Active view must be a sheet.')
        script.exit()
else:
    sel_sheets = forms.select_sheets(title='Select Sheets',
                                     use_selection = True,
                                     include_placeholder=False)


if sel_sheets:
    selection.select_sau_khi_chay_tool(select_viewports(sel_sheets), uidoc)