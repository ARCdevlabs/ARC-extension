# -*- coding: utf-8 -*-
# pylint: disable=E0401,W0703,C0103
__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
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
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
Currentview = doc.ActiveView
try:
    ARC = string.ascii_lowercase
    begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
    module = importlib.import_module(str(begin))
    import Autodesk
    from Autodesk.Revit.DB import *
    from System.Collections.Generic import *
    if module.AutodeskData():
        Currentview = doc.ActiveView
        view_scale = Currentview.Scale
        Curve = []
except:
    sys.exit()

from pyrevit import script

# import this script's configurator
import type_config
# module_path = pick_config.__file__
# print(module_path)
logger = script.get_logger()
my_config = script.get_config()
source_categories = type_config.load_configs()

list_family = module.flatten_list(source_categories) #Đây là list tên family và tên type name của family tag


import base64
def encode_to_base64(input_string):
    input_bytes = input_string.encode('utf-8')
    base64_bytes = base64.b64encode(input_bytes)
    base64_string = base64_bytes.decode('utf-8')  
    return base64_bytes

def wall_direction_X(input_wall):
    location = input_wall.Location
    wall_vector = location.Curve.Direction
    x = wall_vector.X
    return x

def move_point_along_vector(point, vector, distance):
    new_point = point + vector.Normalize() * distance
    return new_point

def create_wall_tags(idoc, input_wall, view,tag_orientation = TagOrientation.Horizontal ):
    location = input_wall.Location
    tag_mode = TagMode.TM_ADDBY_CATEGORY
    wall_ref = Reference(input_wall)
    # tag_orientation = TagOrientation.Horizontal
    wall_mid = location.Curve.Evaluate(0.5, True)
    tag = IndependentTag.Create(idoc, view.Id, wall_ref, False, tag_mode, tag_orientation, wall_mid)
    return tag

def get_wall_mid(input_wall):
    location = input_wall.Location
    wall_mid = location.Curve.Evaluate(0.5, True)
    return wall_mid

def get_wall_vector(input_wall):
    location = input_wall.Location
    vector = location.Curve.Direction
    return vector

def rotate_vector(vector):
    new_vector = XYZ(-vector.Y, vector.X, vector.Z)
    return new_vector

def get_family_by_name(idoc, family_name):
    # Sử dụng FilteredElementCollector để lấy tất cả các FamilySymbol trong dự án
    collector = FilteredElementCollector(idoc).OfClass(FamilySymbol)

    # Lặp qua từng FamilySymbol để tìm family với family name cụ thể
    for symbol in collector:
        if symbol.FamilyName == family_name:
            return symbol.Family
def get_all_family_types(doc):
    # Sử dụng FilteredElementCollector để lấy tất cả các FamilySymbol trong dự án
    collector = FilteredElementCollector(doc).OfClass(FamilySymbol)

    # Lấy danh sách TypeId của từng FamilySymbol và trả về danh sách TypeId
    all_type_ids = [symbol.GetTypeId() for symbol in collector]
    
    return all_type_ids

# Gọi family ra
get_family = get_family_by_name(doc,list_family[0])
def get_type_by_family_and_type_name (idoc, family_name, type_name):
    get_family = get_family_by_name(idoc,family_name)
    all_type_of_family = get_family.GetFamilySymbolIds()
    for type_id in all_type_of_family:
        element_type = doc.GetElement(type_id)
        element_type.Activate()
        name = module.get_parameter_value_by_name(element_type, "Type Name")
        if name == type_name:
            return type_id
def ChangeType(element, typeId):
    try:
        element.ChangeTypeId(typeId)
        return element
    except:
        pass
#1: LGS+ board slab to slab
# TEdTK+ODnOODvOODieWFseOCueODqeODlnRv44K544Op44OW

#2:  LGS only slab to slab
# TEdT44Gu44G/44K544Op44OWdG/jgrnjg6njg5Y=

#3: LGS + board up to the ceiling
# TEdTK+ODnOODvOODieWFseWkqeS6leOBvuOBpw==

#4:  LGS+Board Slab to Slab_Sub
# TEdTK+ODnOODvOODieWFseOCueODqeODlnRv44K544Op44OWX+OCteODlg==

#5:  LGS only slab to slab_sub
# TEdT44Gu44G/44K544Op44OWdG/jgrnjg6njg5Zf44K144OW

#6:  LGS + board sub to ceiling
# TEdTK+ODnOODvOODieWFseWkqeS6leOBvuOBp1/jgrXjg5Y=


# LGS+ボード共スラブtoスラブ
# LGSのみスラブtoスラブ
# LGS+ボード共天井まで
# LGS+ボード共スラブtoスラブ_サブ
# LGSのみスラブtoスラブ_サブ
# LGS+ボード共天井まで_サブ

Ele = module.get_selected_elements(uidoc,doc)
t = Transaction(doc,"Tag tường LGS theo tiêu chuẩn Meada")
t.Start()
try:
    for wall in Ele:
        list_tag = []
        # para_value_1 = "a"
        # para_value_2 = "a"
        # para_value_3 = "a"
        # para_value_4 = "a"
        # para_value_5 = "a"
        # para_value_6 = "a"
        point_center = get_wall_mid (wall)
        which_param = []
        wall_vector = get_wall_vector(wall)
        get_wall_type = module.get_type(doc, wall)
        rotate = rotate_vector (wall_vector)
        para_set = get_wall_type.Parameters
        get_type_wall_width = get_wall_type.Width
        view_scale = Currentview.Scale
        new_point_center_1 = move_point_along_vector(point_center, rotate, 0.3*(view_scale/50) + get_type_wall_width) #Dua tren scale 1/50
        new_point_center_2 = move_point_along_vector(point_center, rotate,-0.3*(view_scale/50) - get_type_wall_width)  #Dua tren scale 1/50

        for para in para_set:
            para_name = para.Definition.Name
            # print para_name
            try:
                if para_name == "LGS+ボード共スラブtoスラブ":
                    para_value_1 = para.AsValueString()
                    if len (para_value_1) > 1:
                        which_param.append(1)
                        continue
            except:
                pass
                # print para_value_1
            try:
                if para_name == "LGSのみスラブtoスラブ=":
                    para_value_2 = para.AsValueString()
                    if len (para_value_2) > 1:
                        which_param.append(2)
                        continue
            except:
                pass
                # print para_value_2
            try:
                if para_name == "LGS+ボード共天井まで":
                    para_value_3 = para.AsValueString()
                    if len (para_value_3) > 1:
                        which_param.append(3)
                        continue
            except:
                pass
            #     # print para_value_3
            try:
                if para_name == "LGS+ボード共スラブtoスラブ_サブ":
                    para_value_4 = para.AsValueString()
                    if len (para_value_4) > 1:          
                        which_param.append(4)
                        continue
            except:
                    pass
            #     # print para_value_4
            try:
                if para_name == "LGSのみスラブtoスラブ_サブ":
                    para_value_5 = para.AsValueString()
                    if len (para_value_5) > 1:
                        which_param.append(5)
            except:
                pass

            try:
                if para_name == "LGS+ボード共天井まで_サブ":
                    para_value_6 = para.AsValueString()
                    if len (para_value_6) > 1:
                        which_param.append(6)
                        continue
            except:
                pass
            else:
                continue
                # print para_value_6

        for each_param in which_param:
            direction = wall_direction_X(wall)
            if abs(direction) == 1:
                tag_wall = create_wall_tags(doc, wall, Currentview, TagOrientation.Horizontal)
                # xoay_tag = module.set_parameter_value_by_name(tag_wall, "Angle", 0)
            else:
                tag_wall = create_wall_tags(doc, wall, Currentview, TagOrientation.Vertical)
                # xoay_tag = module.set_parameter_value_by_name(tag_wall, "Angle", math.pi/2)
            type = get_type_by_family_and_type_name(doc, list_family[0],list_family[each_param])
            ChangeType(tag_wall, type)
            list_tag.append(tag_wall)
        try:
            list_tag[0].TagHeadPosition = new_point_center_1
        except:
            pass
        try:
            list_tag[1].TagHeadPosition = new_point_center_2
        except:
            # print(traceback.format_exc())
            pass
    t.Commit()
except:
    # print(traceback.format_exc())
    pass