# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
from Autodesk.Revit.DB import HostObjectUtils,XYZ,Line, ElementId, Transaction
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
import traceback
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Currentview = doc.ActiveView

    Ele = module.get_element(uidoc,doc, "Select Floors to get boundary", noti = False)
    select = uidoc.Selection
    detailline= []
    mot_san = Ele[0]
    ref = HostObjectUtils.GetBottomFaces(mot_san)
    try:
        view_direction = Currentview.ViewDirection
        if view_direction.Z == 1 and str(Currentview.ViewType) != "ThreeD":
            # param_bottom_offset = mot_san.get_Parameter(DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)
            param_bottom_offset = module.get_builtin_parameter_by_name(mot_san, DB.BuiltInParameter.STRUCTURAL_ELEVATION_AT_BOTTOM)
            bottom_level = param_bottom_offset.AsDouble()
            for i in ref:
                t = Transaction (doc, "Get Floor's Boundary")
                t.Start()
                if param_bottom_offset.HasValue == False:
                    try:
                        boundaryloops = mot_san.GetGeometryObjectFromReference(i).GetEdgesAsCurveLoops()
                        for loop in boundaryloops:   
                            sketchloop = []
                            sketchloop.append([x for x in loop])
                            for a1 in sketchloop:
                                for a2 in a1:
                                    Startpoint = a2.GetEndPoint(0)
                                    Endpoint = a2.GetEndPoint(1)
                                    PlaPoint1 = XYZ(Startpoint.X, Startpoint.Y, 0)
                                    PlaPoint2 = XYZ(Endpoint.X, Endpoint.Y, 0)
                                    L1 = Line.CreateBound(PlaPoint1,PlaPoint2)
                                    detailline.append(doc.Create.NewDetailCurve(Currentview,L1))

                    except:
                        # import traceback
                        # print(traceback.format_exc())
                        pass
                else:
                    try:
                        boundaryloops = mot_san.GetGeometryObjectFromReference(i).GetEdgesAsCurveLoops()
                        for loop in boundaryloops:   
                            sketchloop = []
                            sketchloop.append([x for x in loop])
                            for a1 in sketchloop:
                                for a2 in a1:
                                    detailline.append(doc.Create.NewDetailCurve(Currentview,a2))
                    except:
                        # import traceback
                        # print(traceback.format_exc())
                        pass
                t.Commit()    
            listid = []
            for seg in detailline:
                segid = seg.Id
                listid.append(segid)
            Icollection = List[ElementId](listid)
            select.SetElementIds(Icollection)
        else:
            module.message_box("Please use the tool in plan view.") 
    except:
        # import traceback
        # print(traceback.format_exc())
        pass


    