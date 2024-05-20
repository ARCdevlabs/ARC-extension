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
        from pyrevit import forms
        with forms.WarningBar(title='Click 1 điểm bất kì để bố trí dim'):
            click_point = uidoc.Selection.PickPoint(snap_settings, prompt) 
    except:
        # print(traceback.format_exc())
        pass
    return click_point

def are_vector_parallel(vector_1, vector_2):
    tolerance=0.001
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
    from pyrevit import forms
    with forms.WarningBar(title='Quét chuột để chọn các dầm cần dim'):
        selection = uidoc.Selection
        selected_elements = selection.PickElementsByRectangle(BeamSelectionFilter(), "Chọn các dầm")
    return selected_elements


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

vector_beam = covert_reference_to_element[0].Location.Curve.Direction
vector_beam_Z0 = XYZ(vector_beam.X, vector_beam.Y,0)
list_dam_song_song = []


for beam, ref_beam in zip(covert_reference_to_element,picks):
    try:
        direction = beam.Location.Curve.Direction
        direction_Z0 = XYZ(direction.X, direction.Y,0)
        if direction:
            check_song_song = are_vector_parallel (vector_beam_Z0, direction_Z0)
            if check_song_song:
                ref_array.Append(ref_beam)
            else:
                dialog = TaskDialog("ARC: Thông báo")
                thong_bao = "Có dầm không song song, ID là: " + str(beam.Id)
                dialog.MainContent = thong_bao
                dialog.TitleAutoPrefix = False
                dialog.Show()
    except:
        ref_array.Append(ref_beam)
        # import traceback
        # print(traceback.format_exc())
        pass


pick = pick_point_with_nearest_snap()
xoay_vector_90_do = XYZ(-vector_beam.Y, vector_beam.X, vector_beam.Z)
new_point = move_point_along_vector(pick,xoay_vector_90_do, 1)

line = Line.CreateBound(pick,new_point)
Currentview = doc.ActiveView

t = Transaction(doc,"Dimension beam (centered)")
t.Start()

dim = create_dim(Currentview,line,ref_array)

t.Commit()