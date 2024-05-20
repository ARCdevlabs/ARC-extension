__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import*
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Element
from System.Collections.Generic import *
import math
from rpw import ui
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
Currentview = doc.ActiveView
Curve = []
import os
import clr
import os.path as op
import sys
'''
USER_ROAMING_DIR = os.getenv('appdata')
PYREVIT_APP_DIR = op.join(USER_ROAMING_DIR,'pyRevit-Master','extensions','pyRevitTools.extension','SonKawamura.tab','Core') 
sys.path.append(PYREVIT_APP_DIR)  # path of dll
clr.AddReference ("SonKawamura") # the dll
import SonKawamura
'''

def get_selected_elements():
    selection = uidoc.Selection
    selection_ids = selection.GetElementIds()
    elements = []
    for element_id in selection_ids:
        elements.append(doc.GetElement(element_id))
    return elements

Ele = get_selected_elements()
t = Transaction (doc, "Place line1 elements")
t.Start()
for i in Ele:
    Cur = i.Location.Curve
    Direction = Cur.Direction
    Startpoint = Cur.GetEndPoint(0)
    Endpoint = Cur.GetEndPoint(1)
    Midpoint0 = Cur.Evaluate(0.7, True)
    PlaMidpoint0 = XYZ(Midpoint0.X, Midpoint0.Y, 0)
    Zpoint = XYZ(Midpoint0.X, Midpoint0.Y, Midpoint0.Z + 10)
    # Midpoint1 = Cur.Evaluate(0.9, True)
    # PlaMidpoint1 = XYZ(Midpoint1.X, Midpoint1.Y, 0)
    Zaxis = Line.CreateBound(Midpoint0, Zpoint)
    # L1 = Line.CreateBound(PlaMidpoint0,PlaMidpoint1)
    LCenter = Line.CreateBound(XYZ(Startpoint.X,Startpoint.Y,0),XYZ(Endpoint.X,Endpoint.Y,0))
    Detaillinecenter = doc.Create.NewDetailCurve(Currentview,LCenter)
    # Detailline1 = doc.Create.NewDetailCurve(Currentview,L1)
    # Loc1 = Detailline1.Location
    # Arrow1 = Loc1.Rotate(Zaxis, 3 * math.pi / 4)
    # Detailline2 = doc.Create.NewDetailCurve(Currentview,L1)
    # Loc2 = Detailline2.Location
    # Arrow2 = Loc2.Rotate(Zaxis, 5 * math.pi / 4)
t.Commit()


