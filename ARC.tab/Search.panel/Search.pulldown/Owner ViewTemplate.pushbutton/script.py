# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import codecs
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
if module.AutodeskData():
    import Autodesk
    from Autodesk.Revit.DB import View, FilteredElementCollector, Transaction
    import sys
    from pyrevit import forms, script
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

    list_view = []
    list_view_name =[]
    selected_views_template = forms.select_viewtemplates(multiple=False)
    text = str(selected_views_template.Name)
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
    results = []
    for i,j in zip(list_view_name, list_view):             
        output = script.get_output()
        # print (output.linkify(j.Id) + "                   " +  "View Name: " + str(i) )
        # print ("______________________________________________________________________")
        results.append((output.linkify(j.Id), str(i)))
    if len(results) != 0:
        output.print_md("## View đang sử dụng view teamplte: " + str(text))
        headers = ["View ID", "View Name"]
        output.print_table(results, headers)
    else: module.message_box("Không có view nào đang áp dụng view template được chọn")