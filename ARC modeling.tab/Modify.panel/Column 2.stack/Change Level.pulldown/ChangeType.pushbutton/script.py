# -*- coding: utf-8 -*-
#pylint: disable=E0401,W0703,W0613
import re
from pyrevit import coreutils
from pyrevit import revit, DB
from pyrevit import forms
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

def ChangeType(element, typeId):
    try:
        element.ChangeTypeId(typeId)
        return element
    except:
        pass

def unique_values(lst):
    seen = set()
    unique_list = []
    for item in lst:
        if item not in seen:
            unique_list.append(item)
            seen.add(item)
    return unique_list

def get_family(idoc):
    list_family = []
    collector = DB.FilteredElementCollector(idoc).OfClass(DB.Family)
    for __family in collector:
        list_family.append(__family)
    return list_family

def get_family_by_category(idoc, category):
    list_family = []
    collector = DB.FilteredElementCollector(idoc).OfClass(DB.Family)
    for __family in collector:
        family_category = __family.FamilyCategory
        if str(family_category) == str(category):
            list_family.append(family_category)
    return list_family

def get_family_types(idoc,family_name):
    collector = DB.FilteredElementCollector(idoc).OfClass(DB.Family)
    for family in collector:
        if family.Name == family_name:
            family_types = family.GetFamilySymbolIds()
            return [idoc.GetElement(ftype) for ftype in family_types]
    return []

def find_type_by_family_and_type_name(idoc,family_name, __type_name):
    danh_sach_type = get_family_types(idoc,family_name)
    for moi_type in danh_sach_type:
        name = module.get_builtin_parameter_by_name(moi_type, DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
        if name == __type_name:
            return moi_type
        
def find_type_by_type_name(idoc,ele_dau_vao, __type_name):
    family_name = revit.db.query.get_family_name(ele_dau_vao)
    danh_sach_type = get_family_types(idoc,family_name)
    for moi_type in danh_sach_type:
        name = module.get_builtin_parameter_by_name(moi_type, DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
        if name == __type_name:
            return moi_type

class ReValueItem(object):
    def __init__(self, eid, oldvalue, final=False):
        self.eid = eid
        self.oldvalue = oldvalue
        self.newvalue = ''
        self.final = final
        self.tooltip = ''
        self.check_type = ''

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
                    
                    get_element = doc.GetElement(self.eid)
                    # check = find_type_by_family_and_type_name(doc,"RC大梁", str(self.newvalue))
                    check = find_type_by_type_name(doc,get_element, str(self.newvalue))
                    if str(self.oldvalue) == str(self.newvalue):
                        self.check_type = "Nothing changes"
                    elif check:
                        self.check_type = "Ready"
                    else:
                        self.check_type = "Type is not available"

            else:
                self.tooltip = 'No Conversion Specified'
                self.newvalue = ''
                self.check_type = ''
        except Exception:
            self.newvalue = ''
            self.check_type = ''

class ReValueWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        # create pattern maker window and process options
        forms.WPFWindow.__init__(self, xaml_file_name)
        self._target_elements = module.get_elements(uidoc, doc, 'Select Element', noti = False)
        self._reset_preview()
        self._setup_params()


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
    
    def _setup_params(self):
        # family_name = []
        # all_categories = []
        # danh_sach_ele = self._target_elements
        # for __tung_ele in danh_sach_ele:
        #     try:
        #         all_categories.append(str(__tung_ele.Category))
        #     except:
        #         pass
        # set_category = unique_values(all_categories)
        # # print set_category
        # if len(set_category) == 1:
        #     all_family_by_catgory = get_family_by_category(doc, str(set_category[0]))
        #     for __moi_family in all_family_by_catgory:
        #         family_name.append(__moi_family.Name)
        #     self.params_cb.ItemsSource = family_name
        #     self.params_cb.SelectedIndex = 0
        # else:
        #     all_family = get_family(doc)
        #     for __tung_family in all_family:
        #         family_name.append(__tung_family.Name)
            self.params_cb.ItemsSource = ["Giá trị nháp thôi, đặt tên gì cũng được"]
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
            old_value = revit.query.get_name(element)
            newitem = ReValueItem(eid=element.Id, oldvalue=old_value)
            newitem.format_value(self.old_format,
                                 self.new_format)

            self._revalue_items.append(newitem)
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

    def apply_new_values(self, sender, args):
        t = DB.Transaction (doc, "Change Level Type")
        t.Start()        
        
        for item,tung_element in zip(self._revalue_items,self._target_elements):
            try:
                type_name = item.newvalue
                # xac_dinh_type = find_type_by_family_and_type_name(doc,"RC大梁", str(type_name))
                xac_dinh_type = find_type_by_type_name(doc,tung_element, str(type_name))
                check = item.check_type
                if str(check) == "Ready":
                    doi_type = ChangeType(tung_element, xac_dinh_type.Id)
            except:
                pass
        self.Close()
        t.Commit()

ReValueWindow('changetype.xaml').show(modal=True)
