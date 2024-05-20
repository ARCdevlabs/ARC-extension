__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
from re import X
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import Transaction, ForgeTypeId
from System.Collections.Generic import *
import Autodesk.Revit.UI.Selection
import sys
from Autodesk.Revit.UI.Selection import ObjectType, ObjectSnapTypes
from Autodesk.Revit.UI import UIDocument
from System.Windows.Forms import Form, Label, TextBox, Button, ComboBox, ComboBoxStyle, MessageBox, FormStartPosition
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    pick = uidoc.Selection.PickObjects(ObjectType.PointOnElement)
    list_point = []
    for i in pick:
        element = doc.GetElement(i)
        geometry = element.GetGeometryObjectFromReference(i)
        point = i.GlobalPoint
        list_point.append(point)
    # plane = Autodesk.Revit.DB.Plane.CreateByThreePoints(list_point[0],list_point[1],list_point[2])
    # one_point_of_plane = list_point[0]
    # Autodesk.Revit.UI.TaskDialog.Show("ARC", "Ok, Please select all points need to set elevation")
    MessageBox.Show("Ok, Please select all points need to set elevation", "Message")
    pick_2 = uidoc.Selection.PickObjects(ObjectType.PointOnElement)
    list_point_2 = []
    t = Transaction (doc, "Set subelement of floor with 2 points")
    t.Start()
    # def calculate_Z (X,Y, plane):
    #     point_on_plane = plane.Origin

    #     normal_vector = plane.Normal

    #     a = normal_vector.X
    #     b = normal_vector.Y
    #     c = normal_vector.Z
    #     d = -(a * point_on_plane.X + b * point_on_plane.Y + c * point_on_plane.Z)
    #     Z = (-a * X - b * Y - d) / c
    #     return Z

    def calculate_direction_vector(A, B):
        direction_vector = (B.X - A.X, B.Y - A.Y, B.Z - A.Z)
        return direction_vector


    def calculate_z_coordinate(A, B, x, y):
        if A == B:
            return None
        if B.X - A.X >= 0.001 and B.X - A.X <= -0.001:
            z_coordinate = A.Z + ((x - A.X) / (B.X - A.X)) * (B.Z - A.Z)
        else:
            z_coordinate = A.Z + ((y - A.Y) * (B.Z - A.Z)) / (B.Y - A.Y)
        return z_coordinate
    def check_point_on_line(A, B, C):
        if A == B:
            return False
        try:
            calculated_x = A.X + ((C.Z - A.Z) / (B.Z - A.Z)) * (B.X - A.X)
            calculated_y = A.Y + ((C.Z - A.Z) / (B.Z - A.Z)) * (B.Y - A.Y)
            if abs(calculated_x - C.X) < (1.640419948) and abs(calculated_y - C.Y) < (1.640419948): #khoang 500mm khi quy doi tu feet sang mm
                return True
            else:
                return False
        except:
            return True
    def get_level_of_floor(floor):
        level_id = floor.LevelId
        get_level = doc.GetElement(level_id)
        return get_level.ProjectElevation

    for i in pick_2:
        element_id = i.ElementId
        element_2 = doc.GetElement(i)
        get_floor = doc.GetElement(element_id)
        geometry_2 = element_2.GetGeometryObjectFromReference(i)
        point_2 = i.GlobalPoint
        list_point_2.append(point_2)
    slab_shape_editor = get_floor.SlabShapeEditor.SlabShapeVertices
    for i in slab_shape_editor:
        position = i.Position
        for x in list_point_2:
            if position.X == x.X:
                if position.Y == x.Y:
                    vecto_chi_phuong  = calculate_direction_vector (list_point[0], list_point[1])
                    Z = calculate_z_coordinate(list_point[0], list_point[1], x.X, x.Y)
                    C =  Autodesk.Revit.DB.XYZ(x.X, x.Y, Z)
                    if check_point_on_line(list_point[0], list_point[1], C):
                        height_offset = get_floor.GetParameter(ForgeTypeId('autodesk.revit.parameter:floorHeightabovelevelParam-1.0.0')).AsDouble()
                        plane_of_host_floor = get_level_of_floor(get_floor)                
                        floor_host_elevation = height_offset + plane_of_host_floor
                        Z_chenh_lech = Z - floor_host_elevation
                        get_floor.SlabShapeEditor.ModifySubElement(i, Z_chenh_lech)
                    else:
                        pass
    MessageBox.Show("Done", "Message")
    t.Commit()