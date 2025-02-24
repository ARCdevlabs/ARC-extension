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
from Autodesk.Revit.DB import View, FilteredElementCollector, Transaction, ImportInstance
if module.AutodeskData():
    import sys
    import clr
    clr.AddReference("System.Windows.Forms")
    from System.Windows.Forms import Application, Form, TextBox, Button, FormStartPosition, ComboBox
    from System.Drawing import Point, Size
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    t = Transaction (doc, "Get all view has current view template")
    t.Start()
    def get_all_import_instances(doc):
        collector = FilteredElementCollector(doc)
        import_instances = collector.OfClass(ImportInstance).ToElements()
        return import_instances
    all_import_instances = get_all_import_instances(doc)

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
    list_import_instance = []
    class MyForm(Form):
        def __init__(self):
            self.Text = "Find views include DWG"
            self.InitializeComponents()
            self.StartPosition = FormStartPosition.CenterScreen

        def InitializeComponents(self):
            self.comboBox = ComboBox()
            self.comboBox.Location = Point(10, 10)
            self.comboBox.Size = Size(250, 20)
            for import_instance in all_import_instances:
                try:
                    import_instance_name = import_instance.Category.Name
                    list_import_instance.append(import_instance_name)
                    list_import_instance_set = list(set(list_import_instance))
                except:
                    pass
            for import_name in list_import_instance_set:
                self.comboBox.Items.Add(import_name)
            self.comboBox.Sorted = True

            self.button = Button()
            self.button.Text = "Find view"
            self.button.Location = Point(10, 40)
            self.button.Click += self.button_Click

            self.Controls.Add(self.comboBox)
            self.Controls.Add(self.button)
        def button_Click(self, sender, e):
            list_view_id = []
            text = self.comboBox.SelectedItem
            for import_instance in all_import_instances:
                get_import_instance_name = import_instance.Category.Name
                if text == get_import_instance_name:
                    owner_view = import_instance.OwnerViewId
                    list_view_id.append(owner_view)
                    # print import_instance.Id
                    # new_list_view_id = list(set(list_view_id))
            for i in list_view_id:
                view = doc.GetElement(i)
                view_name = Autodesk.Revit.DB.Element.Name.GetValue(view)
                print(view_name)
            self.Close()  
    if __name__ == "__main__":
        form = MyForm()
        Application.Run(form)
    t.Commit()      

