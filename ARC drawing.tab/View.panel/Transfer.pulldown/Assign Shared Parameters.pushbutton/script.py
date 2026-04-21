# -*- coding: utf-8 -*-
from pyrevit import forms, script, revit, DB
import clr
import System
import os
import codecs

# Import Revit API
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

try:
    REVIT_VERSION = int(app.VersionNumber)
except:
    REVIT_VERSION = 2022

IS_NEW_REVIT = REVIT_VERSION >= 2024

GROUP_NAMES = [
    "Constraints", "Construction", "Data", "Dimensions",
    "Fire Protection", "General", "Graphics", "Identity Data",
    "Layers", "Materials and Finishes", "Model Properties", "Other", 
    "Plumbing", "Structural", "Title Text", "Text", "Visibility"
]

def get_group_mapping():
    mapping = {}
    if IS_NEW_REVIT:

        mapping = {
            "Constraints": GroupTypeId.Constraints,
            "Construction": GroupTypeId.Construction,
            "Data": GroupTypeId.Data,
            "Dimensions": GroupTypeId.Geometry,
            "Fire Protection": GroupTypeId.FireProtection,
            "General": GroupTypeId.General,
            "Graphics": GroupTypeId.Graphics,
            "Identity Data": GroupTypeId.IdentityData,
            "Layers": GroupTypeId.RebarSystemLayers,
            "Model Properties": GroupTypeId.AdskModelProperties,
            "Plumbing": GroupTypeId.Plumbing,
            "Structural": GroupTypeId.Structural,
            "Title Text": GroupTypeId.Title,
            "Text": GroupTypeId.Text,
            "Visibility": GroupTypeId.Visibility
        }
        

        if hasattr(GroupTypeId, 'MaterialAndFinishes'):
            mapping["Materials and Finishes"] = GroupTypeId.MaterialAndFinishes
        elif hasattr(GroupTypeId, 'MaterialFinishes'):
            mapping["Materials and Finishes"] = GroupTypeId.MaterialFinishes
        else:
            mapping["Materials and Finishes"] = GroupTypeId.General

        if hasattr(GroupTypeId, 'Other'):
            mapping["Other"] = GroupTypeId.Other
        else:
            mapping["Other"] = ForgeTypeId() 
    else:

        mapping = {
            "Constraints": BuiltInParameterGroup.PG_CONSTRAINTS,
            "Construction": BuiltInParameterGroup.PG_CONSTRUCTION,
            "Data": BuiltInParameterGroup.PG_DATA,
            "Dimensions": BuiltInParameterGroup.PG_GEOMETRY,
            "Fire Protection": BuiltInParameterGroup.PG_FIRE_PROTECTION,
            "General": BuiltInParameterGroup.PG_GENERAL,
            "Graphics": BuiltInParameterGroup.PG_GRAPHICS,
            "Identity Data": BuiltInParameterGroup.PG_IDENTITY_DATA,
            "Layers": BuiltInParameterGroup.PG_REBAR_SYSTEM_LAYERS,
            "Materials and Finishes": BuiltInParameterGroup.PG_MATERIALS, # Cập nhật Group cũ
            "Model Properties": BuiltInParameterGroup.PG_ADSK_MODEL_PROPERTIES,
            "Plumbing": BuiltInParameterGroup.PG_PLUMBING,
            "Structural": BuiltInParameterGroup.PG_STRUCTURAL,
            "Title Text": BuiltInParameterGroup.PG_TITLE,
            "Text": BuiltInParameterGroup.PG_TEXT,
            "Visibility": BuiltInParameterGroup.PG_VISIBILITY
        }
        if hasattr(BuiltInParameterGroup, 'PG_OTHER'):
            mapping["Other"] = BuiltInParameterGroup.PG_OTHER
        else:
            mapping["Other"] = BuiltInParameterGroup.INVALID
            
    return mapping

GROUP_MAPPING = get_group_mapping()

def get_param_group_from_def(definition):
    if IS_NEW_REVIT:
        return definition.GetGroupTypeId()
    else:
        return definition.ParameterGroup

def get_label_for_group(group_obj):
    try:
        val = LabelUtils.GetLabelFor(group_obj)
        if val: return val
    except: pass
    if IS_NEW_REVIT:
        try:
            raw_id = group_obj.TypeId
            if ":" in raw_id: raw_id = raw_id.split(":")[-1]
            if "-" in raw_id: raw_id = raw_id.split("-")[0]
            return raw_id.replace("_", " ").title()
        except:
            return str(group_obj)
    return str(group_obj)

class ParamItem(object):
    def __init__(self, name, group, p_type):
        self.Name = name
        self.Group = group
        self.ParamType = p_type 
        self.IsChecked = False

class CategoryOption(object):
    def __init__(self, category):
        self.Name = category.Name
        self.Category = category
        self.IsChecked = False

class SearchWindow(forms.WPFWindow):
    def __init__(self, xaml_file):
        forms.WPFWindow.__init__(self, xaml_file)
        self.is_family_doc = doc.IsFamilyDocument
        self.all_params = []
        self.load_shared_params_smart()
        
        if self.is_family_doc:
            self.category_lb.IsEnabled = False
            self.cat_search_tb.IsEnabled = False
            self.btn_check_all.IsEnabled = False
            self.btn_check_none.IsEnabled = False
            self.category_group_box.Header = "3. Select Categories (Not required for Family)"
        else:
            self.all_categories = []
            self.load_categories()
            self.btn_check_all.Click += self.check_all_click
            self.btn_check_none.Click += self.check_none_click
        
        self.group_cb.ItemsSource = GROUP_NAMES
        self.group_cb.SelectedIndex = 2
        self.search_name_tb.Focus()

    def load_shared_params_smart(self):
        sp_filename = app.SharedParametersFilename
        if not sp_filename or not os.path.exists(sp_filename):
            self.status_lb.Text = "Error: Shared Parameters file is not linked."
            return
        encodings = ['utf-16', 'utf-8-sig', 'utf-8', 'mbcs']
        lines = []
        for enc in encodings:
            try:
                with codecs.open(sp_filename, 'r', encoding=enc) as f:
                    temp_lines = f.readlines()
                if "GROUP" in "".join(temp_lines[:20]) or "PARAM" in "".join(temp_lines[:20]):
                    lines = temp_lines
                    break
            except: continue
        if not lines:
            self.status_lb.Text = "File encoding error."
            return
        try:
            group_map = {}
            temp_params = []
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'): continue
                parts = line.split('\t')
                if "GROUP" in parts[0] and len(parts) >= 3:
                    group_map[parts[1].strip()] = parts[2].strip()
                elif "PARAM" in parts[0] and len(parts) >= 6:
                    p_name = parts[2].strip()
                    raw_type = parts[3].strip()
                    p_type = raw_type.replace('_', ' ').title()
                    g_name = group_map.get(parts[5].strip(), "Unknown")
                    temp_params.append(ParamItem(p_name, g_name, p_type))
            
            temp_params.sort(key=lambda x: (x.Group, x.Name))
            self.all_params = temp_params
            self.result_dg.ItemsSource = self.all_params
            count = len(self.all_params)
            msg = "Family Mode" if self.is_family_doc else "Project Mode"
            self.status_lb.Text = "{}: {} parameters.".format(msg, count)
        except Exception as e:
            self.status_lb.Text = "Data error:" + str(e)

    def search_box_changed(self, sender, args):
        name_kw = self.search_name_tb.Text.lower()
        group_kw = self.search_group_tb.Text.lower()
        filtered = []
        for p in self.all_params:
            if name_kw and (name_kw not in p.Name.lower()): continue
            if group_kw and (group_kw not in p.Group.lower()): continue
            filtered.append(p)
        filtered.sort(key=lambda x: (x.Name, x.Group))
        self.result_dg.ItemsSource = filtered

    def param_checkbox_click(self, sender, args):
        try:
            cb = sender
            is_checked = cb.IsChecked 
            current_item = cb.DataContext
            selected_items = self.result_dg.SelectedItems
            if selected_items and current_item in selected_items and selected_items.Count > 1:
                for item in selected_items:
                    item.IsChecked = is_checked
                self.result_dg.Items.Refresh()
        except Exception as e:
            print("Checkbox Error: " + str(e))

    def check_all_param_click(self, sender, args):
        current_list = self.result_dg.ItemsSource
        if current_list:
            for item in current_list:
                item.IsChecked = True
            self.result_dg.Items.Refresh()

    def check_none_param_click(self, sender, args):
        current_list = self.result_dg.ItemsSource
        if current_list:
            for item in current_list:
                item.IsChecked = False
            self.result_dg.Items.Refresh()

    def load_categories(self):
        cats = doc.Settings.Categories
        cat_list = []
        for cat in cats:
            if cat.AllowsBoundParameters and cat.CategoryType == CategoryType.Model:
                cat_list.append(CategoryOption(cat))
        self.all_categories = sorted(cat_list, key=lambda x: x.Name)
        self.category_lb.ItemsSource = self.all_categories

    def cat_search_changed(self, sender, args):
        if self.is_family_doc: return
        keyword = self.cat_search_tb.Text.lower()
        if not keyword: self.category_lb.ItemsSource = self.all_categories
        else:
            filtered = [c for c in self.all_categories if keyword in c.Name.lower()]
            self.category_lb.ItemsSource = filtered

    def check_all_click(self, sender, args):
        for item in self.category_lb.ItemsSource: item.IsChecked = True
        self.category_lb.Items.Refresh()

    def check_none_click(self, sender, args):
        for item in self.all_categories: item.IsChecked = False
        self.category_lb.Items.Refresh()

    def get_definition_by_name(self, param_name):
        try:
            sp_file = app.OpenSharedParameterFile()
            if not sp_file: return None
            for group in sp_file.Groups:
                for definition in group.Definitions:
                    if definition.Name == param_name: return definition
            return None
        except: return None

    def add_parameter_logic(self, is_instance):
        checked_items = [p for p in self.all_params if p.IsChecked]
        if not checked_items:
            print(u"❌ Error: No parameters checked (Please tick checkboxes)!")
            return
        selected_group_name = self.group_cb.SelectedItem
        default_grp = GroupTypeId.Data if IS_NEW_REVIT else BuiltInParameterGroup.PG_DATA
        target_group = GROUP_MAPPING.get(selected_group_name, default_grp)
        t_name = "Shared Parameter Assignment"
        script.get_output().show()
        try:
            with revit.Transaction(t_name):
                if self.is_family_doc:
                    fam_mgr = doc.FamilyManager
                    fam_target_group = target_group
                    if selected_group_name == "Other":
                        if IS_NEW_REVIT:
                            fam_target_group = ForgeTypeId() 
                        else:
                            fam_target_group = BuiltInParameterGroup.INVALID
                    for item in checked_items:
                        p_name = item.Name
                        definition = self.get_definition_by_name(p_name)
                        if not definition:
                            print(u"{} - {} - ❌ Error: Definition not found!".format(p_name, selected_group_name))
                            continue
                        existing_param = fam_mgr.get_Parameter(p_name)
                        if existing_param:
                            exist_grp_obj = get_param_group_from_def(existing_param.Definition)
                            exist_group_label = get_label_for_group(exist_grp_obj)
                            print(u"{} - {}".format(p_name, selected_group_name))
                            print(u" ⚠️ Already exists in Group - {} => Skipped".format(exist_group_label))
                        else:
                            try:
                                fam_mgr.AddParameter(definition, fam_target_group, is_instance)
                                print(u"{} - {}".format(p_name, selected_group_name))
                                print(u" ✔ Assigned to Parameter Group - {}".format(selected_group_name))
                            except Exception as e:
                                print(u"{} - {} - ❌ Add failed: {}".format(p_name, selected_group_name, str(e)))
                else:
                    selected_cats = [item.Category for item in self.all_categories if item.IsChecked]
                    if not selected_cats:
                        print(u"❌ Error: No categories selected!")
                        return
                    dest_cat_names = ", ".join([c.Name for c in selected_cats])
                    for item in checked_items:
                        p_name = item.Name
                        definition = self.get_definition_by_name(p_name)
                        if not definition:
                            print(u"{} - ❌ Definition Not Found".format(p_name))
                            continue
                        existing_binding = None
                        if doc.ParameterBindings.Contains(definition):
                            existing_binding = doc.ParameterBindings[definition]
                        if existing_binding:
                            is_exist_instance = isinstance(existing_binding, InstanceBinding)
                            if is_instance != is_exist_instance:
                                exist_type_str = "Instance" if is_exist_instance else "Type"
                                req_type_str = "Instance" if is_instance else "Type"
                                print(u"{} - {}".format(p_name, selected_group_name))
                                print(u" ⚠️ Binding type mismatch: Current [{}] ! Required [{}] -> Skipped".format(exist_type_str, req_type_str))
                                continue
                            sp_elem = SharedParameterElement.Lookup(doc, definition.GUID)
                            real_group_obj = sp_elem.GetDefinition().GetGroupTypeId() if (sp_elem and IS_NEW_REVIT) else (get_param_group_from_def(definition))
                            is_group_match = False
                            if IS_NEW_REVIT:
                                try:
                                    if real_group_obj.TypeId == target_group.TypeId: is_group_match = True
                                except:
                                    if str(real_group_obj) == str(target_group): is_group_match = True
                            else:
                                if real_group_obj == target_group: is_group_match = True
                            if not is_group_match:
                                real_group_label = get_label_for_group(real_group_obj)
                                print(u"{} - {}".format(p_name, selected_group_name))
                                print(u" ⚠️ Group mismatch: Current [{}] ! Required [{}] -> Skipped".format(real_group_label, selected_group_name))
                                continue
                            current_cat_set = existing_binding.Categories
                            new_cat_set = app.Create.NewCategorySet()
                            for c in current_cat_set: new_cat_set.Insert(c)
                            added_cat_names = []
                            for c in selected_cats:
                                if not new_cat_set.Contains(c):
                                    new_cat_set.Insert(c)
                                    added_cat_names.append(c.Name)
                            if not added_cat_names:
                                print(u"{} - {}".format(p_name, selected_group_name))
                                print(u" ℹ️ All selected categories already exist → No changes applied.")
                                continue
                            new_binding = app.Create.NewInstanceBinding(new_cat_set) if is_instance else app.Create.NewTypeBinding(new_cat_set)
                            try:
                                doc.ParameterBindings.ReInsert(definition, new_binding, target_group)
                                print(u"{} - {}".format(p_name, selected_group_name))
                                print(u" 🔄 UPDATED: Reassigned to Category [{}]".format(", ".join(added_cat_names)))
                            except Exception as e:
                                print(u"{} - ❌ ReInsert error: {}".format(p_name, str(e)))
                        else:
                            cat_set = app.Create.NewCategorySet()
                            for c in selected_cats: cat_set.Insert(c)
                            binding = app.Create.NewInstanceBinding(cat_set) if is_instance else app.Create.NewTypeBinding(cat_set)
                            try:
                                doc.ParameterBindings.Insert(definition, binding, target_group)
                                print(u"{} - {}".format(p_name, selected_group_name))
                                print(u" ✔ Assigned to Category [{}]".format(dest_cat_names))
                            except Exception as e:
                                print(u"{} - ❌ Insert error: {}".format(p_name, str(e)))
            self.status_lb.Text = "Parameter Assignment Completed!!!"
        except Exception as e:
            print(u"❌ Transaction Critical Error: " + str(e))

    def add_instance_click(self, sender, args):
        self.add_parameter_logic(is_instance=True)

    def add_type_click(self, sender, args):
        self.add_parameter_logic(is_instance=False)

if __name__ == '__main__':
    xaml_path = script.get_bundle_file('InputSharePara.xaml')
    if os.path.exists(xaml_path):
        window = SearchWindow(xaml_path)
        window.ShowDialog()