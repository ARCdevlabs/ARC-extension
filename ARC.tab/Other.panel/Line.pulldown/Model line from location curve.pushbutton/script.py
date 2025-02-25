# -*- coding: utf-8 -*-
import Autodesk
import nances
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
if nances.AutodeskData():
    def create_plane_from_three_points(point1, point2, point3):
        plane = Plane.CreateByThreePoints(point1, point2, point3)
        return plane
    try:
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        currentview = doc.ActiveView
        sketchloop = []
        t = Transaction (doc, "Create line from location curve")
        t.Start()
        Ele = nances.get_elements(uidoc,doc, 'Select Element', noti = False)
        list_point= []
        for element in Ele:
            try:
                Line = element.Location.Curve
                point_1 = Line.GetEndPoint(0)
                point_2 = Line.GetEndPoint(1)
                Offset_Line = Line.CreateOffset (1,XYZ(0.55123123123,0.123123123123155,0))
                plane = create_plane_from_three_points(point_1,point_2,Offset_Line.GetEndPoint(0))
                sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(doc,plane)
                model_line = doc.Create.NewModelCurve(Line, sketch_plane)
            except:
                pass
        t.Commit()
    except:
        t.RollBack()
        pass


    