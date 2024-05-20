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
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        currentview = doc.ActiveView
        sketchloop = []
        # t = Transaction (doc, "Get Floor's Boundary")
        # t.Start()
        select = uidoc.Selection
        # type_of = Views
        # filter = Autodesk.Revit.DB.ElementClassFilter(Autodesk.Revit.DB.View)
        currentview_id = currentview.Id
        # get_depentdent = currentview.GetDependentElements(filter)
        list_id = []
        # for i in get_depentdent:
        minus_1 = int(str(currentview_id)) - 1
        list_id.Add(ElementId(minus_1))
        Icollection = List[ElementId](list_id)
        select.SetElementIds(Icollection)
except:
    pass