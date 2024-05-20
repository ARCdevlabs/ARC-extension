import string
import importlib
#Get UIDocument

ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    currentview = doc.ActiveView
    t = Transaction (doc, "Get Floor's Boundary")
    t.Start()
    select = uidoc.Selection
    detailline= []
    list_id = []
    Ele = module.get_selected_elements(uidoc,doc)
    DatumExtentType = Autodesk.Revit.DB.DatumExtentType.ViewSpecific
    for i in Ele:
        a = i.GetCurvesInView(DatumExtentType,currentview)
        for x in a:
        #need to change to line in plan view because some floor is not on a plane.
            Startpoint = x.GetEndPoint(0)
            Endpoint = x.GetEndPoint(1)
            L1 = Line.CreateBound(Startpoint,Endpoint)
            set_curve_in_view = i.SetCurveInView(DatumExtentType,currentview, L1)
            detailline.append(doc.Create.NewDetailCurve(currentview,L1))
    for seg in detailline:
        segid = seg.Id
        list_id.append(segid)
    Icollection = List[ElementId](list_id)
    select.SetElementIds(Icollection)
    t.Commit()
    