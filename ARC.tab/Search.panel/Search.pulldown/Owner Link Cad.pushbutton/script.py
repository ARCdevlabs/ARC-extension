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
    from pyrevit import forms, script
    import sys
    import clr
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    t = Transaction (doc, "View đang chứa link cad đang được chọn")
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
    list_view_id = []
    list_view_name =[]
    selected_import_instance = forms.select_import_instance(multiple=False)
    # color = forms.select_swatch()
    text = selected_import_instance

    for import_instance in all_import_instances:
        try:
            get_import_instance_name = import_instance.Category.Name
        except:
            pass
        if text == get_import_instance_name:
            owner_view = import_instance.OwnerViewId
            list_view_id.append(owner_view)
            # print import_instance.Id
            # new_list_view_id = list(set(list_view_id))
    
    for i in list_view_id:
        view = doc.GetElement(i)
        view_name = Autodesk.Revit.DB.Element.Name.GetValue(view)
        list_view_name.append(view_name)

    for i,j in zip(list_view_name, list_view_id):             
        output = script.get_output()
        # print ("View Name: " + str(i))
        print (output.linkify(j) + "                   " +  "View Name: " + str(i) )
        print ("______________________________________________________________________")
    t.Commit()      

