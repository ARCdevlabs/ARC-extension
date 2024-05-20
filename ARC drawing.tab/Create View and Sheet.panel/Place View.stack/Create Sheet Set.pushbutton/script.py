# -*- coding: utf-8 -*-
"""Tạo sheet set"""

from pyrevit import framework
from pyrevit import revit, script, DB, UI
from pyrevit import forms



# Get printmanager / viewsheetsetting
printmanager = revit.doc.PrintManager
printmanager.PrintRange = DB.PrintRange.Select
viewsheetsetting = printmanager.ViewSheetSetting

# Collect existing ViewSheetSets
print_sets_existing = DB.FilteredElementCollector(revit.doc)\
    .WhereElementIsNotElementType().OfClass(DB.ViewSheetSet).ToElements()
print_sets_names_existing = [vs.Name for vs in print_sets_existing if vs.Name]

# Collect selected views
selected_views = forms.select_views(use_selection=True,
    filterfunc=lambda v: not isinstance(v, DB.ViewSheet)
                         or not v.IsPlaceholder)

if selected_views:
    myviewset = DB.ViewSet()
    for el in selected_views:
        myviewset.Insert(el)

    if myviewset.IsEmpty:
        forms.alert('Chọn ít nhất một sheet')
    else:
        # Ask for a print set name and check if need to be replaced
        sheetsetname = None
        while not sheetsetname\
                or (sheetsetname in print_sets_names_existing
                and not forms.alert("Trùng tên rồi, thay thế Sheet set có sẵn không?",
                                yes=True, no=True)):
            sheetsetname = forms.ask_for_string(
                default=print_sets_names_existing[-1]\
                    if print_sets_names_existing else 'ViewPrintSet',
                prompt="Đặt tên cho sheet set")
            if not sheetsetname:
                script.exit()

        # Collect existing sheet sets
        viewsheetsets = DB.FilteredElementCollector(revit.doc)\
                          .OfClass(framework.get_type(DB.ViewSheetSet))\
                          .WhereElementIsNotElementType()\
                          .ToElements()

        allviewsheetsets = {vss.Name: vss for vss in viewsheetsets}

        with revit.Transaction('Tạo sheet set'):
            # Delete existing matching sheet set
            if sheetsetname in allviewsheetsets.keys():
                viewsheetsetting.CurrentViewSheetSet = \
                    allviewsheetsets[sheetsetname]
                viewsheetsetting.Delete()

            # Create new sheet set
            viewsheetsetting.CurrentViewSheetSet.Views = myviewset
            viewsheetsetting.SaveAs(sheetsetname)
