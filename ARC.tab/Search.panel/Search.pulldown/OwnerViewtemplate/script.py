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
if module.AutodeskData():

    import sys
    import clr
    clr.AddReference("System.Windows.Forms")
    from System.Windows.Forms import Application, Form, TextBox, Button
    from System.Drawing import Point, Size
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Ele = module.get_selected_elements(uidoc,doc)
    t = Transaction (doc, "Get all view has current view template")
    t.Start()

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

    class MyForm(Form):
        def __init__(self):
            self.Text = "My Form"
            self.InitializeComponents()

        def InitializeComponents(self):
            self.textBox = TextBox()
            self.textBox.Location = Point(10, 10)
            self.textBox.Size = Size(200, 20)

            self.button = Button()
            self.button.Text = "Submit"
            self.button.Location = Point(10, 40)
            self.button.Click += self.button_Click

            self.Controls.Add(self.textBox)
            self.Controls.Add(self.button)
        def button_Click(self, sender, e):

            text = self.textBox.Text
            # print text
            # print("Entered name of view template:", text)
            list_view = []
            for view in all_views:
                # if view_template_name == text:
                get_view_template_id = view.ViewTemplateId
                view_template = doc.GetElement(get_view_template_id)
                view_template_name_2 = Autodesk.Revit.DB.Element.Name.GetValue(view_template)
                # print (view_template_name_2)
                if str(text) == str(view_template_name_2):
                    decode_name = view.Name
                    list_view.append(decode_name)
            for i in list_view:
                print (i)
            self.Close()  


    if __name__ == "__main__":
        form = MyForm()
        Application.Run(form)

    t.Commit()      

