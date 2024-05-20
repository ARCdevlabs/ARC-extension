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

t0 = Transaction(doc,"Set workplane")
t0.Start()        
current_view = uidoc.ActiveView
try:
    set_work_plane_for_view (current_view)
except:
    pass
t0.Commit()   


collector = FilteredElementCollector(uidoc.Document, current_view.Id).OfCategory(BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType()
pick = uidoc.Selection.PickObject(ObjectType.Element)
element = doc.GetElement(pick.ElementId)
return_point = pick_point_with_nearest_snap()

t = Transaction(doc,"Tách dim")
t.Start() 
# Tat leader line
tat_leader = module.set_parameter_value_by_name(element, "Leader", 0) 

seg_phai = []
vi_tri_phai = []
seg_trai = []
vi_tri_trai = []

segments = element.Segments
dim_line = element.Curve
vector = dim_line.Direction
gia_tri_ban_dau_phai = 0
gia_tri_ban_dau_trai = 0
for seg in segments:
    text_ori = seg.Origin
    value = seg.Value #Don vi dang la mm
    kich_co = xac_dinh_kich_co_chu(current_view, value*304.8)
    if value * 304.8 < kich_co:
        # move_lan_1 = move_point_along_vector(text_ori, vector, (kich_co + 20)/304.8)
        # move_lan_2 = move_point_along_vector(text_ori, vector, - (kich_co +20 )/304.8)
        xoay_vector_90_do = XYZ(-vector.Y, vector.X, vector.Z)
        xac_dinh_phia = orientation(text_ori,return_point,xoay_vector_90_do)
        if xac_dinh_phia == "Bên phải":
            gia_tri_ban_dau_phai = gia_tri_ban_dau_phai + value * 304.8
            seg_phai.append(seg)
            vi_tri_phai.append(text_ori)
            # seg.TextPosition = move_lan_1
        else:
            gia_tri_ban_dau_trai = gia_tri_ban_dau_trai + value * 304.8
            seg_trai.append(seg)
            vi_tri_trai.append(text_ori)
            # seg.TextPosition = move_lan_2

# Bên phải trước
view_scale = current_view.Scale
sorted_phai =  sort_seg_by_distance(return_point,seg_phai)
kich_co_phai = gia_tri_ban_dau_phai 

for seg_ben_phai in sorted_phai:
    value_phai = seg_ben_phai.Value
    vi_tri_phai = seg_ben_phai.Origin
    if len (sorted_phai) > 1:
        kich_co_phai = kich_co_phai + view_scale + xac_dinh_kich_co_chu(current_view, value_phai*304.8) /2
    else:
        kich_co_phai = kich_co_phai + xac_dinh_kich_co_chu(current_view, value_phai*304.8) /2
    move_phai = move_point_along_vector(vi_tri_phai, vector, (kich_co_phai)/304.8)
    # move_lan_2 = move_point_along_vector(text_ori, vector,(kich_co *2)/304.8)
    seg_ben_phai.TextPosition = move_phai
    kich_co_phai = kich_co_phai + 3* xac_dinh_kich_co_chu(current_view, value_phai*304.8)/2
    add_prefix_to_dimension (seg_ben_phai)
try:
    remove_suffix_prefix(sorted_phai[0])
except:
    pass

# Bên trái trước
sorted_trai =  sort_seg_by_distance(return_point,seg_trai)
kich_co_trai = gia_tri_ban_dau_trai 
for seg_ben_trai in sorted_trai:
    value_trai = seg_ben_trai.Value
    vi_tri_trai = seg_ben_trai.Origin
    if len (sorted_trai) > 1:
        kich_co_trai = kich_co_trai + view_scale +  xac_dinh_kich_co_chu(current_view, value*304.8)/2
    else: 
        kich_co_trai = kich_co_trai +  xac_dinh_kich_co_chu(current_view, value*304.8)/2
    move_trai = move_point_along_vector(vi_tri_trai, vector, -(kich_co_trai)/304.8)
    seg_ben_trai.TextPosition = move_trai
    kich_co_trai = kich_co_trai +  3* xac_dinh_kich_co_chu(current_view, value*304.8)/2
    add_suffix_to_dimension (seg_ben_trai)
try:    
    remove_suffix_prefix(sorted_trai[0])
except:
    pass
t.Commit()






