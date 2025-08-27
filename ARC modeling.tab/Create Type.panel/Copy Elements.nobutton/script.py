# -*- coding: utf-8 -*-
import string
import importlib
#Get UIDocument
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
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
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
import traceback

def create_plane_from_three_points(point1, point2, point3):
    plane = Plane.CreateByThreePoints(point1, point2, point3)
    return plane
try:
    if module.AutodeskData():
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document

        currentview = doc.ActiveView
        def pick_point_with_nearest_snap():       
            snap_settings = Autodesk.Revit.UI.Selection.ObjectSnapTypes.Nearest
            prompt = "Click"
            try:
                click_point = uidoc.Selection.PickPoint(snap_settings, prompt)
            except:
                # print(traceback.format_exc())
                pass
            return click_point

        Ele = module.get_selected_elements(uidoc,doc)

        source_pick = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element)
        source_element = doc.GetElement(source_pick.ElementId)
        source_location_point = source_element.Location
        source_point = source_location_point.Point
        source_point_x = source_point.X
        source_point_y = source_point.Y
        source_point_z = source_point.Z

        if Ele:
            t = Transaction (doc, "Copy 1 element thành nhiều element khác nhau với vị trí dựa theo các đối tượng chọn sẵn")
            t.Start()
            for i in Ele:
                location_point = i.Location
                point = location_point.Point
                new_position = XYZ(point.X - source_point_x , point.Y - source_point_y, source_point_z)
                hand_orientation = i.HandOrientation
                print 
                copy_element = Autodesk.Revit.DB.ElementTransformUtils.CopyElement(doc, source_element.Id, new_position)
            t.Commit()
except:
    import traceback
    print(traceback.format_exc())
    pass


    