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

def create_tags(idoc, input_element, view, tag_orientation = TagOrientation.Horizontal):
    location = input_element.Location
    tag_mode = TagMode.TM_ADDBY_CATEGORY
    element_ref = Reference(input_element)
    # tag_orientation = TagOrientation.Horizontal
    location = location.Point
    tag = Autodesk.Revit.DB.IndependentTag.Create(idoc, view.Id, element_ref, False, tag_mode, tag_orientation, location)
    return tag

def move_point_along_vector(point, vector, distance):
    new_point = point + vector.Normalize() * distance
    return new_point



Ele = module.get_selected_elements(uidoc,doc)
t = Transaction(doc,"Tag cửa")

t.Start()
for door in Ele:
    facing_orient = door.FacingOrientation
    if abs(facing_orient.Y) == 1:
        orient = TagOrientation.Horizontal
    else:
        orient = TagOrientation.Vertical
    new_tag = create_tags (doc, door, Currentview, orient)
    # new_point = move_point_along_vector(new_tag.TagHeadPosition, facing_orient, 5)
    # new_tag.TagHeadPosition = new_point
t.Commit()





