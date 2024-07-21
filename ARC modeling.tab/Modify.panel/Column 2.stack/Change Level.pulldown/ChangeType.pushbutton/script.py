# -*- coding: utf-8 -*-
"""Reformat parameter string values (Super handy for renaming elements)"""
#pylint: disable=E0401,W0703,W0613
import re

from pyrevit import coreutils
from pyrevit import revit, DB
from pyrevit import forms
# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType

import traceback
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document


class ReValueItem(object):
    def __init__(self, eid, oldvalue, final=False):
        self.eid = eid
        self.oldvalue = oldvalue
        self.newvalue = ''
        self.final = final
        self.tooltip = ''
        # self.check_type = ''

    def format_value(self, from_pattern, to_pattern):
        try:
            if to_pattern is None:
                to_pattern = ""

            if from_pattern:
                # if format contains pattern finders use reformatter
                if any(x in from_pattern for x in ['{', '}']):
                    self.newvalue = \
                        coreutils.reformat_string(self.oldvalue,
                                                  from_pattern,
                                                  to_pattern)
                    self.tooltip = '{} --> {}'.format(from_pattern, to_pattern)
                # otherwise use a simple find/replacer
                else:
                    self.newvalue = \
                        re.sub(from_pattern, to_pattern, self.oldvalue)
            else:
                self.tooltip = 'No Conversion Specified'
                self.newvalue = ''
        except Exception:
            self.newvalue = ''


def ChangeType(element, typeId):
    try:
        element.ChangeTypeId(typeId)
        return element
    except:
        pass

class CheckType():
    def __init__(self):
        self.check_type = ''
    
    def ket_qua_check_type(self, ket_qua):
        self.check_type = ket_qua


def get_family_types(idoc,family_name):
    # Tạo một bộ lọc để lấy tất cả các đối tượng thuộc category Families
    collector = DB.FilteredElementCollector(idoc).OfClass(DB.Family)

    # Duyệt qua tất cả các đối tượng family
    for family in collector:
        if family.Name == family_name:
            # Lấy tất cả các loại của family
            family_types = family.GetFamilySymbolIds()
            return [idoc.GetElement(ftype) for ftype in family_types]
    return []


def find_type_by_family_and_type_name(idoc,family_name, __type_name):
    danh_sach_type = get_family_types(idoc,family_name)
    for moi_type in danh_sach_type:
        name = module.get_builtin_parameter_by_name(moi_type, DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
        if name == __type_name:
            return moi_type


class ReValueWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        # create pattern maker window and process options
        forms.WPFWindow.__init__(self, xaml_file_name)
        self._target_elements = module.get_elements(uidoc, doc, 'Select Element', noti = False)
        self._reset_preview()
        self._setup_params()
        # self.check_type
        # self.ket_qua_check_type("ket qua")

    @property
    def selected_param(self):
        return self.params_cb.SelectedItem

    @property
    def old_format(self):
        return self.orig_format_tb.Text

    @old_format.setter
    def old_format(self, value):
        self.orig_format_tb.Text = value

    @property
    def new_format(self):
        return self.new_format_tb.Text
    
    @property
    def preview_items(self):
        return self.preview_dg.ItemsSource

    @property
    def selected_preview_items(self):
        return self.preview_dg.SelectedItems
    

    # def ket_qua_check_type(self, ket_qua):
    #     self.check_type = ket_qua

    def _setup_params(self):
        unique_params = set()
        for element in self._target_elements:
            # grab element parameters
            for param in element.Parameters:
                if not param.IsReadOnly \
                        and param.StorageType == DB.StorageType.String:
                    unique_params.add(param.Definition.Name)

        all_params = ['Name', 'Family: Name']
        all_params.extend(sorted(list(unique_params)))
        self.params_cb.ItemsSource = all_params
        self.params_cb.SelectedIndex = 0

    def _reset_preview(self):
        self._revalue_items = []
        self.preview_dg.ItemsSource = self._revalue_items

    def _refresh_preview(self):
        self.preview_dg.Items.Refresh()

    def on_param_change(self, sender, args):
        self._reset_preview()
        for element in self._target_elements:
            old_value = ''
            if self.selected_param == 'Name':
                old_value = revit.query.get_name(element)
            elif self.selected_param == 'Family: Name':
                if hasattr(element, 'Family') and element.Family:
                    old_value = revit.query.get_name(element.Family)
            else:
                param = element.LookupParameter(self.selected_param)
                if param:
                    old_value = param.AsString()

            newitem = ReValueItem(eid=element.Id, oldvalue=old_value)
            newitem.format_value(self.old_format,
                                 self.new_format)
            

            
            # # Kiểm tra có type hay không?
            # for tung_item in self._revalue_items:
            #     tim_type_name = tung_item.newvalue
            #     type = find_type_by_family_and_type_name(doc,"S_G_H_3Sec", str(tim_type_name))
            #     if str(type) != "None":
            #         newitem.ket_qua_check_type("Đã có sẵn type")
            #     else:
            #         newitem.ket_qua_check_type("Chưa có sẵn type")

            # self._revalue_items.append(newitem)

        self._refresh_preview()

    def on_format_change(self, sender, args):
        for item in self._revalue_items:
            if not item.final:
                item.format_value(self.old_format,
                                  self.new_format)
        self._refresh_preview()

    def on_selection_change(self, sender, args):
        if self.preview_dg.SelectedItems.Count == 1 \
                and not self.new_format:
            self.old_format = self.preview_dg.SelectedItem.oldvalue

    def mark_as_final(self, sender, args):
        selected_names = [x.eid for x in self.selected_preview_items]
        for item in self._revalue_items:
            if item.eid in selected_names:
                item.final = True
        self._refresh_preview()

    # def apply_new_values(self, sender, args):
    #     self.Close()
    #     try:
    #         with revit.Transaction('ReValue {}'.format(self.selected_param),
    #                                log_errors=False):
    #             for item in self._revalue_items:
    #                 if item.newvalue:
    #                     element = revit.doc.GetElement(item.eid)
    #                     if self.selected_param == 'Name':
    #                         element.Name = item.newvalue
    #                     elif self.selected_param == 'Family: Name':
    #                         if element.Family:
    #                             element.Family.Name = item.newvalue
    #                     else:
    #                         param = element.LookupParameter(self.selected_param)
    #                         if param:
    #                             param.Set(item.newvalue)
    #     except Exception as ex:
    #         forms.alert(str(ex), title='Error')

    def apply_new_values(self, sender, args):
        t = DB.Transaction (doc, "Change Level Type")
        t.Start()
        
        thu_check_type = CheckType()
        

        for item,tung_element in zip(self._revalue_items,self._target_elements):
            try:
                type_name = item.newvalue
                xac_dinh_type = find_type_by_family_and_type_name(doc,"S_G_H_3Sec", str(type_name))
                if xac_dinh_type:
                    thu_check_type.ket_qua_check_type("Đã có thai")
                    doi_type = ChangeType(tung_element, xac_dinh_type.Id)
                else:
                    thu_check_type.ket_qua_check_type("Chưa có type")
            except:
                pass
        t.Commit()

ReValueWindow('changetype.xaml').show(modal=True)
