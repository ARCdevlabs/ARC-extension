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
try:
    if module.AutodeskData():
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        from nances import forms
        from pyrevit.coreutils import applocales
        current_applocale = applocales.get_current_applocale()
        if str(current_applocale) == "日本語 / Japanese (ja)":
            message = "3 つのサブ要素点を選択して平面を形成し、[完了]を押します。"
        else:
            message = "Pick 1 điểm sub element để tạo thành 1 mặt phẳng, sau đó ấn Finish"

        with forms.WarningBar(title = message):
            
            pick = uidoc.Selection.PickObject(ObjectType.PointOnElement)
            if pick:
                element = doc.GetElement(pick)
                geometry = element.GetGeometryObjectFromReference(pick)
                point = pick.GlobalPoint
             
                def main():
                    while True:
                        try:
                            with forms.WarningBar(title='Select Sub Elements'):
                                pick_2 = uidoc.Selection.PickObject(ObjectType.PointOnElement)

                            def get_level_of_floor(floor):
                                level_id = floor.LevelId
                                get_level = doc.GetElement(level_id)
                                return get_level.ProjectElevation


                            element_id = pick_2.ElementId
                            get_floor = doc.GetElement(element_id)

                            point_2 = pick_2.GlobalPoint

                            slab_shape_editor = get_floor.SlabShapeEditor.SlabShapeVertices
                            t = Transaction (doc, "Set subelement of floor")
                            t.Start()
                            for i in slab_shape_editor:
                                position = i.Position
                                if position.X == point_2.X:
                                    if position.Y == point_2.Y:
                                            
                                            Z = point.Z
                                            
                                            height_offset = (module.get_builtin_parameter_by_name(element, DB.BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM).AsDouble())

                                            plane_of_host_floor = get_level_of_floor(get_floor)     

                                            floor_host_elevation = height_offset + plane_of_host_floor

                                            Z_chenh_lech = Z- floor_host_elevation

                                            get_floor.SlabShapeEditor.ModifySubElement(i, Z_chenh_lech)

                            t.Commit()
                        except Exception as ex:
                            if "Canceled" in str(ex):
                                break
                            else:
                                break
                main()
except:
    pass