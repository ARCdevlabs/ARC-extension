# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib
import traceback
try:
    ARC = string.ascii_lowercase
    begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
    module = importlib.import_module(str(begin))
    import Autodesk
    from Autodesk.Revit.DB import *
    from System.Collections.Generic import *
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
        t = Transaction(doc, "Ẩn hiện Curtain wall")
        t.Start()
        AcView= module.Active_view(doc)
        ids = List[ElementId]()
        wall = []
        collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType()
        collector.ToElements()
        list_curtain_wall = []
        for i in collector:
            # print i
            wall_type = module.get_type(doc, i)
            family_name = wall_type.FamilyName
            if family_name in "Curtain Wall, カーテンウォール":
                is_hidden = i.IsHidden(AcView)
                if is_hidden:
                    hide_element = AcView.UnhideElements(List[ElementId]([i.Id]))
                else:
                    unhide_element = AcView.HideElements(List[ElementId]([i.Id]))

        t.Commit()
except:
    pass     

      