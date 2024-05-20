# -*- coding: utf-8 -*-
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
Currentview = doc.ActiveView
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
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
Currentview = doc.ActiveView
try:
    def get_dependent_element (element):
        filter = Autodesk.Revit.DB.ElementClassFilter(SpotDimension)
        get_dependent_id = element.GetDependentElements(filter)
        return get_dependent_id

    def get_dependent_element_view (view):
        filter = Autodesk.Revit.DB.ElementClassFilter(ViewPlan)
        get_dependent_id = view.GetDependentElements(filter)
        return get_dependent_id


    def get_dependent (idoc, view, ref, point, bend, end,ref_point, leader):
        spot = idoc.Create.NewSpotElevation(view, ref, point, bend, end,ref_point, leader)
        return spot

    def move_element (idoc, element, vector):
        move = Autodesk.Revit.DB.ElementTransformUtils.MoveElement(idoc,element.Id,vector)
        return move

    Ele = module.get_selected_elements(uidoc,doc)
    t = Transaction(doc,"Chỉnh lại vị trí spot sàn theo tag")
    top_faces = []
    top_ref = []
    t.Start()
    for tag in Ele:
        get_element_Id = tag.TaggedLocalElementId
        floor = doc.GetElement(get_element_Id)
        spots = get_dependent_element(floor)
        for spot_id in spots:
            get_spot = doc.GetElement(spot_id)
            owner_view = get_spot.OwnerViewId
            view_tong = get_dependent_element_view(doc.GetElement(owner_view))
            for dependent_view_tong in view_tong:
                if Currentview.Id == dependent_view_tong:
                    is_hidden = get_spot.IsHidden(Currentview)
                    if not is_hidden:
                        tag_position = tag.TagHeadPosition
                        spot_location = get_spot.Origin
                        move = move_element (doc, get_spot, XYZ(tag_position.X - spot_location.X,tag_position.Y - spot_location.Y,spot_location.Z))
    t.Commit()
except:
    pass




