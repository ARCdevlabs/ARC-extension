# -*- coding: utf-8 -*-
"""Tao hang loat view"""
import string
import codecs
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
from pyrevit import revit, DB
from nances import forms
from pyrevit import script
# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
logger = script.get_logger()

def duplicableview(view):
    return view.CanViewBeDuplicated(DB.ViewDuplicateOption.Duplicate)


def duplicate_views(viewlist, dupop):
    dup_view_ids = []
    with revit.Transaction('Duplicate views đã chọn'):
        for el in viewlist:
            try:
                dup_view_ids.append(el.Duplicate(dupop))
            except Exception as duplerr:
                logger.error('Lỗi trong quá trình duplicate views "{}" | {}'
                             .format(revit.query.get_name(el), duplerr))
        if dup_view_ids:
            revit.doc.Regenerate()
    return dup_view_ids

selected_views = forms.select_views(filterfunc=duplicableview,
                                    use_selection=True)

trans_group = TransactionGroup(doc, 'Duplicate View')
trans_group.Start()

try:
    if selected_views:
        selected_option = \
            forms.CommandSwitchWindow.show(
                ['Whit Detailing',
                'Whitout Detailing',
                'As Dependent'],
                message='Chọn option khi duplicate'
                )
        from rpw.ui.forms import TextInput
        input = TextInput('Number of duplicate views', default="1")
        input_value = input

        so_luong = round(float(input_value),0)
        n = 1 
        checking = True
        while checking == True:
            if selected_option:
                dupop = DB.ViewDuplicateOption.AsDependent
                if selected_option == 'Whit Detailing':
                    dupop = DB.ViewDuplicateOption.WithDetailing
                if selected_option == 'Whitout Detailing':
                    dupop = DB.ViewDuplicateOption.Duplicate
                if selected_option == 'As Dependent':
                    dupop = DB.ViewDuplicateOption.AsDependent
                dup_view_ids = duplicate_views(
                    selected_views,dupop)
                if dup_view_ids:
                    revit.get_selection().set_to(dup_view_ids)
            n += 1
            if n > so_luong:
                checking = False
    trans_group.Assimilate()
except:
    trans_group.RollBack                
