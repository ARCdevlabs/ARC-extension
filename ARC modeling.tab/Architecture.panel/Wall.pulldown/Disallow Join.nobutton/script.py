# -*- coding: utf-8 -*-
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
from pyrevit import revit, DB, UI
import traceback
try:
    if module.AutodeskData():
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        Ele = module.get_selected_elements(uidoc,doc)
        t = Transaction (doc, "DisAllow join tường")
        
        t.Start()
        def disallow_join_at_end(element, ind):
            Autodesk.Revit.DB.WallUtils.DisallowWallJoinAtEnd(element,ind)

        def pick_point_with_nearest_snap():       
            snap_settings = UI.Selection.ObjectSnapTypes.None
            prompt = "Click"
            try:

                click_point = uidoc.Selection.PickPoint(snap_settings, prompt)
                
            except:
                # print(traceback.format_exc())
                pass
            return click_point

        def distance_2_point(point , reference_point):
            distance = point.DistanceTo(reference_point)
            return distance

        def get_nearest_point(points, reference_point):
            min_distance = float('inf')
            nearest_point = None
            
            for point in points:
                distance = point.DistanceTo(reference_point)
                if distance < min_distance:
                    min_distance = distance
                    nearest_point = point
            return nearest_point

        point = pick_point_with_nearest_snap()

        for i in Ele:
            curve_wall = i.Location.Curve
            start_point = curve_wall.GetEndPoint(0)
            end_point = curve_wall.GetEndPoint(1)
            tim_point = get_nearest_point([start_point,end_point], point)
            if tim_point == start_point:
                index = 0
            else:
                index = 1
            disallow_join_at_end(i, index)
        t.Commit()
except:
    import traceback
    # print (traceback.format_exc_())
    pass