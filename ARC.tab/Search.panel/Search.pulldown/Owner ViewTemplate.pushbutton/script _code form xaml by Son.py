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
from Autodesk.Revit.DB import View, FilteredElementCollector, Transaction
import sys
import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Application, Form, TextBox, Button
from System.Drawing import Point, Size

from pyrevit import script

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
def get_all_view_templates():
    collector = Autodesk.Revit.DB.FilteredElementCollector(doc)
    views = collector.OfClass(View).ToElements()
    view_templates = [view for view in views if view.IsTemplate]
    return view_templates
all_view_templates = get_all_view_templates()

def get_all_views():
    collector = Autodesk.Revit.DB.FilteredElementCollector(doc)
    views = collector.OfClass(View).ToElements()
    valid_views = [view for view in views if not view.IsTemplate]
    return valid_views

all_views = get_all_views()

for view in all_views:
    get_view_template_id = view.ViewTemplateId

    view_template = doc.GetElement(get_view_template_id)
    view_name = Autodesk.Revit.DB.Element.Name.GetValue(view_template)

import unicodedata
def decode_unicode_string(unicode_string):
    decoded_string = ""
    for char in unicode_string:
        try:
            decoded_char = unicodedata.name(char)
            decoded_string += decoded_char
        except ValueError:
            decoded_string += char
    return decoded_string

def encode_to_base64(input_string):
    import base64
    input_bytes = input_string.encode('utf-8')
    base64_bytes = base64.b64encode(input_bytes)
    base64_string = base64_bytes.decode('utf-8')  
    return base64_bytes

def decode_to_base64(input_string):
    import base64
    base64_encoded = base64.b64decode(input_string).decode('utf-8')
    return base64_encoded


# dependencies
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

# find the path of ui.xaml
from pyrevit import UI
from pyrevit import script
xamlfile = script.get_bundle_file('OwnerViewTemplate.xaml')

# import WPF creator and base Window
import wpf
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System")
from System import Windows
list_view = []
list_view_name =[]
class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)
        # self.setup_combobox_data()
        # self.setup_listbox_data()
    @property
    def input_viewtemplate_name(self):
        return self.textbox.Text

    def find_view(self, sender, args):
        text = str(self.input_viewtemplate_name)
        for view in all_views:
            # if view_template_name == text:
            get_view_template_id = view.ViewTemplateId
            view_template = doc.GetElement(get_view_template_id)
            view_template_name_2 = Autodesk.Revit.DB.Element.Name.GetValue(view_template)
            # print (view_template_name_2)
            if str(text) == str(view_template_name_2):
                decode_name = view.Name
                list_view_name.append(decode_name)
                list_view.append(view)
                # for i in list_view:
                #     print (i)
    # def find_view(self, sender, args):
        for i,j in zip(list_view_name, list_view):             
            output = script.get_output()
            # print ("View Name: " + str(i))
            print ("View Name: " + str(i) + "         ID view: " +  output.linkify(j.Id))
            print ("_________________________________________________________")
        self.Close()
MyWindow().ShowDialog()

