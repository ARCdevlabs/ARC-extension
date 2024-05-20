__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
import Autodesk
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

#Get Document 

from Autodesk.Revit.UI.Selection import ObjectType, Selection
def main():
    # Bat dau vong lap lua chon
    while True:
        try:
            uidoc = __revit__.ActiveUIDocument
            doc = uidoc.Document
            from pyrevit import revit, DB, UI

            def set_work_plane_for_view(view):


                current_work_plane = view.SketchPlane
                

                if current_work_plane is None:
                    sketch_plane = view.SketchPlane
                    try:
                        sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(view.Document, Autodesk.Revit.DB.Plane.CreateByNormalAndOrigin(view.ViewDirection, view.Origin))
                        view.SketchPlane = sketch_plane
                    except:
                        pass
                        # print(traceback.format_exc())
                return True

                

            def pick_point_with_nearest_snap():       
                snap_settings = UI.Selection.ObjectSnapTypes.None
                prompt = "Click"
                
                try:

                    click_point = uidoc.Selection.PickPoint(snap_settings, prompt)
                    
                except:
                    # print(traceback.format_exc())
                    pass
                return click_point




            def get_nearest_point(points, reference_point):

                min_distance = float('inf')
                nearest_point = None
                
                for point in points:
                    distance = point.DistanceTo(reference_point)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_point = point
                return nearest_point

            def distance_2_point(point , reference_point):
                distance = point.DistanceTo(reference_point)
                return distance


            def add_prefix_to_dimension(dimension):
                try:
                    dimension.Prefix = "W="
                except:
                    pass    
            t0 = Transaction(doc,"Set workplane")
            t0.Start()        
            current_view = uidoc.ActiveView
            try:
                set_work_plane_for_view (current_view)
            except:
                pass
            t0.Commit()   
            return_point = pick_point_with_nearest_snap()
            collector = FilteredElementCollector(uidoc.Document, current_view.Id).OfCategory(BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType()

            list_dimension_and_seg= []
            list_dim_seg_point = []
            list_each_dimension = []
            t = Transaction(doc,"Add W=")
            t.Start()  
            for dimension in collector:
                number_segment = dimension.NumberOfSegments
                if number_segment > 1:
                    segments = dimension.Segments
                    for seg in segments:
                        list_dimension_and_seg.append(seg)
                else:
                    list_dimension_and_seg.append(dimension)
            for each_dim in list_dimension_and_seg:
                seg_posi = each_dim.TextPosition
                list_dim_seg_point.append(seg_posi)
            zipped_seg = zip(list_dimension_and_seg, list_dim_seg_point)
            nearest_point_to_seg = get_nearest_point(list_dim_seg_point, return_point)
            if distance_2_point(nearest_point_to_seg, return_point) < 3:
                for dim_seg, dim_seg_point in zipped_seg:
                    if dim_seg_point == nearest_point_to_seg:
                        choosen_seg = dim_seg
                        add_prefix_to_dimension(choosen_seg)
                        break
            t.Commit()
        except Exception as ex:
            if "Operation canceled by user." in str(ex):
                break
            else:
                break
main()









