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

from pyrevit import DB, script, revit
config = script.get_config('Toggle wallA')
def set_config(state, config):
    config.twoDhighlight = state
    script.toggle_icon(state)
    script.save_config()

def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    off_icon = script_cmp.get_bundle_file('off.png')
    ui_button_cmp.set_icon(off_icon)

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
            isstruc_wall = module.get_builtin_parameter_by_name(i, BuiltInParameter.WALL_STRUCTURAL_SIGNIFICANT)
            if isstruc_wall.AsInteger() == 0:
                list_wallA.append(i)
        t = Transaction(doc, "Hide wallA")
        t.Start()
        for wallA in list_wallA:
            is_hidden = wallA.IsHidden(AcView)
            if is_hidden:
                hide_element = AcView.UnhideElements(List[ElementId]([wallA.Id]))
                set_config(False, config)
            else:
                unhide_element = AcView.HideElements(List[ElementId]([wallA.Id]))
                set_config(True, config)
        t.Commit()
except:
    import traceback
    print(traceback.format_exc())

      