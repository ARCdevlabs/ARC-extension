# -*- coding: utf-8 -*-
import string
import importlib
#Get UIDocument
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
from Autodesk.Revit.UI.Selection import ObjectType
def create_plane_from_three_points(point1, point2, point3):
    plane = Plane.CreateByThreePoints(point1, point2, point3)
    return plane
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document

    currentview = doc.ActiveView
    def pick_point_with_nearest_snap():       
        snap_settings = Autodesk.Revit.UI.Selection.ObjectSnapTypes.Nearest
        prompt = "Click"
        try:
            click_point = uidoc.Selection.PickPoint(snap_settings, prompt)
        except:
            # print(traceback.format_exc())
            pass
        return click_point
    t = Transaction (doc, "Tạo sample model để tạo bảng thống kê")
    t.Start()
    Ele = module.get_selected_elements(uidoc,doc)
    module.message_box("Ok, bây giờ thì chọn 1 đối tượng mẫu")
    pick = uidoc.Selection.PickObject(ObjectType.Element)
    # module.message_box("Tiếp tục chọn điểm để bắt đầu copy")
    # start_point = pick_point_with_nearest_snap()
    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                Separator, Button, CheckBox)
    components = [Label('Nhập khoảng cách'),
                    TextBox('textbox1', Text="1500"),
                #   CheckBox('checkbox1', 'Check this'), (khong can check box)
                    Separator(),
                    Button('Ok')]
    form = FlexForm('ARC tools', components)
    form.show()
    form.values
    khoang_cach_dau_vao = float(form.values["textbox1"])
    n = 1
    for i in Ele:
        # print dir(i)

        khoang_cach = n * (khoang_cach_dau_vao/304.8)
        new_position = XYZ(khoang_cach, 0, 0)
        copy_element = Autodesk.Revit.DB.ElementTransformUtils.CopyElement(doc, pick.ElementId, new_position)
        for tung_ele in copy_element:
            lay_element = doc.GetElement(tung_ele)
            doi_type = lay_element.ChangeTypeId(i.Id)
        n += 1
    t.Commit()



    