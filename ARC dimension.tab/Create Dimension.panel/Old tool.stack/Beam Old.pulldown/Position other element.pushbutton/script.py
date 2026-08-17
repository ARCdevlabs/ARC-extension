# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FailuresAccessor
from Autodesk.Revit.DB import Line
from Autodesk.Revit.Creation import ItemFactoryBase
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
import Autodesk.Revit.DB as DB
import math
import sys
import string
import importlib
import traceback
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
import Autodesk.Revit.UI.Selection
import sys
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.UI import *
from pyrevit import revit, DB, UI
if module.AutodeskData():
    try:
        def create_dim(view, line, ref):
            dim = doc.Create.NewDimension(view, line, ref)
            return dim

        def move_point_along_vector(point, vector, distance):
            new_point = point + vector.Normalize() * distance
            return new_point

        def pick_point_with_nearest_snap():    
            snap_settings = UI.Selection.ObjectSnapTypes.Nearest
            prompt = "Bấm vào vị trí mà cần bố trí dim"
            try:
                from nances import forms
                with forms.WarningBar(title='Click 1 điểm bất kì để bố trí dim'):
                    click_point = uidoc.Selection.PickPoint(snap_settings, prompt) 
            except:
                # print(traceback.format_exc())
                pass
            return click_point

        def are_vector_parallel(vector_1, vector_2):
            tolerance=0.0001
            cross_product = vector_1.CrossProduct(vector_2)
            return cross_product.GetLength() < tolerance



        class DimensionSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
            def AllowElement(self, element):
                return isinstance(element, FamilyInstance) and element.Category.Name == "Casework"

            def AllowReference(self, reference, point):
                # Không sử dụng AllowReference trong trường hợp này
                return False
        # Hàm chọn một Dimension từ danh sách sử dụng ISelectionFilter
        def pick_filter_elements():
            selected_dimension = uidoc.Selection.PickObjects(Autodesk.Revit.UI.Selection.ObjectType.Element, DimensionSelectionFilter(), "Chọn Framing")
            return selected_dimension if selected_dimension else None
            

        class BeamSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
            def AllowElement(self, element):
                return isinstance(element, FamilyInstance) and element.Category.Name == "Casework"

            def AllowReference(self, reference, point):
                return False

        def get_beam_elements():
            collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType()
            return list(collector)

        def pick_beams_by_rectangle():
            from nances import forms
            with forms.WarningBar(title='Quét chuột để chọn các dầm cần dim'):
                selection = uidoc.Selection
                selected_elements = selection.PickElementsByRectangle(BeamSelectionFilter(), "Chọn các dầm")
            return selected_elements
        
        def get_direction_of_beam(beam):
            location_curve = beam.Location.Curve
            start_point = location_curve.GetEndPoint(0)
            end_point = location_curve.GetEndPoint(1)
            vector_beam = XYZ(end_point.X - start_point.X,end_point.Y - start_point.Y,0)    
            return vector_beam
        
        from Autodesk.Revit.DB import BuiltInCategory

        class LineAndGridSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):

            def AllowElement(self, element):
                if element.Category is None:
                    return False

                return element.Category.Id.IntegerValue in (
                    int(BuiltInCategory.OST_Casework),
                    int(BuiltInCategory.OST_Grids)
                )

            def AllowReference(self, reference, point):
                return False
            
        def pick_lines_and_grid_by_rectangle():
            from nances import forms
            with forms.WarningBar(title='Quét chuột để chọn các line cần dim'):
                selection = uidoc.Selection
                selected_elements = selection.PickElementsByRectangle(LineAndGridSelectionFilter(), "Chọn các line")
            return selected_elements

        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        list_element_da_chon = []

        selected_beams = pick_lines_and_grid_by_rectangle()


        # selected_beams = pick_beams_by_rectangle()


        ref_array = ReferenceArray()

        for moi_element in selected_beams:
            category_name = moi_element.Category.Name
            if str(category_name) == "Grids":
                ref_grid = Reference(moi_element)
                ref_array.Append(ref_grid)
                continue
            else:
                ref_cua_element = moi_element.GetReferences(Autodesk.Revit.DB.FamilyInstanceReferenceType.CenterLeftRight)
                
                list_element_da_chon.append(ref_cua_element[0])
            
        picks = list_element_da_chon
        
        covert_reference_to_element = []
        for ref_beam in picks:
            ref_array.Append(ref_beam) 
        pick = pick_point_with_nearest_snap()
        pick_lan_2 = pick_point_with_nearest_snap()
        line = Line.CreateBound(pick,pick_lan_2)
        Currentview = doc.ActiveView

        t = Transaction(doc,"Dim position of beam")
        t.Start()
        try:
            dim = create_dim(Currentview,line,ref_array)
            t.Commit()
        except:
            print(traceback.format_exc())
            t.RollBack()
    except:
        print(traceback.format_exc())
        pass