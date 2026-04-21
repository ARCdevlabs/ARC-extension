# -*- coding: utf-8 -*-
__title__     = "Project Transfer"

import os, sys
from collections import defaultdict
from Autodesk.Revit.DB import *
from pyrevit import forms
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System")
clr.AddReference("PresentationFramework")
import System 
from System.Collections.Generic import List
from System.Windows import Visibility
from System.ComponentModel import INotifyPropertyChanged, PropertyChangedEventArgs
import wpf

class ListItem(INotifyPropertyChanged):
    def __init__(self, name, element_id, item_type, checked=False):
        self._name = name
        self._element_id = element_id
        self._item_type = item_type
        self._is_checked = checked
        self._property_changed = None

    @property
    def Name(self): return self._name
    @property
    def Type(self): return self._item_type
    @property
    def Id(self): return self._element_id
    @property
    def IsChecked(self): return self._is_checked
    
    @IsChecked.setter
    def IsChecked(self, value):
        if self._is_checked != value:
            self._is_checked = value
            self.OnPropertyChanged("IsChecked")

    def add_PropertyChanged(self, value):
        self._property_changed = System.Delegate.Combine(self._property_changed, value)
    def remove_PropertyChanged(self, value):
        self._property_changed = System.Delegate.Remove(self._property_changed, value)
    def OnPropertyChanged(self, property_name):
        if self._property_changed:
            self._property_changed(self, PropertyChangedEventArgs(property_name))

try:
    from Snippets._context_manager import ef_Transaction
except ImportError:
    class ef_Transaction:
        def __init__(self, doc, name):
            self.t = Transaction(doc, name)
            
        def __enter__(self): 
            self.t.Start()
            return self.t
            
        def __exit__(self, exc_type, exc_value, traceback):
            if exc_type is not None:
                if self.t.HasStarted() and self.t.GetStatus() == TransactionStatus.Started:
                    self.t.RollBack()
            else:
                if self.t.HasStarted() and self.t.GetStatus() == TransactionStatus.Started:
                    self.t.Commit()

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
PATH_SCRIPT = os.path.dirname(__file__)
dict_projects = {d.Title:d for d in app.Documents if not d.IsFamilyDocument and not d.IsLinked}

TYPE_VIEW_TEMPLATE = "Transfer View Template"
TYPE_FILTER        = "Transfer Filters (View Filters)"
TYPE_LINE_STYLE    = "Transfer Detail Line / Line Style"
TYPE_FAMILY        = "Transfer Family"
TYPE_ANNOTATION    = "Transfer Annotation Symbols"
TYPE_DIMENSION     = "Transfer Dimension Styles"
TYPE_SPOT          = "Transfer Spot Elevation Styles"
TYPE_TEXT          = "Transfer Text Styles"
TYPE_BROWSER_ORG   = "Transfer Browser Organization"

class CopyViewTemplate(forms.WPFWindow):
    def __init__(self):
        path_xaml_file = os.path.join(PATH_SCRIPT, 'CopyViewTemplate.xaml')
        wpf.LoadComponent(self, path_xaml_file)

        active_title = doc.Title
        self.doc_to = doc
        self.UI_CopyTo.Items.Add(active_title)
        self.UI_CopyTo.SelectedIndex = 0
        
        for name in sorted(dict_projects.keys()):
            if name != active_title:
                self.UI_CopyFrom.Items.Add(name)

        modes = [TYPE_VIEW_TEMPLATE, TYPE_FILTER, TYPE_LINE_STYLE, TYPE_FAMILY, 
                 TYPE_ANNOTATION, TYPE_DIMENSION, TYPE_SPOT, TYPE_TEXT, 
                 TYPE_BROWSER_ORG]
        for m in modes:
            self.UI_Combo_TransferType.Items.Add(m)
        self.UI_Combo_TransferType.SelectedIndex = 0 

        self.UI_GroupBox_List.Visibility = Visibility.Collapsed
        self.UI_btn_Run.IsEnabled = False
        self.ShowDialog()

    def UIe_TransferType_Changed(self, sender, e):
        self.current_mode = self.UI_Combo_TransferType.SelectedValue
        self.refresh_data_list()

    def UIe_Project_Changed(self, sender, e):
        self.doc_to = dict_projects.get(self.UI_CopyTo.SelectedValue)
        self.doc_from = dict_projects.get(self.UI_CopyFrom.SelectedValue)
        if self.doc_to and self.doc_from and (self.doc_to.Title != self.doc_from.Title):
            self.UI_GroupBox_List.Visibility = Visibility.Visible
            self.UI_btn_Run.IsEnabled = True
            self.refresh_data_list()
        else:
            self.UI_GroupBox_List.Visibility = Visibility.Collapsed
            self.UI_btn_Run.IsEnabled = False

    def collect_elements_safe(self, doc_target, mode):
        try:
            if mode == TYPE_VIEW_TEMPLATE:
                return [v for v in FilteredElementCollector(doc_target).OfClass(View).ToElements() if v.IsTemplate]
            elif mode == TYPE_FILTER:
                return FilteredElementCollector(doc_target).OfClass(ParameterFilterElement).ToElements()
            elif mode == TYPE_LINE_STYLE:
                cat = doc_target.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
                if cat: return [s.GetGraphicsStyle(GraphicsStyleType.Projection) for s in cat.SubCategories if s.GetGraphicsStyle(GraphicsStyleType.Projection)]
                return []
            elif mode == TYPE_FAMILY:
                return [f for f in FilteredElementCollector(doc_target).OfClass(Family).ToElements() if f.IsEditable and f.FamilyCategory.CategoryType != CategoryType.Annotation]
            elif mode == TYPE_ANNOTATION:
                return [f for f in FilteredElementCollector(doc_target).OfClass(Family).ToElements() if f.FamilyCategory and f.FamilyCategory.CategoryType == CategoryType.Annotation]
            elif mode == TYPE_DIMENSION:
                return FilteredElementCollector(doc_target).OfClass(DimensionType).ToElements()
            elif mode == TYPE_SPOT:
                return FilteredElementCollector(doc_target).OfClass(SpotDimensionType).ToElements()
            elif mode == TYPE_TEXT:
                return FilteredElementCollector(doc_target).OfClass(TextNoteType).ToElements()
            elif mode == TYPE_BROWSER_ORG:
                return FilteredElementCollector(doc_target).OfClass(BrowserOrganization).ToElements()
        except:
            return []
        return []

    def get_ui_type_name(self):
        mapping = {
            TYPE_VIEW_TEMPLATE: "View Template",
            TYPE_FILTER:        "Filters",
            TYPE_LINE_STYLE:    "Line",
            TYPE_FAMILY:        "Family",
            TYPE_ANNOTATION:    "Symbols",
            TYPE_DIMENSION:     "Dimension",
            TYPE_SPOT:          "Spot Elevation",
            TYPE_TEXT:          "Text",
            TYPE_BROWSER_ORG:   "Browser Org"
        }
        return mapping.get(self.current_mode, "Element")

    def get_transaction_name(self):
        mapping = {
            TYPE_VIEW_TEMPLATE: "Transfer View Template",
            TYPE_FILTER:        "Transfer Filters",
            TYPE_LINE_STYLE:    "Transfer Line",
            TYPE_FAMILY:        "Transfer Family",
            TYPE_ANNOTATION:    "Transfer Symbols",
            TYPE_DIMENSION:     "Transfer Dimension",
            TYPE_SPOT:          "Transfer Spot Elevation",
            TYPE_TEXT:          "Transfer Text",
            TYPE_BROWSER_ORG:   "Transfer Browser Organization"
        }
        return mapping.get(self.current_mode, "Transfer Elements")

    def refresh_data_list(self):
        if not self.doc_from or not self.current_mode: return
        
        elements = self.collect_elements_safe(self.doc_from, self.current_mode)
        ui_type = self.get_ui_type_name()
        
        temp_list = []
        for e in elements:
            try:
                name = Element.Name.__get__(e)
                if not name or name.startswith("<"): continue
                temp_list.append(ListItem(name, e.Id, ui_type, False))
            except: continue

        temp_list.sort(key=lambda x: (x.Type, x.Name))
        self.Current_List_Items = List[ListItem](temp_list)
        self.UI_ListBox_Items.ItemsSource = self.Current_List_Items

    def UIe_CheckBox_Clicked(self, sender, e):
        cb = sender
        item_context = cb.DataContext
        is_checked = cb.IsChecked
        selected_items = self.UI_ListBox_Items.SelectedItems
        if selected_items.Contains(item_context) and selected_items.Count > 1:
            for item in selected_items:
                item.IsChecked = is_checked

    def UIe_text_filter_updated(self, sender, e):
        if not self.Current_List_Items: return
        txt = self.UI_TextBox_Filter.Text.lower()
        filtered = List[ListItem]()
        for i in self.Current_List_Items:
            if txt in i.Name.lower(): filtered.Add(i)
        self.UI_ListBox_Items.ItemsSource = filtered

    def select_mode(self, checked):
        if not self.UI_ListBox_Items.ItemsSource: return
        for item in self.UI_ListBox_Items.ItemsSource: item.IsChecked = checked
    def UIe_btn_select_all(self, sender, e): self.select_mode(True)
    def UIe_btn_select_none(self, sender, e): self.select_mode(False)

    def UIe_btn_run(self, sender, e):
        selected_wrappers = [i for i in self.Current_List_Items if i.IsChecked]
        if not selected_wrappers: return
        
        is_family_mode = self.current_mode in [TYPE_FAMILY, TYPE_ANNOTATION]

        existing_names = set()
        target_families_dict = {} 
        
        if self.current_mode == TYPE_BROWSER_ORG:
            try:
                target_bos = FilteredElementCollector(self.doc_to).OfClass(BrowserOrganization).ToElements()
                for t in target_bos: 
                    if t.Name: existing_names.add(t.Name)
            except: pass
        else:
            existing_elements = self.collect_elements_safe(self.doc_to, self.current_mode)
            for el in existing_elements:
                try:
                    n = Element.Name.__get__(el)
                    if n: 
                        existing_names.add(n)
                        if is_family_mode:
                            target_families_dict[n] = el 
                except: pass
        
        ids_to_copy = List[ElementId]()
        names_to_copy = []
        names_skipped = []
        
        missing_type_ids = [] 
        missing_type_reports = []

        for item in selected_wrappers:
            if is_family_mode and item.Name in existing_names:
                target_fam = target_families_dict.get(item.Name)
                src_fam = self.doc_from.GetElement(item.Id)
                
                if target_fam and src_fam:
                    target_type_names = set()
                    for t_s_id in target_fam.GetFamilySymbolIds():
                        t_type = self.doc_to.GetElement(t_s_id)
                        if t_type: target_type_names.add(Element.Name.__get__(t_type))
                    
                    added_new_type = False
                    for s_s_id in src_fam.GetFamilySymbolIds():
                        s_type = self.doc_from.GetElement(s_s_id)
                        if s_type:
                            s_type_name = Element.Name.__get__(s_type)
                            if s_type_name not in target_type_names:
                                missing_type_ids.append(s_s_id)
                                missing_type_reports.append("Family name: {} - Type name: {}".format(item.Name, s_type_name))
                                added_new_type = True
                    
                    if not added_new_type:
                        names_skipped.append(item.Name) 
                continue
            
            if item.Name in existing_names:
                names_skipped.append(item.Name)
                continue
                
            ids_to_copy.Add(item.Id)
            names_to_copy.append(item.Name)

        if ids_to_copy.Count == 0 and not missing_type_ids:
            forms.alert("No new items or types to transfer.\nSkipped {} existing items.".format(len(names_skipped)))
            self.Close()
            return

        full_trans_name = self.get_transaction_name()
        tg = TransactionGroup(self.doc_to, full_trans_name)
        
        try:
            tg.Start()

            param_report = ""
            if self.current_mode == TYPE_BROWSER_ORG:
                try:
                    src_params = FilteredElementCollector(self.doc_from).OfClass(ParameterElement).ToElements()
                    
                    tgt_params_names = set()
                    for p in FilteredElementCollector(self.doc_to).OfClass(ParameterElement).ToElements():
                        tgt_params_names.add(p.Name)
                    
                    param_ids_to_copy = List[ElementId]()
                    count_param = 0
                    for p in src_params:
                        if p.Name not in tgt_params_names:
                            param_ids_to_copy.Add(p.Id)
                            count_param += 1
                    
                    if param_ids_to_copy.Count > 0:
                        with ef_Transaction(self.doc_to, "Transfer Dependency Parameters"):
                            self.perform_copy(param_ids_to_copy)
                        param_report = "\n[AUTO-TRANSFER] Copied {} missing Project Parameters.".format(count_param)
                except Exception as p_ex:
                    print("Warning: Failed to transfer parameters. " + str(p_ex))

            if self.current_mode == TYPE_VIEW_TEMPLATE:
                with ef_Transaction(self.doc_to, full_trans_name):
                    self.perform_copy(ids_to_copy)
            
            elif is_family_mode:
                all_symbol_ids = []
                for item in selected_wrappers:
                    if item.Name in names_to_copy:
                        try:
                            fam_elem = self.doc_from.GetElement(item.Id)
                            if fam_elem:
                                for s_id in fam_elem.GetFamilySymbolIds(): 
                                    all_symbol_ids.append(s_id)
                        except: pass
                
                all_symbol_ids.extend(missing_type_ids)
                
                if all_symbol_ids:
                    with ef_Transaction(self.doc_to, full_trans_name):
                        self.perform_copy(List[ElementId](all_symbol_ids))
            
            else:
                with ef_Transaction(self.doc_to, full_trans_name):
                    self.perform_copy(ids_to_copy)

            tg.Assimilate()
            
            # REPORT
            print("="*70)
            print("REPORT: {}".format(full_trans_name.upper()))
            print("="*70)
            
            if param_report:
                print(param_report)
            
            total_success = len(names_to_copy) + len(missing_type_reports)
            if total_success > 0:
                print("\n[SUCCESSFULLY TRANSFERRED: {}]".format(total_success))
                for n in names_to_copy:
                    print("+ {} (Transfer)".format(n))
                for nt in missing_type_reports:
                    print("+ {} (New Type)".format(nt))
            
            if names_skipped:
                print("\n[SKIPPED - ALREADY EXIST: {}]".format(len(names_skipped)))
                for n in names_skipped:
                    print("- {} (Skip)".format(n))
            
            print("\n" + "="*70)
            print("DONE.")
            
        except Exception as ex:
            if tg.GetStatus() == TransactionStatus.Started: tg.RollBack()
            forms.alert("Error: {}".format(ex))
        finally:
            self.Close()

    def perform_copy(self, ids):
        opts = CopyPasteOptions()
        handler = CustomCopyHandler()
        opts.SetDuplicateTypeNamesHandler(handler)
        ElementTransformUtils.CopyElements(self.doc_from, ids, self.doc_to, Transform.Identity, opts)

class CustomCopyHandler(IDuplicateTypeNamesHandler):
    def OnDuplicateTypeNamesFound(self, args):
        return DuplicateTypeAction.UseDestinationTypes

if __name__ == '__main__':
    CopyViewTemplate()