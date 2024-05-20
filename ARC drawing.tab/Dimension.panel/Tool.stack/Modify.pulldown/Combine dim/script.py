# -*- coding: utf-8 -*-
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
__doc__ = 'nguyenthanhson1712@gmail.com'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
#Get Document 

from Autodesk.Revit.UI.Selection import ObjectType, Selection

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
def xac_dinh_kich_co_chu (view,value):
    round_format_value = round(value,2)
    formatted_value = str(round_format_value).rstrip('0').rstrip('.')
    len_formatted_value = len(formatted_value)
    one_unit_width = 1.8 #Chieu rong 1 don vi text
    width_text = float(len_formatted_value * one_unit_width * (view.Scale))
    return width_text


def move_point_along_vector(point, vector, distance):
    new_point = point + vector.Normalize() * distance
    return new_point



def add_prefix_to_dimension(dimension):
    try:
        dimension.Prefix = "W="
    except:
        pass    

def orientation(A, B, vector):
    C = move_point_along_vector(B, vector, 1)
    # Chuyển đổi tọa độ thành tuple
    # Vector AB
    vector_AB = (B.X - A.X, B.Y - A.Y)
    # Vector BC
    vector_BC = (C.X - B.X, C.Y - B.Y)
    # Tính cross product
    cross_product = vector_AB[0] * vector_BC[1] - vector_AB[1] * vector_BC[0]
    # Xác định hướng dựa trên dấu của cross product
    if cross_product > 0:
        ket_qua = "Bên trái"
    elif cross_product < 0:
        ket_qua = "Bên phải"
    else:
        ket_qua= "Thẳng hàng"        
    return ket_qua


def distance(point1, point2):
    return ((point2.X - point1.X)**2 + (point2.Y - point1.Y)**2)**0.5


def distance_from_point_to_element(point1, obj):
    return distance(point1, obj.Origin)

def sort_points_by_distance(A, points_list):
    # Sắp xếp các điểm trong list dựa trên khoảng cách từ xa đến gần điểm A
    sorted_points = sorted(points_list, key=lambda point: distance(A, point), reverse=False)
    return sorted_points


def sort_seg_by_distance(A, seg_list):
    # Sắp xếp các điểm trong list dựa trên khoảng cách từ xa đến gần điểm A
    sorted_points = sorted(seg_list, key=lambda obj: distance_from_point_to_element(A, obj), reverse=False)
    return sorted_points

def add_prefix_to_dimension(dimension):
    try:
        dimension.Prefix = ","
    except:
        pass   

def add_suffix_to_dimension(dimension):
    try:
        dimension.Suffix = ","
    except:
        pass     

def remove_suffix_prefix(dimension):
    try:
        dimension.Suffix = ""
    except:
        pass
    try:
        dimension.Prefix = ""
    except:
        pass  

def find_farthest_points(points):
    from itertools import combinations
    from Autodesk.Revit.DB import XYZ
    # Tạo tất cả các cặp điểm từ danh sách
    point_combinations = list(combinations(points, 2))

    # Tìm cặp điểm có khoảng cách lớn nhất
    max_distance = 0
    farthest_points = None

    for pair in point_combinations:
        distance = pair[0].DistanceTo(pair[1])
        if distance > max_distance:
            max_distance = distance
            farthest_points = pair

    return farthest_points

def find_midpoint(point_a, point_b):
    # Tính toán điểm chính giữa
    midpoint = (point_a + point_b) / 2
    return midpoint


# t0 = Transaction(doc,"Set workplane")
# t0.Start()        
# current_view = uidoc.ActiveView
# try:
#     set_work_plane_for_view (current_view)
# except:
#     pass
# t0.Commit()   


# collector = FilteredElementCollector(uidoc.Document, current_view.Id).OfCategory(BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType()
current_view = uidoc.ActiveView
# pick = uidoc.Selection.PickObject(ObjectType.Element)
Ele = module.get_selected_elements(uidoc,doc)
t = Transaction(doc,"Gộp dim")
t.Start() 
he_so = 1.7
all_ref = ReferenceArray()
list_all_ref =[]
for element in Ele:
    ref_array = element.References
    line = element.Curve
    for ref in ref_array:
        string_stable_ref = ref.ConvertToStableRepresentation(doc)
        ref_sau = Autodesk.Revit.DB.Reference.ParseFromStableRepresentation(doc, string_stable_ref)
        all_ref.Append(ref_sau)
        print ref_sau

# seen = set()
# # Tạo một danh sách mới để chứa các đối tượng không trùng nhau
# unique_objects = []
# # Lặp qua các đối tượng trong danh sách ban đầu
# for obj in list_all_ref:
#     # Kiểm tra xem đối tượng đã được thấy trước đó chưa
#     if obj not in seen:
#         # Nếu chưa thấy, thêm vào danh sách mới và đánh dấu là đã thấy
#         unique_objects.append(obj)
#         seen.add(obj)
# for uni_ref in unique_objects:
#     all_ref.Append(uni_ref)
new_dim = doc.Create.NewDimension(current_view, line, all_ref)
new_dim_ref = new_dim.References
for a in new_dim_ref:
    print a
segments = new_dim.Segments
# for seg in segments:
#     seg_value = seg.Value
#     if seg_value == 0:
#         print dir(seg)
t.Commit()






