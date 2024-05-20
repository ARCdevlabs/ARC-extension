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
    try:
        import Autodesk
        from Autodesk.Revit.DB import *
        from System.Collections.Generic import *
        from pyrevit import forms, script
        if module.AutodeskData():
            uidoc = __revit__.ActiveUIDocument
            doc = uidoc.Document
            Ele = module.get_selected_elements(uidoc,doc)
            if not Ele:
                import sys
                sys.exit()
            t = Transaction (doc, "View chứa đối tượng 2D đang được chọn")
            t.Start()
            view_name = []
            list_view_id =[]
            for i in Ele:
                owner_view = i.OwnerViewId
                list_view_id.append(owner_view)
            new_list_view_id = list(set(list_view_id))
            for tung_view in new_list_view_id:
                view = doc.GetElement((tung_view))
                view_name.append(Autodesk.Revit.DB.Element.Name.GetValue(view)) 
            for i, j in zip (view_name, new_list_view_id):
                # view = doc.GetElement(i)
                # view_name = Autodesk.Revit.DB.Element.Name.GetValue(view)
                output = script.get_output()
                print (output.linkify(j) + "                   " +  "View Name: " + str(i) )
                print ("______________________________________________________________________")
            t.Commit()
    except:
        pass


