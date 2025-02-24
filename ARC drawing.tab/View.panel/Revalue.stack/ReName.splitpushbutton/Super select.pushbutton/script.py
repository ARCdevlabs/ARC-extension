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

class FSCategoryItem(forms.TemplateListItem):
    """Wrapper class for frequently selected category list item"""
    pass


def load_configs():
    """Load list of frequently selected categories from configs or defaults"""
    fscats = my_config.get_option("family_tag_wall", [])
    revit_cats = [fscats]
    return revit_cats


def save_configs(content):
    """Save given list of categories as frequently selected"""
    my_config.family_tag_wall = content
    script.save_config()


def reset_defaults(options):
    """Reset frequently selected categories to defaults"""
    defaults = [revit.query.get_category(x)
                for x in FREQUENTLY_SELECTED_CATEGORIES]
    default_names = [x.Name for x in defaults if x]
    for opt in options:
        if opt.name in default_names:
            opt.checked = True


'''Code để import wpf form'''
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
# find the path of ui.xaml
from pyrevit import UI
from pyrevit import script
xamlfile = script.get_bundle_file('SuperSelect.xaml')
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
        self.category_output = []
        self.parameter_output = []
        self.set_category()
        self.set_parameter()
        self.set_value()

    def set_category(self):
        self.category.ItemsSource = ["category 1", "category 2"]

    def category_item_click(self, sender, e):
        selected_item = self.category.SelectedItem
        if str(selected_item) == 'category 1':
            self.category_output = ['a']
        if str(selected_item) == 'category 2':
            self.category_output = ['b']
        self.set_parameter()

    def set_parameter(self):
        self.parameter.ItemsSource = self.category_output 

    def parameter_item_click(self, sender, e):
        selected_item = self.parameter.SelectedItem
        if str(selected_item) == 'a':
            self.parameter_output = ['c', 'd']
        if str(selected_item) == 'b':
            self.parameter_output = ['e', 'f']
        self.set_value()

    def set_value(self):
        self.value.ItemsSource = self.parameter_output

    def done_button(self, sender, args):
        self.Close()


MyWindow().ShowDialog()
