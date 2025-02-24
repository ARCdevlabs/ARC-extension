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
from System.Collections.Generic import *
import traceback
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    try:
        Ele = module.get_elements(uidoc,doc, "Select Beams", noti = False)
        def disallow_join_at_end(element, ind):
            Autodesk.Revit.DB.WallUtils.DisallowWallJoinAtEnd(element,ind)

        from rpw.ui.forms import TextInput
        gia_tri_dieu_chinh = TextInput('ARC: Input value to modify offset', default="0")

        
        trans_group = TransactionGroup(doc, "Modify level of beam")
        trans_group.Start()

        t1 = Transaction (doc, "Set_yz Justification")
        t1.Start()
        for tung_ele in Ele:
            set_yz_para = module.get_builtin_parameter_by_name(tung_ele, DB.BuiltInParameter.YZ_JUSTIFICATION).Set(int(1))
        t1.Commit()

        t = Transaction (doc, "Modify level")
        t.Start()
        for i in Ele:
            if i.Category.Name == "Structural Framing" or i.Category.Name == "構造フレーム":
                get_para_start = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.START_Z_OFFSET_VALUE)
                # get_para_value_start = module.get_parameter_value_by_name(i, "Start z Offset Value", is_UTF8 = False)
                get_para_value_start = get_para_start.AsDouble()


                # get_para_value_end = module.get_parameter_value_by_name(i, "End z Offset Value", is_UTF8 = False)
                get_para_end = module.get_builtin_parameter_by_name(i, DB.BuiltInParameter.END_Z_OFFSET_VALUE)
                get_para_value_end = get_para_end.AsDouble()

                # set_para_value_start = module.set_parameter_value_by_name(i, "Start z Offset Value", (float(get_para_value_start) + float(gia_tri_dieu_chinh)/304.8), is_UTF8 = False)
                set_para_value_start = get_para_start.Set(float(get_para_value_start) + float(gia_tri_dieu_chinh)/304.8)

                # set_para_value_end = module.set_parameter_value_by_name(i, "End z Offset Value", (float(get_para_value_end) + float (gia_tri_dieu_chinh))/304.8, is_UTF8 = False)
                set_para_value_end = get_para_end.Set(float(get_para_value_end) + float(gia_tri_dieu_chinh)/304.8)

        t.Commit()
        trans_group.Assimilate()
    except:

        pass