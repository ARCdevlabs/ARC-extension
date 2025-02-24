# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib

ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
try:
    if module.AutodeskData():
        import Autodesk
        from Autodesk.Revit.DB import *
        from Autodesk.Revit.UI.Selection.Selection import PickObject
        from Autodesk.Revit.UI.Selection  import ObjectType
        from Autodesk.Revit.DB import Element
        from System.Collections.Generic import *
        #Get UIDocument
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        acview= module.Active_view(doc)
        t = Transaction(doc, "Turn off RoomSeparator View Temporary")
        t.Start()
        Checkviewtemplate = str(acview.ViewTemplateId)
        #Check view have ViewTemplate or not, if not => don't need to Enable Temporary view
        if Checkviewtemplate != "-1":
            tem = acview.EnableTemporaryViewPropertiesMode(acview.Id)
        listcate = doc.Settings.Categories
        list_cate_all = acview.Category
        for i in listcate: 
            # print i.Name
            if str(i.Name) in "Lines, 線分":
                sub_cate = i.SubCategories
                for tung_sub_cate in sub_cate:
                    if tung_sub_cate.Name in "<Room Separation>, <部屋を分割>":
                        sub_cate_room_separator = tung_sub_cate
                        id_an = tung_sub_cate.Id
        if sub_cate_room_separator.Visible[acview]:            
            an = acview.SetCategoryHidden(id_an, True)
        else:
            hien = acview.SetCategoryHidden(id_an, False)
        t.Commit()  
except:
    pass
