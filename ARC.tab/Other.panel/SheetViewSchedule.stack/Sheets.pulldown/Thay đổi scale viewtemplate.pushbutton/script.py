# -*- coding: utf-8 -*-
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FailuresAccessor
from Autodesk.Revit.DB import Line
from Autodesk.Revit.Creation import ItemFactoryBase
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
import string
import codecs
import importlib
import Autodesk
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script
def dat_view_vao_sheet (idoc, sheet_id, view_id, point):
    # kiem_tra = Autodesk.Revit.DB.Viewport.CanAddViewToSheet(idoc,sheet_id, view_id)
    # if kiem_tra:
    new_viewport = Autodesk.Revit.DB.Viewport.Create(idoc, sheet_id, view_id, point)
    return new_viewport
if module.AutodeskData():
    t = Transaction (doc, "Thay đổi scale view template")
    t.Start()
    Ele = module.get_selected_elements(uidoc,doc)
    from rpw.ui.forms import TextInput
    nhap_scale = TextInput('ARC: Nhập scale', default="100")
    for i in Ele:
        view_ports = i.GetAllViewports()
        for view_port in view_ports:
            lay_view_port = doc.GetElement(view_port)
            box_center_dau = lay_view_port.GetBoxCenter()
            view_id = lay_view_port.ViewId
            try:
                view_template = doc.GetElement(view_id).ViewTemplateId
                # try:
                lay_view_template = doc.GetElement(view_template)
                # lay_view_template_scale = doc.GetElement(view_template).Scale
                # print (lay_view_template_scale)
                # lay_view_template_scale = int(65)
                scale = module.get_parameter_by_name(lay_view_template, "Scale Value    1:", is_UTF8 = False)
                scale.Set(int(nhap_scale))
            except:
                pass




            # try:
            #     rotation = module.get_parameter_by_name(lay_view_port, "Rotation on Sheet", is_UTF8 = False)
            #     xoay = rotation.Set(int(2))
            #     box_center_sau = lay_view_port.GetBoxCenter()
            #     vector_move = XYZ(-box_center_sau.X + box_center_dau.X, -box_center_sau.Y + box_center_dau.Y,-box_center_sau.Z + box_center_dau.Z)
            #     move_element = Autodesk.Revit.DB.ElementTransformUtils.MoveElement(doc, lay_view_port.Id, vector_move)
            #     # delete_viewport_cu = i.DeleteViewport(lay_view_port)
            #     # Autodesk.Revit.DB.Viewport.Create(doc, i.Id, view_id, Autodesk.Revit.DB.XYZ(420.5/304.8,297/304.8,0))
            # except:
            #     pass

    t.Commit()
