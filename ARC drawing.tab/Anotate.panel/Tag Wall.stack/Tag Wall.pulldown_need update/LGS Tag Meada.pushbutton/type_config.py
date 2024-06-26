# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import codecs
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
import sys
from Autodesk.Revit.DB import View, FilteredElementCollector, Transaction, ImportInstance, BuiltInCategory
import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Application, Label, Form, TextBox, Button, FormStartPosition, ComboBox
from System.Drawing import Point, Size
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
Currentview = doc.ActiveView
try:
    ARC = string.ascii_lowercase
    begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
    module = importlib.import_module(str(begin))
    import Autodesk
    from Autodesk.Revit.DB import *
    from System.Collections.Generic import *
    if module.AutodeskData():
        Currentview = doc.ActiveView
        view_scale = Currentview.Scale
        Curve = []
except:
    sys.exit()
# pylint: disable=E0401,W0703,C0103
from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script


logger = script.get_logger()
my_config = script.get_config("family_tag_wall")

# class FSCategoryItem(forms.TemplateListItem):
#     """Wrapper class for frequently selected category list item"""
#     pass


def load_configs():
    """Load list of frequently selected categories from configs or defaults"""
    fscats = my_config.get_option("family_tag_wall", [])
    revit_cats = [fscats]
    return revit_cats


def save_configs(content):
    """Save given list of categories as frequently selected"""
    my_config.family_tag_wall = content
    script.save_config()


# def reset_defaults(options):
#     """Reset frequently selected categories to defaults"""
#     defaults = [revit.query.get_category(x)
#                 for x in FREQUENTLY_SELECTED_CATEGORIES]
#     default_names = [x.Name for x in defaults if x]
#     for opt in options:
#         if opt.name in default_names:
#             opt.checked = True


'''Code để import wpf form'''
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
# find the path of ui.xaml
from pyrevit import UI
from pyrevit import script
xamlfile = script.get_bundle_file('Setuptagwall.xaml')
# import WPF creator and base Window
import wpf
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System")
from System import Windows
list_view = []
class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)
        # self.setup_combobox_data()
        # self.setup_listbox_data()
    @property
    def setup_family(self):
        return self.family_name.Text
    
    @property
    def setup_type_1(self):
        return self.type_name_1.Text
    @property
    def setup_type_2(self):
        return self.type_name_2.Text

    @property
    def setup_type_3(self):
        return self.type_name_3.Text

    @property
    def setup_type_4(self):
        return self.type_name_4.Text
    
    @property
    def setup_type_5(self):
        return self.type_name_5.Text
    
    @property
    def setup_type_6(self):
        return self.type_name_6.Text

    def done_button(self, sender, args):
        family_name = self.setup_family
        type_name_1 = self.setup_type_1
        type_name_2 = self.setup_type_2
        type_name_3 = self.setup_type_3
        type_name_4 = self.setup_type_4
        type_name_5 = self.setup_type_5
        type_name_6 = self.setup_type_6
        total = [family_name,type_name_1,type_name_2,type_name_3,type_name_4,type_name_5,type_name_6]
        save_configs(total)
        self.Close()
MyWindow().ShowDialog()
