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
        AcView= module.Active_view(doc)
        ids = List[ElementId]()
        wall = []
        collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType()
        collector.ToElements()
        list_wallA = []
        for i in collector:
            try:
                isstruc_wall = module.get_builtin_parameter_by_name(i, BuiltInParameter.WALL_STRUCTURAL_SIGNIFICANT)
                if isstruc_wall.AsInteger() == 0:
                    list_wallA.append(i)
            except:
                pass
        t = Transaction(doc, "Hide wallA")
        t.Start()
        for wallA in list_wallA:
            is_hidden = wallA.IsHidden(AcView)
            if is_hidden:
                hide_element = AcView.UnhideElements(List[ElementId]([wallA.Id]))
            else:
                unhide_element = AcView.HideElements(List[ElementId]([wallA.Id]))
        t.Commit()
except:
    pass

      