
__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FailuresAccessor
from Autodesk.Revit.DB import Line
from Autodesk.Revit.Creation import ItemFactoryBase
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
import math
import sys
import string
import importlib
import traceback
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
try:
    ARC = string.ascii_lowercase
    begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
    module = importlib.import_module(str(begin))
    import Autodesk
    from Autodesk.Revit.DB import *
    from System.Collections.Generic import *
    if module.AutodeskData():
        Currentview = doc.ActiveView
        view_scale = Currentview.Scale
        Curve = []
except:
    sys.exit()

Currentview = doc.ActiveView

def spot_elevation (idoc, view, ref, point, bend, end,ref_point, leader):
    spot = idoc.Create.NewSpotElevation(view, ref, point, bend, end,ref_point, leader)
    return spot

Ele = module.get_elements(uidoc,doc, "Select Tag of Slabs", noti = False)
if Ele:
    try:
        t = Transaction(doc,"Spot floor follow tag")
        top_faces = []
        top_ref = []
        t.Start()
        for tag in Ele:
            try:
                get_element_Id = tag.TaggedLocalElementId
                floor = doc.GetElement(get_element_Id)
                top = HostObjectUtils.GetTopFaces(floor)
                tag_position = tag.TagHeadPosition
                for ref in top:
                    try:
                        top_face = floor.GetGeometryObjectFromReference(ref)
                        top_faces.append(top_face)
                        top_ref.append(ref)
                        last_ref = ref
                    except:
                        pass
                spot_elevation(doc, Currentview, last_ref, tag_position, tag_position, tag_position,tag_position, False)
            except:
                pass
        t.Commit()
    except:
        pass




