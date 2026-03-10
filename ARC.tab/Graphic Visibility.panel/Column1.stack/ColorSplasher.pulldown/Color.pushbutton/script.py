# -*- coding: utf-8 -*-
import clr
import sys
import gc

# --- PRE-LOAD ASSEMBLIES ---
clr.AddReference('System')
clr.AddReference('System.Core')
clr.AddReference('PresentationCore')
clr.AddReference('PresentationFramework')
clr.AddReference('WindowsBase')
clr.AddReference('System.Windows')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

# --- IMPORTS ---
import System
from System.Collections.Generic import List
from System.Windows import Window, Thickness
from System.Windows.Controls import GridView, TextBox, Button, CheckBox
from System.Windows.Media import Brush, SolidColorBrush, VisualTreeHelper, Colors
from System.Windows.Media import Color as WpfColor
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit import forms, script
import wpf
from System.ComponentModel import INotifyPropertyChanged, PropertyChangedEventArgs

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# --- HELPER ---
def get_id_val(e_id):
    try:
        return e_id.Value
    except AttributeError:
        return e_id.IntegerValue
# --------------

class ValueItem(INotifyPropertyChanged):
    def __init__(self, name, element_ids):
        self._name = name
        self._element_ids = element_ids
        self._count = len(element_ids)
        self._is_checked = False
        self._background_brush = None
        self._revit_color = None
        self._property_changed = None

    @property
    def Name(self): return self._name
    @property
    def ElementIds(self): return self._element_ids
    @property
    def Count(self): return self._count
    @property
    def IsChecked(self): return self._is_checked
    @IsChecked.setter
    def IsChecked(self, value):
        if self._is_checked != value:
            self._is_checked = value
            self.OnPropertyChanged("IsChecked")
    @property
    def BackgroundBrush(self): return self._background_brush
    @BackgroundBrush.setter
    def BackgroundBrush(self, value):
        if self._background_brush != value:
            self._background_brush = value
            self.OnPropertyChanged("BackgroundBrush")
    @property
    def RevitColor(self): return self._revit_color
    @RevitColor.setter
    def RevitColor(self, value): self._revit_color = value

    def add_PropertyChanged(self, value):
        import System
        self._property_changed = System.Delegate.Combine(self._property_changed, value)
    def remove_PropertyChanged(self, value):
        import System
        self._property_changed = System.Delegate.Remove(self._property_changed, value)
    def OnPropertyChanged(self, property_name):
        if self._property_changed is not None:
            self._property_changed(self, PropertyChangedEventArgs(property_name))

class CategoryItem(object):
    def __init__(self, name, category_id):
        self.Name = name
        self.Id = category_id
    def __str__(self): return self.Name

class ParameterItem(object):
    def __init__(self, name, definition, is_instance):
        self.Name = name
        self.Definition = definition
        self.IsInstance = is_instance
        self.TypeLabel = "(I)" if is_instance else "(T)"
        self.DisplayName = "{} ({})".format(name, "Instance" if is_instance else "Type")
    def __str__(self): return self.DisplayName

class ColorPickerWindow(Window):
    def __init__(self, parent_item):
        wpf.LoadComponent(self, script.get_bundle_file('ColorPicker.xaml'))
        self.selected_item = parent_item
        self.generate_colors()

    def generate_colors(self):
        import colorsys
        hue_steps = 60 
        sat_steps = [0.65, 0.90]
        light_steps = [0.65, 0.78, 0.92]
        
        for h_idx in range(hue_steps):
            hue = h_idx / float(hue_steps)
            for sat in sat_steps:
                for light in light_steps:
                    r, g, b = colorsys.hls_to_rgb(hue, light, sat)
                    R, G, B = int(r * 255), int(g * 255), int(b * 255)
                    
                    btn = Button()
                    btn.Width = 25; btn.Height = 25
                    brush = SolidColorBrush(WpfColor.FromRgb(R, G, B))
                    if brush.CanFreeze: brush.Freeze()
                    
                    btn.Background = brush
                    btn.Margin = Thickness(1)
                    btn.Cursor = System.Windows.Input.Cursors.Hand
                    btn.Click += self.color_btn_click
                    btn.Tag = Color(R, G, B)
                    self.wpColors.Children.Add(btn)

    def color_btn_click(self, sender, args):
        new_revit_color = sender.Tag
        new_brush = sender.Background
        if self.selected_item:
            self.selected_item.RevitColor = new_revit_color
            self.selected_item.BackgroundBrush = new_brush
            self.selected_item.IsChecked = True
        self.Close()
    def btnCancel_Click(self, sender, args): self.Close()

class ColorSplasherWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, script.get_bundle_file('ColorSplasher.xaml'))
        
        self.all_elements_in_view = []
        self.current_value_items = []
        self.master_value_items = []
        self.all_param_items = []
        self.txtTotalCount_Control = None
        self.type_cache = {}

        try:
            self.load_categories()
        except Exception as e:
            print("Init Error: " + str(e))
            
        self.lvValues.ItemContainerGenerator.StatusChanged += self.OnItemContainerGeneratorStatusChanged
        self.Closing += self.OnWindowClosing

    def FindVisualChild(self, parent, child_type, name=None):
        for i in range(VisualTreeHelper.GetChildrenCount(parent)):
            child = VisualTreeHelper.GetChild(parent, i)
            if clr.GetClrType(child_type).IsInstanceOfType(child):
                if name:
                    if hasattr(child, "Name") and child.Name == name: return child
                else: return child
            result = self.FindVisualChild(child, child_type, name)
            if result: return result
        return None

    def OnItemContainerGeneratorStatusChanged(self, sender, args):
        if self.lvValues.ItemContainerGenerator.Status == System.Windows.Controls.Primitives.GeneratorStatus.ContainersGenerated:
            for item in self.current_value_items:
                container = self.lvValues.ItemContainerGenerator.ContainerFromItem(item)
                if container:
                    checkbox = self.FindVisualChild(container, CheckBox)
                    if checkbox:
                        checkbox.Checked -= self.OnCheckBoxChecked
                        checkbox.Unchecked -= self.OnCheckBoxUnchecked
                        checkbox.Checked += self.OnCheckBoxChecked
                        checkbox.Unchecked += self.OnCheckBoxUnchecked

    def OnCheckBoxChecked(self, sender, e):
        if self.lvValues.SelectedItems.Count > 1:
            for selected_item in self.lvValues.SelectedItems:
                selected_item.IsChecked = True

    def OnCheckBoxUnchecked(self, sender, e):
        if self.lvValues.SelectedItems.Count > 1:
            for selected_item in self.lvValues.SelectedItems:
                selected_item.IsChecked = False

    def lvValues_MouseDoubleClick(self, sender, args):
        if self.lvValues.SelectedItem:
            item = self.lvValues.SelectedItem
            ColorPickerWindow(item).ShowDialog()

    def OnWindowClosing(self, sender, args):
        try:
            # Clean up only when closing
            self.lvValues.ItemContainerGenerator.StatusChanged -= self.OnItemContainerGeneratorStatusChanged
            self.Closing -= self.OnWindowClosing
            self.all_elements_in_view = []
            self.master_value_items = []
            self.current_value_items = []
            self.type_cache = {}
            gc.collect() # Only GC here
        except: pass

    def load_categories(self):
        collector = None
        try:
            view = doc.ActiveView
            if not view.IsValidObject: return 
            from Autodesk.Revit.DB import FilteredElementCollector
            
            collector = FilteredElementCollector(doc, view.Id).WhereElementIsNotElementType()
            cat_dict = {}
            self.all_elements_in_view = []
            
            excluded_cats = set([
                "Cameras", "Project Information", "Sketch Lines", "Views",
                "Sheets", "Project Base Point", "Survey Point", "Guide Grids",
                "Analysis Display Style", "Center Line"
            ])
            
            elements = collector.ToElements()
            for el in elements:
                # Optimized validation
                try:
                    cat = el.Category
                    if cat and get_id_val(cat.Id) != -1:
                        if cat.Name in excluded_cats: continue
                        
                        self.all_elements_in_view.append(el)
                        if cat.Name not in cat_dict:
                            cat_dict[cat.Name] = cat.Id
                except: continue
                        
            sorted_cats = sorted(cat_dict.keys())
            self.lbCategories.ItemsSource = [CategoryItem(name, cat_dict[name]) for name in sorted_cats]
        except Exception as e:
            forms.alert("Error loading categories: {}".format(e))
        finally:
            if collector: collector.Dispose()

    def get_parameter_value(self, element, param_name, is_instance):
        try:
            t_id = element.GetTypeId()
            elem_type = None
            if t_id != ElementId.InvalidElementId:
                type_key = get_id_val(t_id)
                # Optimized cache lookup
                elem_type = self.type_cache.get(type_key)
                if elem_type is None:
                    try:
                        elem_type = doc.GetElement(t_id)
                        self.type_cache[type_key] = elem_type
                    except: pass
            
            if param_name == "Family and Type":
                family_name = element.Category.Name if element.Category else ""
                type_name = ""
                if elem_type:
                    try: family_name = getattr(elem_type, "FamilyName", family_name) or family_name
                    except: pass
                    try: type_name = elem_type.Name
                    except: pass
                if not type_name and element.Name: type_name = element.Name
                return "{} : {}".format(family_name, type_name)
            
            if param_name == "Family":
                if elem_type:
                    try: 
                        fn = getattr(elem_type, "FamilyName", None)
                        if fn: return fn
                    except: pass
                return element.Category.Name if element.Category else "<No Family>"
            
            if param_name == "Type":
                if elem_type:
                    try: 
                        tn = elem_type.Name
                        if tn: return tn
                    except: pass
                return element.Name if element.Name else "<No Type>"
            
            param = None
            try:
                if is_instance: param = element.LookupParameter(param_name)
                else:
                    if elem_type: param = elem_type.LookupParameter(param_name)
            except: return "<Null>"
            
            if not param: return "<Null>"
            if not param.HasValue: return "<Empty>"
            
            # Fast path for strings
            st = param.StorageType
            if st == StorageType.String:
                return param.AsString() or "<Empty>"
            
            # Try getting value string first (most common)
            try:
                val_str = param.AsValueString()
                if val_str: return val_str
            except: pass
            
            if st == StorageType.ElementId:
                e_id = param.AsElementId()
                if e_id == ElementId.InvalidElementId: return "<Empty>"
                try:
                    e = doc.GetElement(e_id)
                    return e.Name if e else str(get_id_val(e_id))
                except: return str(get_id_val(e_id))
            elif st == StorageType.Integer:
                try:
                    if param.Definition.GetDataType().ToString().lower().find("boolean") != -1:
                        return "Yes" if param.AsInteger() == 1 else "No"
                except: 
                    # Fallback for old Revit or non-boolean integers
                    pass
                return str(param.AsInteger())
            
            return "N/A"
        except Exception: return "<Error>"

    def lbCategories_SelectionChanged(self, sender, args):
        selected_categories = self.lbCategories.SelectedItems
        if not selected_categories:
            self.lbParameters.ItemsSource = None
            self.all_param_items = []
            return
        
        selected_cat_ids = set([cat.Id for cat in selected_categories])
        example_elements = [el for el in self.all_elements_in_view if el.Category.Id in selected_cat_ids]
        
        if not example_elements:
            self.lbParameters.ItemsSource = None
            self.all_param_items = []
            return
        
        params_dict = {}
        try:
            # Add implicit parameters
            params_dict[("Family and Type", True)] = ParameterItem("Family and Type", None, True)
            
            # Scan first 5 elements for efficiency
            for el in example_elements[:5]:
                for p in el.Parameters:
                    if p.Definition:
                        p_name = p.Definition.Name
                        if (p_name, True) not in params_dict:
                            params_dict[(p_name, True)] = ParameterItem(p_name, p.Definition, True)
                
                t_id = el.GetTypeId()
                if t_id != ElementId.InvalidElementId:
                    elem_type = doc.GetElement(t_id)
                    if elem_type:
                        for p in elem_type.Parameters:
                            if p.Definition:
                                p_name = p.Definition.Name
                                if (p_name, False) not in params_dict:
                                    params_dict[(p_name, False)] = ParameterItem(p_name, p.Definition, False)
        except: pass
        
        sorted_keys = sorted(params_dict.keys(), key=lambda x: x[0])
        self.all_param_items = [params_dict[k] for k in sorted_keys]
        self.lbParameters.ItemsSource = self.all_param_items
        
        if self.txtSearchParam.Text:
            self.txtSearchParam_TextChanged(self.txtSearchParam, None)

    def lbParameters_SelectionChanged(self, sender, args):
        selected_categories = self.lbCategories.SelectedItems
        selected_param = self.lbParameters.SelectedItem
        if not selected_categories or not selected_param: return
        
        values_map = {}
        collector = None
        try:
            for cat_item in selected_categories:
                # Optimized Collector
                collector = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategoryId(cat_item.Id).WhereElementIsNotElementType()
                # ToElementIds is faster than ToElements for just getting IDs to loop
                all_ids = collector.ToElementIds()
                
                for eid in all_ids:
                    try:
                        el = doc.GetElement(eid)
                        if not el: continue # Light check
                        val = self.get_parameter_value(el, selected_param.Name, selected_param.IsInstance)
                        if val not in values_map: values_map[val] = []
                        values_map[val].append(eid)
                    except: continue
                
                collector.Dispose()
                collector = None

            self.master_value_items = []
            import random
            for val_str in sorted(values_map.keys()):
                item = ValueItem(val_str, values_map[val_str])
                self.assign_random_color(item)
                self.master_value_items.append(item)
            
            self.current_value_items = list(self.master_value_items)
            self.lvValues.ItemsSource = self.current_value_items
            
            tb = self.FindVisualChild(self.lvValues, TextBox, "txtSearchValue")
            if tb: tb.Text = ""
            self.update_total_count()
            # REMOVED GC.COLLECT HERE FOR SPEED

        except Exception as ex:
            forms.alert("Error loading values: {}".format(ex))
        finally:
            if collector: collector.Dispose()

    def txtSearchParam_TextChanged(self, sender, args):
        search_text = sender.Text.lower()
        if not self.all_param_items: return
        if not search_text: self.lbParameters.ItemsSource = self.all_param_items
        else:
            self.lbParameters.ItemsSource = [p for p in self.all_param_items if search_text in p.Name.lower()]

    def txtSearchValue_TextChanged(self, sender, args):
        search_text = sender.Text.lower()
        if not self.master_value_items: return
        if not search_text: self.current_value_items = list(self.master_value_items)
        else: self.current_value_items = [v for v in self.master_value_items if search_text in v.Name.lower()]
        self.lvValues.ItemsSource = self.current_value_items
        self.update_total_count()

    def txtTotalCount_Loaded(self, sender, args):
        self.txtTotalCount_Control = sender
        self.update_total_count()

    def update_total_count(self):
        total = sum(item.Count for item in self.current_value_items) if self.current_value_items else 0
        if self.txtTotalCount_Control: self.txtTotalCount_Control.Text = str(total)

    def btnCheckAll_Click(self, sender, args):
        if not self.current_value_items: return
        for item in self.current_value_items: item.IsChecked = True

    def btnCheckNone_Click(self, sender, args):
        if not self.current_value_items: return
        for item in self.current_value_items: item.IsChecked = False

    def lvValues_SizeChanged(self, sender, args):
        if self.lvValues.View and isinstance(self.lvValues.View, GridView):
            gv = self.lvValues.View
            if gv.Columns.Count >= 2:
                new_width = self.lvValues.ActualWidth - gv.Columns[1].Width - 10
                if new_width > 0: gv.Columns[0].Width = new_width

    def assign_random_color(self, item):
        import random
        r = random.randint(130, 255)
        g = random.randint(130, 255)
        b = random.randint(130, 255)
        brush = SolidColorBrush(WpfColor.FromRgb(r, g, b))
        if brush.CanFreeze: brush.Freeze()
        item.BackgroundBrush = brush
        item.RevitColor = Color(r, g, b)

    def btnRefresh_Click(self, sender, args):
        for item in self.master_value_items: self.assign_random_color(item)

    def btnRainbow_Click(self, sender, args):
        import colorsys
        items = self.master_value_items
        count = len(items)
        if count == 0: return
        
        for i, item in enumerate(items):
            ratio = float(i) / float(max(count - 1, 1))
            hue = ratio * 0.85
            r, g, b = colorsys.hls_to_rgb(hue, 0.75, 0.8)
            R, G, B = int(r * 255), int(g * 255), int(b * 255)
            
            brush = SolidColorBrush(WpfColor.FromRgb(R, G, B))
            if brush.CanFreeze: brush.Freeze()
            item.BackgroundBrush = brush
            item.RevitColor = Color(R, G, B)

    def btnApply_Click(self, sender, args):
        solid_pat_id = None
        pats = FilteredElementCollector(doc).OfClass(FillPatternElement).ToElements()
        for p in pats:
            if p.GetFillPattern().IsSolidFill:
                solid_pat_id = p.Id
                break
        

        if not solid_pat_id:
            forms.alert("No Solid Fill Pattern found!")
            return
        
        view = doc.ActiveView
        t = Transaction(doc, "Color Splasher Apply")
        try:
            t.Start()
            applied_count = 0
            failed = []
            for item in self.master_value_items:
                if not item.IsChecked: continue
                ogs = OverrideGraphicSettings()
                ogs.SetProjectionLineColor(item.RevitColor)
                ogs.SetCutLineColor(item.RevitColor)
                ogs.SetSurfaceForegroundPatternId(solid_pat_id)
                ogs.SetSurfaceForegroundPatternColor(item.RevitColor)
                ogs.SetCutForegroundPatternId(solid_pat_id)
                ogs.SetCutForegroundPatternColor(item.RevitColor)
                
                for eid in item.ElementIds:
                    try:
                        view.SetElementOverrides(eid, ogs)
                        applied_count += 1
                    except Exception as inner:
                        failed.append(str(get_id_val(eid)) + " - " + str(inner))
            
            if applied_count > 0:
                t.Commit()
                uidoc.RefreshActiveView()
                msg = "Áp dụng thành công cho {} đối tượng.".format(applied_count)
                if failed: msg += "\n\nLỗi:\n" + "\n".join(failed[:5])
                forms.alert(msg)
            else:
                t.RollBack()
                forms.alert("Không đối tượng nào được tô màu.")
        except Exception as ex:
            if t.HasStarted(): t.RollBack()
            forms.alert("Lỗi: " + str(ex))
        finally:
            if t.HasStarted(): t.RollBack()
            t.Dispose()
        self.Close()
        
    def btnClear_Click(self, sender, args):
        view = doc.ActiveView
        t = Transaction(doc, "Clear Colors")
        try:
            t.Start()
            empty_ogs = OverrideGraphicSettings()
            ids_to_clear = List[ElementId]()
            for item in self.master_value_items:
                for eid in item.ElementIds: ids_to_clear.Add(eid)
            
            if ids_to_clear.Count > 0:
                for eid in ids_to_clear:
                      try: view.SetElementOverrides(eid, empty_ogs)
                      except: pass
            else:
                col = FilteredElementCollector(doc, view.Id).WhereElementIsNotElementType().ToElementIds()
                for eid in col:
                      try: view.SetElementOverrides(eid, empty_ogs)
                      except: pass
            t.Commit()
            uidoc.RefreshActiveView()
            forms.alert("Đã xóa màu!")
        except Exception as ex:
            if t.HasStarted(): t.RollBack()
            forms.alert("Lỗi: " + str(ex))
        finally:
            if t.HasStarted(): t.RollBack()
            t.Dispose()

    def btnSelect_Click(self, sender, args):
        ids_to_select = List[ElementId]()
        for item in self.master_value_items:
            if item.IsChecked:
                for eid in item.ElementIds: ids_to_select.Add(eid)
        if ids_to_select.Count > 0:
            uidoc.Selection.SetElementIds(ids_to_select)
            self.Close()
        else:
            forms.alert("Chưa chọn giá trị nào.")

try:
    gc.collect()
    ColorSplasherWindow().ShowDialog()
except Exception as e:
    forms.alert("Fatal error: {}".format(e))
    print(e)