# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))

import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit import revit, DB, UI

import math

def normalize(vector):
    """Hàm để chuẩn hóa một vector."""
    norm = math.sqrt(sum(x ** 2 for x in vector))
    return tuple(x / norm for x in vector)

def dot_product(v1, v2):
    """Hàm để tính tích vô hướng của hai vector."""
    return sum(x * y for x, y in zip(v1, v2))

def cross_product(v1, v2):
    """Hàm để tính tích có hướng của hai vector."""
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    )

def rotate_vector(vector_A, vector_B, angle_degrees):
    """
    Xoay vector_A quanh vector_B một góc tùy chỉnh.

    Args:
    vector_A (tuple): Vector cần xoay.
    vector_B (tuple): Vector trục xoay.
    angle_degrees (float): Góc xoay tính bằng độ.

    Returns:
    tuple: Vector đã được xoay.
    """
    # Chuyển vector thành tuple nếu cần
    if not isinstance(vector_A, tuple):
        vector_A = (vector_A.X, vector_A.Y, vector_A.Z)
    if not isinstance(vector_B, tuple):
        vector_B = (vector_B.X, vector_B.Y, vector_B.Z)

    # Chuẩn hóa vector_B để đảm bảo nó là vector đơn vị
    B = normalize(vector_B)
    
    # Chuyển đổi góc từ độ sang radian
    angle_radians = math.radians(angle_degrees)
    
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)
    
    dot = dot_product(vector_A, B)
    cross = cross_product(B, vector_A)
    
    rotated_vector_list = (
        cos_angle * vector_A[0] + sin_angle * cross[0] + (1 - cos_angle) * dot * B[0],
        cos_angle * vector_A[1] + sin_angle * cross[1] + (1 - cos_angle) * dot * B[1],
        cos_angle * vector_A[2] + sin_angle * cross[2] + (1 - cos_angle) * dot * B[2]
    )

    rotated_vector = XYZ(rotated_vector_list[0],rotated_vector_list[1],rotated_vector_list[2])

    return rotated_vector