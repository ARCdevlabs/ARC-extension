# -*- coding: utf-8 -*-

from pyrevit import forms, script, revit, DB
import clr
import System
import os
import io
import uuid


clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application


try:
    REVIT_VERSION = int(app.VersionNumber)
except:
    REVIT_VERSION = 2022

IS_NEW_REVIT = REVIT_VERSION >= 2024

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
    
    return str(group_obj).replace("PG_", "").title()

def get_param_type_string(definition):

    try:
        if IS_NEW_REVIT:
            type_id = definition.GetDataType() # ForgeTypeId
            type_str = type_id.TypeId 
            
            if "length" in type_str: return "LENGTH"
            if "area" in type_str: return "AREA"
            if "volume" in type_str: return "VOLUME"
            if "angle" in type_str: return "ANGLE"
            if "string" in type_str or "text" in type_str: return "TEXT"
            if "integer" in type_str: return "INTEGER"
            if "number" in type_str: return "NUMBER"
            if "boolean" in type_str or "yesno" in type_str: return "YESNO"
            if "material" in type_str: return "MATERIAL"
            if "url" in type_str: return "URL"
            if "multiline" in type_str: return "MULTILINETEXT"
            if "image" in type_str: return "IMAGE"
            return "TEXT"
        else:
            p_type = definition.ParameterType
            t_str = str(p_type).upper()
            if "TEXT" in t_str: return "TEXT"
            if "LENGTH" in t_str: return "LENGTH"
            if "AREA" in t_str: return "AREA"
            if "VOLUME" in t_str: return "VOLUME"
            if "YESNO" in t_str: return "YESNO"
            if "INTEGER" in t_str: return "INTEGER"
            if "NUMBER" in t_str: return "NUMBER"
            if "MATERIAL" in t_str: return "MATERIAL"
            return "TEXT"
    except:
        return "TEXT"

class ProjectParamItem(object):
    def __init__(self, definition, is_shared):
        self.Name = definition.Name.strip()
        self.Definition = definition
        self.IsShared = is_shared
        

        self.ParamType = get_param_type_string(definition) 


        self.IsChecked = False
        
        try:
            if IS_NEW_REVIT:
                self.Group = get_label_for_group(definition.GetGroupTypeId())
            else:
                self.Group = get_label_for_group(definition.ParameterGroup)
        except:
            self.Group = "Other"

        self.ExistingGUID = None
        if is_shared:
            try:
                self.ExistingGUID = definition.GUID.ToString()
            except: pass

class ExportWindow(forms.WPFWindow):
    def __init__(self, xaml_file):
        forms.WPFWindow.__init__(self, xaml_file)
        
        self.raw_params = []        
        self.filtered_params = []   
        self.existing_names_in_txt = set() 
        self.existing_groups_in_txt = [] 


        self.load_project_params()
        

        current_sp_file = app.SharedParametersFilename
        found_file = False

        if current_sp_file and os.path.exists(current_sp_file):
            try:

                self.file_path_tb.Text = current_sp_file
                

                p_names, g_names = self.scan_txt_file_data(current_sp_file)
                self.existing_names_in_txt = p_names 
                self.existing_groups_in_txt = g_names
                

                self.update_group_combobox(g_names)
                

                self.status_lb.Text = "Auto-loaded active Shared Parameter file."
                found_file = True
            except:
                found_file = False


        if not found_file:
            self.update_group_combobox([])
            self.status_lb.Text = "No active Shared Parameter file found. Please browse."
        

        self.refresh_list_view()

    def load_project_params(self):
        iterator = doc.ParameterBindings.ForwardIterator()
        temp_list = []
        
        while iterator.MoveNext():
            definition = iterator.Key
            if definition:
                if isinstance(definition, InternalDefinition):
                    if definition.BuiltInParameter != BuiltInParameter.INVALID:
                        continue 
                
                is_shared = False
                try:
                    g = definition.GUID
                    is_shared = True
                except:
                    is_shared = False
                


                item = ProjectParamItem(definition, is_shared)
                temp_list.append(item)
        
        temp_list.sort(key=lambda x: (x.Group, x.Name))
        self.raw_params = temp_list

    def read_file_safe(self, file_path):
        if not os.path.exists(file_path): return []
        try:
            with io.open(file_path, 'r', encoding='utf-16') as f: return f.readlines()
        except: pass
        try:
            with io.open(file_path, 'r', encoding='utf-8-sig') as f: return f.readlines()
        except: pass
        try:
            with io.open(file_path, 'r', encoding='utf-8') as f: return f.readlines()
        except: return []

    def scan_txt_file_data(self, file_path):
        p_names = set()
        g_names = []
        
        lines = self.read_file_safe(file_path)
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            parts = line.split('\t')
            if len(parts) < 2: continue 

            first_col = parts[0].strip()

            if first_col == "PARAM" and len(parts) >= 3:
                name_in_file = parts[2].strip()
                p_names.add(name_in_file)
            
            if first_col == "GROUP" and len(parts) >= 3:
                g_name = parts[2].strip()
                if g_name and (g_name not in g_names):
                    g_names.append(g_name)
                    
        return p_names, g_names

    def update_group_combobox(self, existing_groups):
        items = []
        for g in existing_groups:
            items.append(g)
        
        if not items and "Exported Parameters" not in items:
            items.append("Exported Parameters")

        items.append("<New...>")
        
        self.group_name_cb.ItemsSource = items
        
        if items:
            self.group_name_cb.SelectedIndex = 0
            self.group_name_cb.IsEditable = False

    def group_combo_selection_changed(self, sender, args):
        selected_item = self.group_name_cb.SelectedItem
        
        if selected_item == "<New...>":
            self.group_name_cb.IsEditable = True
            self.group_name_cb.Text = "" 
            
        elif selected_item is not None:
            self.group_name_cb.IsEditable = False
            self.group_name_cb.Text = str(selected_item)

    def refresh_list_view(self):
        name_kw = self.search_name_tb.Text.lower()
        group_kw = self.search_group_tb.Text.lower()
        
        filtered = []
        for p in self.raw_params:
            if p.Name in self.existing_names_in_txt: 
                continue

            if name_kw and (name_kw not in p.Name.lower()): continue
            if group_kw and (group_kw not in p.Group.lower()): continue
            
            filtered.append(p)
            
        self.filtered_params = filtered
        self.param_dg.ItemsSource = self.filtered_params
        
        count_hidden = len(self.raw_params) - len(filtered)
        if self.existing_names_in_txt:
            self.status_lb.Text = "Auto-Loaded. Showing {}. Hidden {} parameters (already in txt file).".format(len(filtered), count_hidden)
        else:
            self.status_lb.Text = "Showing {} parameters.".format(len(filtered))

    # --- EVENT HANDLERS ---
    def search_box_changed(self, sender, args):
        self.refresh_list_view()

    def check_all_click(self, sender, args):
        for p in self.filtered_params:
            p.IsChecked = True
        self.param_dg.Items.Refresh()

    def check_none_click(self, sender, args):
        for p in self.filtered_params:
            p.IsChecked = False
        self.param_dg.Items.Refresh()

    def checkbox_click(self, sender, args):
        cb = sender
        clicked_item = cb.DataContext
        new_state = cb.IsChecked
        if self.param_dg.SelectedItems and self.param_dg.SelectedItems.Contains(clicked_item):
            for item in self.param_dg.SelectedItems:
                item.IsChecked = new_state
            self.param_dg.Items.Refresh()

    def browse_file_click(self, sender, args):
        path = forms.save_file(file_ext='txt', 
                               title="Select Shared Parameter File",
                               default_name="SharedParameters.txt")
        if path:
            self.file_path_tb.Text = path
            p_names, g_names = self.scan_txt_file_data(path)
            self.existing_names_in_txt = p_names 
            self.existing_groups_in_txt = g_names
            self.update_group_combobox(g_names)
            self.refresh_list_view()

    def export_click(self, sender, args):
        file_path = self.file_path_tb.Text
        target_group_name = self.group_name_cb.Text.strip()
        
        if not target_group_name or target_group_name == "<New...>":
            target_group_name = "Exported Parameters"

        checked_items = [p for p in self.filtered_params if p.IsChecked]

        if not file_path:
            forms.alert("Please select a file path!", title="Warning")
            return
        
        if not checked_items:
            forms.alert("Please check at least one parameter!", title="Warning")
            return

        try:
            existing_lines = self.read_file_safe(file_path)
            
            final_group_id = "1"
            max_id = 1
            found_group = False
            
            for line in existing_lines:
                if line.startswith("GROUP") and not line.startswith("*GROUP"):
                    parts = line.strip().split('\t')
                    if len(parts) >= 3:
                        try:
                            gid = int(parts[1])
                            if gid >= max_id: max_id = gid
                        except: pass
                        
                        if parts[2].strip().lower() == target_group_name.lower():
                            final_group_id = parts[1]
                            target_group_name = parts[2].strip() 
                            found_group = True
            
            lines_to_write = []
            has_header = False
            
            for l in existing_lines[:10]:
                if "*META" in l: has_header = True

            if not has_header:
                lines_to_write.append(u"# This is a Revit shared parameter file.")
                lines_to_write.append(u"# Do not edit manually.")
                lines_to_write.append(u"*META\tVERSION\tMINVERSION")
                lines_to_write.append(u"META\t2\t1")
                lines_to_write.append(u"*GROUP\tID\tNAME")
                if not found_group:
                    lines_to_write.append(u"GROUP\t{}\t{}".format(final_group_id, target_group_name))
                lines_to_write.append(u"*PARAM\tGUID\tNAME\tDATATYPE\tDATACATEGORY\tGROUP\tVISIBLE\tDESCRIPTION\tUSERMODIFIABLE\tHIDEWHENNOVALUE")
            else:
                for line in existing_lines:
                    if line.strip():
                        lines_to_write.append(line.strip())
                
                if not found_group:
                    final_group_id = str(max_id + 1)
                    insert_idx = len(lines_to_write)
                    for i, l in enumerate(lines_to_write):
                        if l.startswith("*PARAM"):
                            insert_idx = i
                            break
                    
                    lines_to_write.insert(insert_idx, u"GROUP\t{}\t{}".format(final_group_id, target_group_name))

            count = 0
            exported_names = []
            
            for item in checked_items:
                p_guid = item.ExistingGUID
                if not p_guid: p_guid = str(uuid.uuid4())
                

                line = u"PARAM\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                    p_guid, item.Name, item.ParamType, "", final_group_id, "1", "", "1", "0"
                )

                lines_to_write.append(line)
                count += 1
                exported_names.append(item.Name)

            full_content = u"\r\n".join(lines_to_write)
            
            with io.open(file_path, 'w', encoding='utf-16', newline='') as f:
                f.write(full_content)
                f.write(u"\r\n")
            
            for n in exported_names:
                self.existing_names_in_txt.add(n)
            
            if not found_group:
                p_names_new, g_names_new = self.scan_txt_file_data(file_path)
                self.existing_groups_in_txt = g_names_new
                self.update_group_combobox(g_names_new)
                self.group_name_cb.Text = target_group_name

            self.refresh_list_view()
            forms.alert("Export complete! {} parameters added.".format(count))

        except Exception as e:
            self.status_lb.Text = "Error: " + str(e)

if __name__ == '__main__':
    xaml_path = script.get_bundle_file('ExportPara.xaml')
    if os.path.exists(xaml_path):
        window = ExportWindow(xaml_path)
        window.ShowDialog()