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


# def TempIsolate(view, items):
#     ielements = List[ElementId]([x.Id for x in items])
#     view.HideElementsTemporary(ielements)

# def hide_elements(view, items):
#     ielements = List[ElementId]([x.Id for x in items])
#     view.HideElements(ielements)
#     return 
# def unhide_elements(view, items):
#     ielements = List[ElementId]([x.Id for x in items])
#     view.UnhideElements(ielements)
#     return
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
        list_wallS = []
        for i in collector:
            isstruc_wall = module.get_builtin_parameter_by_name(i, BuiltInParameter.WALL_STRUCTURAL_SIGNIFICANT)
            if isstruc_wall.AsInteger() == 1:
                list_wallS.append(i)
        t = Transaction(doc, "Hide wallS")
        t.Start()
        for wallS in list_wallS:
            is_hidden = wallS.IsHidden(AcView)
            if is_hidden:
                hide_element = AcView.UnhideElements(List[ElementId]([wallS.Id]))
            else:
                unhide_element = AcView.HideElements(List[ElementId]([wallS.Id]))
        t.Commit()
except:
    import traceback
    print(traceback.format_exc())

      