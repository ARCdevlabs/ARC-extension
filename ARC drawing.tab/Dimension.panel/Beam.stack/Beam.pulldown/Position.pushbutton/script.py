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
            return isinstance(element, FamilyInstance) and element.Category.Name == "Structural Framing"

        def AllowReference(self, reference, point):
            # Không sử dụng AllowReference trong trường hợp này
            return False
    # Hàm chọn một Dimension từ danh sách sử dụng ISelectionFilter
    def pick_filter_elements():
        selected_dimension = uidoc.Selection.PickObjects(Autodesk.Revit.UI.Selection.ObjectType.Element, DimensionSelectionFilter(), "Chọn Framing")
        return selected_dimension if selected_dimension else None
        

    class BeamSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
        def AllowElement(self, element):
            return isinstance(element, FamilyInstance) and element.Category.Name == "Structural Framing"

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

    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    list_element_da_chon = []
    beam_elements_list = get_beam_elements()
    if beam_elements_list:
        selected_beams = pick_beams_by_rectangle()
        for moi_element in selected_beams:
            ref_cua_element = moi_element.GetReferences(Autodesk.Revit.DB.FamilyInstanceReferenceType.CenterFrontBack)
            list_element_da_chon.append(ref_cua_element[0])
    # picks = uidoc.Selection.PickObjects(ObjectType.Element)
    picks = list_element_da_chon
    ref_array = ReferenceArray()
    covert_reference_to_element = []
    for i in picks:
        # ref_array.Append(i)
        element_id = i.ElementId
        covert_reference_to_element.append(doc.GetElement(element_id))


    '''Dùng thuật toán bucket sorting để tìm ra group có số lượng dầm song song nhiều nhất'''
    parallel_groups = []
    for tung_beam in covert_reference_to_element:
        found_group = False
        direction = get_direction_of_beam(tung_beam)
        for group in parallel_groups:            
            # Kiểm tra xem vector của dầm có song song với dầm trong nhóm không
            if are_vector_parallel(group[0], direction):
                group.append(tung_beam)
                found_group = True
                break

        # Nếu không tìm thấy nhóm nào, tạo nhóm mới
        if not found_group:
            parallel_groups.append([direction, tung_beam])
    try:
        largest_group = max(parallel_groups, key=lambda g: len(g))
    except:
        sys.exit()
    
    # print("Nhóm có số dầm song song nhiều nhất: ")
    # for beam in largest_group[1:]: # Bỏ qua vector đầu tiên
    #     print("Dầm ID: {}".format(beam.Id))
       

    vector_beam = get_direction_of_beam(largest_group[1])  # Bỏ qua giá trị đầu tiên vì giá trị đầu tiên là vector, không phải dầm.

    vector_beam_Z0 = XYZ(vector_beam.X, vector_beam.Y,0)
    
    list_dam_song_song = []
    for beam, ref_beam in zip(covert_reference_to_element,picks):
        try:
            # direction = beam.Location.Curve.Direction
            direction = get_direction_of_beam(beam)
            direction_Z0 = XYZ(direction.X, direction.Y,0)
            if direction:
                check_song_song = are_vector_parallel (vector_beam_Z0, direction_Z0)
                if check_song_song:
                    try:
                        para_cross_section = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEND_DIR_ANGLE)
                        if para_cross_section.AsDouble() == 0:
                            ref_array.Append(ref_beam)        
                    except:
                        ref_array.Append(ref_beam) 

        except:
            pass
    pick = pick_point_with_nearest_snap()
    xoay_vector_90_do = XYZ(-vector_beam.Y, vector_beam.X, vector_beam.Z)
    new_point = move_point_along_vector(pick,xoay_vector_90_do, 1)

    line = Line.CreateBound(pick,new_point)
    Currentview = doc.ActiveView

    t = Transaction(doc,"Dim position of beam")
    t.Start()
    try:
        dim = create_dim(Currentview,line,ref_array)
        t.Commit()
    except:
        t.RollBack()