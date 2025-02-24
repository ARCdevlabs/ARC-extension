# -*- coding: utf-8 -*-
import string
import importlib
#Get UIDocument
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
import traceback

def create_plane_from_three_points(point1, point2, point3):
    plane = Plane.CreateByThreePoints(point1, point2, point3)
    return plane
try:
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

        Ele = module.get_selected_elements(uidoc,doc)

        if Ele:
            t = Transaction (doc, "Tạo sample model để tạo bảng thống kê")
            t.Start()
            # module.message_box("Ok, bây giờ thì chọn 1 đối tượng mẫu")
            # pick = uidoc.Selection.PickObject(ObjectType.Element)
            # module.message_box("Tiếp tục chọn điểm để bắt đầu copy")
            # start_point = pick_point_with_nearest_snap()
            from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                        Separator, Button, CheckBox)
            components = [Label('Nhập khoảng cách'),
                            TextBox('textbox1', Text="6700"),
                        #   CheckBox('checkbox1', 'Check this'), (khong can check box)
                            Separator(),
                            Button('Ok')]
            form = FlexForm('ARC tools', components)
            form.show()
            form.values
            khoang_cach_dau_vao = float(form.values["textbox1"])
            for i in Ele:
                # print dir(i)
                name_ban_dau = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.VOLUME_OF_INTEREST_NAME)
                name_ban_dau_value = name_ban_dau.AsString()
                new_name = name_ban_dau_value + "_3F"
                khoang_cach = (khoang_cach_dau_vao/304.8)
                new_position = XYZ(0, 0, khoang_cach)
                copy_element = Autodesk.Revit.DB.ElementTransformUtils.CopyElement(doc, i.Id, new_position)
                for tung_ele in copy_element:
                    name_new = module.get_builtin_parameter_by_name(doc.GetElement(tung_ele), DB.BuiltInParameter.VOLUME_OF_INTEREST_NAME)
                    name_new.Set(new_name)
                    # lay_element = doc.GetElement(tung_ele)
                    # doi_type = lay_element.ChangeTypeId(i.Id)
            t.Commit()
except:
    import traceback
    print(traceback.format_exc())
    pass


    