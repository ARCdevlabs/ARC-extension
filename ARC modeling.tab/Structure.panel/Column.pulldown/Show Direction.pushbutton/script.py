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
import math
import traceback
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    #Get Document 
    doc = uidoc.Document
    Currentview = doc.ActiveView
    view_direction = Currentview.ViewDirection

    if view_direction.Z == 1 and str(Currentview.ViewType) != "ThreeD":
        Curve = []
        Ele = module.get_elements(uidoc,doc, "Select Column", noti = False)
        if Ele:
            try:
                t = Transaction (doc, "Show direction of column or foundation")
                t.Start()
                for i in Ele:
                    try:
                        Location1 = i.Location
                        Point_1 = Location1.Point
                        Direction1 = i.FacingOrientation
                        Point_2 =  Point_1 + 7* Direction1
                        Point_3 =  Point_1 + 5 * Direction1
                        PlanPoint_1 = XYZ(Point_1.X, Point_1.Y, 0)
                        PlanPoint_2 = XYZ(Point_2.X, Point_2.Y, 0)
                        PlanPoint_3 = XYZ(Point_3.X, Point_3.Y, 0)
                        Zpoint = XYZ(Point_2.X, Point_2.Y, Point_2.Z + 100)
                        Zaxis = Line.CreateBound(PlanPoint_2, Zpoint)
                        L1 = Line.CreateBound(PlanPoint_1,PlanPoint_2)
                        L2 = Line.CreateBound(PlanPoint_2, PlanPoint_3)
                        Detailline1 = doc.Create.NewDetailCurve(Currentview,L1)
                        Detailline2 = doc.Create.NewDetailCurve(Currentview,L2)
                        Detailline3 = doc.Create.NewDetailCurve(Currentview,L2)
                        Loc1 = Detailline2.Location
                        Arrow1 = Loc1.Rotate(Zaxis, 1 * math.pi / 4)
                        Loc2 = Detailline3.Location
                        Arrow2 = Loc2.Rotate(Zaxis, 7 * math.pi / 4)
                    except:
                        pass
                t.Commit()
            except:
                pass
    else:
        module.message_box("Please use the tool in plan view.")
