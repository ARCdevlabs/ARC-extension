# -*- coding: utf-8 -*-
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
import Autodesk.Revit.DB as DB
from Autodesk.Revit.UI.Selection import ObjectType, ObjectSnapTypes
from Autodesk.Revit.UI import UIDocument
from System.Windows.Forms import Form, Label, TextBox, Button, ComboBox, ComboBoxStyle, MessageBox, FormStartPosition
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    from pyrevit import forms
    with forms.WarningBar(title='Pick 3 điểm sub element để tạo thành 1 mặt phẳng, sau đó ấn Finish'):
        pick = uidoc.Selection.PickObjects(ObjectType.PointOnElement)
    list_point = []
    for i in pick:
        element = doc.GetElement(i)
        geometry = element.GetGeometryObjectFromReference(i)
        point = i.GlobalPoint
        list_point.append(point)
    plane = Autodesk.Revit.DB.Plane.CreateByThreePoints(list_point[0],list_point[1],list_point[2])
    one_point_of_plane = list_point[0]
    MessageBox.Show("Giờ thì chọn các điểm cần chỉnh sub element của sàn", "Message")
    def main():
    # Bat dau vong lap lua chon
        while True:
            try:
                with forms.WarningBar(title='Pick từng điểm để chỉnh sub element của sàn'):
                    pick_2 = uidoc.Selection.PickObject(ObjectType.PointOnElement)
                list_point_2 = []
                t = Transaction (doc, "Set subelement of floor")
                t.Start()
                def calculate_Z (X,Y, plane):
                    point_on_plane = plane.Origin

                    normal_vector = plane.Normal

                    a = normal_vector.X
                    b = normal_vector.Y
                    c = normal_vector.Z
                    d = -(a * point_on_plane.X + b * point_on_plane.Y + c * point_on_plane.Z)
                    Z = (-a * X - b * Y - d) / c
                    return Z

                def get_level_of_floor(floor):
                    level_id = floor.LevelId
                    get_level = doc.GetElement(level_id)
                    return get_level.ProjectElevation


                element_id = pick_2.ElementId
                element_2 = doc.GetElement(pick_2)
                get_floor = doc.GetElement(element_id)
                geometry_2 = element_2.GetGeometryObjectFromReference(pick_2)
                point_2 = pick_2.GlobalPoint
                list_point_2.append(point_2)

                slab_shape_editor = get_floor.SlabShapeEditor.SlabShapeVertices
                for i in slab_shape_editor:
                    position = i.Position
                    for x in list_point_2:
                        if position.X == x.X:
                            if position.Y == x.Y:
                                Z = calculate_Z(x.X, x.Y, plane)
                                # height_offset = get_floor.GetParameter(ForgeTypeId('autodesk.revit.parameter:floorHeightabovelevelParam-1.0.0')).AsDouble()
                                # height_offset = float(module.get_parameter_value_by_name(get_floor, "Height Offset From Level", False))
                                height_offset = (module.get_builtin_parameter_by_name(element, DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM).AsDouble())
                                convert_feet_to_mm = height_offset
                                plane_of_host_floor = get_level_of_floor(get_floor)                
                                floor_host_elevation = convert_feet_to_mm + plane_of_host_floor
                                Z_chenh_lech = Z - floor_host_elevation
                                get_floor.SlabShapeEditor.ModifySubElement(i, Z_chenh_lech)
                # MessageBox.Show("Done", "Message")
                t.Commit()
            except Exception as ex:
                if "Đã cancel" in str(ex):
                    break
                else:
                    break
    main()
