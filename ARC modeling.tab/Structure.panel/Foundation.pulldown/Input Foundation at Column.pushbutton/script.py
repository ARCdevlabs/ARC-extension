# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
try:
    import Autodesk
    from Autodesk.Revit.DB import *
    from System.Collections.Generic import *
    from Autodesk.Revit.UI.Selection import ObjectType
    from pyrevit import revit, DB, UI
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    def input_family_instance(point, type, level):
        structural_type = Autodesk.Revit.DB.Structure.StructuralType.NonStructural
        family_instance = doc.Create.NewFamilyInstance(point,type,level,structural_type)
        return family_instance
    Ele = module.get_elements(uidoc,doc, "Select Column", noti = False)
    if Ele:
        t = Transaction (doc, "Đặt móng tại vị trí cột")
        t.Start()
        message = "Bây giờ hãy pick 1 móng đã vẽ sẵn, tool sẽ giúp copy ra các chân cột.\n \n既に入力された基礎を1つ選び、ツールがそれをコピーして柱脚に配置します。"
        module.message_box(message)
        pick = uidoc.Selection.PickObject(ObjectType.Element)
        sample = doc.GetElement(pick.ElementId)
        sample_offset = module.get_builtin_parameter_by_name(sample, DB.BuiltInParameter.INSTANCE_FREE_HOST_OFFSET_PARAM)
        sample_type = sample.Symbol
        sample_level = doc.GetElement(sample.LevelId)
        sample_location = sample.Location.Point
        for i in Ele:
            loca = i.Location.Point
            translate = XYZ(-sample_location.X + loca.X,-sample_location.Y + loca.Y,-sample_location.Z + loca.Z)
            copy_element = Autodesk.Revit.DB.ElementTransformUtils.CopyElement(doc, pick.ElementId, translate)
            copy_element_offset = module.get_builtin_parameter_by_name(doc.GetElement(copy_element[0]), DB.BuiltInParameter.INSTANCE_FREE_HOST_OFFSET_PARAM)
            copy_element_offset.Set(sample_offset.AsDouble())
        t.Commit()
except:
    pass