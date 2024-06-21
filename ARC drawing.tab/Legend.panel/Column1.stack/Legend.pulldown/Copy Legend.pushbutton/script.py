__doc__ = 'python for revit api'
__author__ = 'SonKawamura'

import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Application, Form, TextBox, Button
from System.Drawing import Point, Size
from Autodesk.Revit.DB import ElementId, View, Transaction
import Autodesk
from System.Collections.Generic import List
#Get UIDocument
import os.path as op
import sys
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
active_view = doc.ActiveView
def get_fill_regions_and_text_in_active_view(doc, view):
    list_plan_region = []
    collector = FilteredElementCollector(doc, view.Id)
    for i in collector:
        if str(type(i)) == "<type 'FilledRegion'>" or "<type 'TextNote'>":
            list_plan_region.append(i)
    return list_plan_region


def get_all_in_active_view(doc, view):
    list_plan_region = []
    collector = FilteredElementCollector(doc, view.Id)
    for i in collector:
        if str(type(i)) == "<type 'FilledRegion'>" :
            list_plan_region.append(i)
    return list_plan_region


def copy_elements_to_view(element_to_copy, sourceView, target_view_name):
    all_views = FilteredElementCollector(doc).OfClass(View).ToElements()
    target_view = None
    transform_setting = Autodesk.Revit.DB.Transform.Identity
    for view in all_views:
        if view.Name == target_view_name:
            target_view = view
            break
    if not target_view:
        raise ValueError("View with name" + target_view_name + "not found")
    try:
        copied_element_id = Autodesk.Revit.DB.ElementTransformUtils.CopyElements(sourceView, element_to_copy, target_view, None, None)
    except:
        pass
    return copied_element_id


def override_graphics_in_view(target_view_name, element_id, override_setting):
    all_views = FilteredElementCollector(doc).OfClass(View).ToElements()
    target_view = None
    for view in all_views:
        if view.Name == target_view_name:
            target_view = view
            break
    if not target_view:
        raise ValueError("View with name" + target_view_name + "not found")
    override = Autodesk.Revit.DB.OverrideGraphicSettings()
    override = override_setting
    target_view.SetElementOverrides(element_id, override)
    return


class MyForm(Form):
    def __init__(self):
        self.Text = "Copy Legend"
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
        target_view_name = self.textBox.Text
        fill_regions_in_active_view = get_fill_regions_and_text_in_active_view(doc, active_view)
        fill_regions_id = []
        t = Transaction (doc, "Copy FillRegion")
        t.Start()
        for fill_region in fill_regions_in_active_view:
            fill_regions_id.append(fill_region.Id)
            get_override = active_view.GetElementOverrides(fill_region.Id)
            list_element_id = List[ElementId](fill_regions_id)
            copied_element = copy_elements_to_view(list_element_id, active_view,target_view_name )
            override_graphics_in_view(target_view_name, copied_element[0], get_override)
            fill_regions_id.remove(fill_region.Id)      
        t.Commit()  
        self.Close()  
if __name__ == "__main__":
    form = MyForm()
    Application.Run(form)   

