__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib
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
        AcView= module.Active_view(doc)
        ids = List[ElementId]()
        wall = []
        collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType()
        collector.ToElements()
        listfloorA = []
        def TempIsolate(view, items):
            ielements = List[ElementId]([x.Id for x in items])
            view.HideElementsTemporary(ielements)
        count_link_revit = collector.GetElementCount()
        if count_link_revit > 0:
            t = Transaction(doc, "Hide Revit link")
            t.Start()
            TempIsolate(AcView, collector )
            t.Commit()
        else:
            module.message_box("Don't have Revit Link")
except:
    pass     
