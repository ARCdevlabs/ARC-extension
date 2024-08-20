
# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
import traceback
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    #Get Document 
    doc = uidoc.Document
    Currentview = doc.ActiveView
    try:
        view_direction = Currentview.ViewDirection
        if view_direction.Z == 1 and str(Currentview.ViewType) != "ThreeD":
            Ele = module.get_elements(uidoc,doc, "Select Beams", noti = False)
            if Ele:
                t = Transaction (doc, "Place Center Line of Beam")
                t.Start()
                for i in Ele:
                    if i.Category.Name == "Structural Framing" or i.Category.Name == "構造フレーム":
                        Cur = i.Location.Curve
                        Direction = Cur.Direction
                        Startpoint = Cur.GetEndPoint(0)
                        Endpoint = Cur.GetEndPoint(1)
                        Midpoint0 = Cur.Evaluate(0.7, True)
                        PlaMidpoint0 = XYZ(Midpoint0.X, Midpoint0.Y, 0)
                        Zpoint = XYZ(Midpoint0.X, Midpoint0.Y, Midpoint0.Z + 10)
                        Zaxis = Line.CreateBound(Midpoint0, Zpoint)
                        LCenter = Line.CreateBound(XYZ(Startpoint.X,Startpoint.Y,0),XYZ(Endpoint.X,Endpoint.Y,0))
                        Detaillinecenter = doc.Create.NewDetailCurve(Currentview,LCenter)
                t.Commit()
        else:
            module.message_box("Please use the tool in plan view.") 
    except:
        pass

