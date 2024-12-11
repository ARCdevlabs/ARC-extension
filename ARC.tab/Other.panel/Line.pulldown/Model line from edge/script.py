# -*- coding: utf-8 -*-
import Autodesk
import nances
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
from nances import vectortransform
if nances.AutodeskData():
    try:
        def create_plane_from_three_points(point1, point2, point3):
            plane = Plane.CreateByThreePoints(point1, point2, point3)
            return plane

        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        pick_edge = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Edge)
        element_of_edge = doc.GetElement(pick_edge.ElementId)
        geometry_object_of_edge = element_of_edge.GetGeometryObjectFromReference(pick_edge)
        if isinstance(geometry_object_of_edge, Edge):
            t = Transaction (doc, "Create Model Line from Edge")
            t.Start()
            try:
                origin_curve = geometry_object_of_edge.AsCurve()
                curve = origin_curve
                hermite_spline = curve
                control_points = hermite_spline.Tessellate()
                new_plane = create_plane_from_three_points(control_points[0],control_points[1],control_points[2])
                sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(doc,new_plane)
                model_line = doc.Create.NewModelCurve(hermite_spline, sketch_plane)
                t.Commit()
            except:
                try:
                    origin_curve = geometry_object_of_edge.AsCurve()
                    curve = origin_curve
                    point_1 = curve.GetEndPoint(0)
                    point_2 = curve.GetEndPoint(1)
                    new_line = Line.CreateBound(point_1,point_2)
                    offset_line = new_line.CreateOffset (1,XYZ(0.55123123123,0.123123123123155,0))
                    new_plane = create_plane_from_three_points(point_1,point_2,offset_line.GetEndPoint(0))
                    sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(doc,new_plane)
                    model_line = doc.Create.NewModelCurve(curve, sketch_plane)
                    t.Commit()
                except:
                    t.RollBack()
                    pass
            # transform = element_of_edge.GetTransform()
            # if element_of_edge.HasModifiedGeometry() == False:
            #     transformed_line = vectortransform.transform_line(transform, origin_curve)
            #     point_moi = transformed_line.GetEndPoint(0)
            #     point_cu = origin_curve.GetEndPoint(0)
            #     translation_vector = XYZ(point_moi.X- point_cu.X, point_moi.Y- point_cu.Y, point_moi.Z- point_cu.Z)
            #     t2 = Transaction(doc, 'Move line')
            #     t2.Start()
            #     if not element_of_edge.HasModifiedGeometry():
            #         new_line_1 = Autodesk.Revit.DB.ElementTransformUtils.MoveElement(doc, model_line.Id, translation_vector)
            #     t2.Commit()
            select = uidoc.Selection
            listid = []
            listid.append(model_line.Id)
            Icollection = List[ElementId](listid)
            select.SetElementIds(Icollection)
    except:
        pass

    