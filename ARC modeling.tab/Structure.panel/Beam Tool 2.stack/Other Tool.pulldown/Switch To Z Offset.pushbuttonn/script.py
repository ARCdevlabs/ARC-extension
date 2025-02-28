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
from Autodesk.Revit.UI.Selection import ObjectType
from nances import revit
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Ele = module.get_elements(uidoc,doc, 'Select Beams', noti = False)

    # trans_group = TransactionGroup(doc, 'Switch Start End Z Offset to Start End Level Offset')
    # trans_group.Start()
    for beam in Ele:
        clone_para_start_Y = 0
        clone_para_end_Y = 0
        yz_jus = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.YZ_JUSTIFICATION)
        get_para_start_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)
        get_para_end_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION)
        value_yz_jus = yz_jus.AsInteger()

        if value_yz_jus == 1:
            with revit.Transaction('Switch Z offset to Start End Level Offset', swallow_errors=True):
                get_para_start_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.START_Z_OFFSET_VALUE)
                get_para_end_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.END_Z_OFFSET_VALUE)

                get_para_start_Z.Set(get_para_start_level_offset.AsDouble())
                get_para_end_Z.Set(get_para_end_level_offset.AsDouble())

        if value_yz_jus == 0:
            with revit.Transaction('Switch Z offset to Start End Level Offset', swallow_errors=True):
                get_para_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.Z_OFFSET_VALUE)
                get_para_Y = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.Y_OFFSET_VALUE)
                clone_para_Y = get_para_Y.AsDouble()

                get_para_start_level_offset.Set(get_para_Z.AsDouble())
                get_para_end_level_offset.Set(get_para_Z.AsDouble())

        if value_yz_jus == 1:
            t2 = Transaction (doc, "Chuyển start end y offset thành 0")
            t2.Start()
            get_para_start_Z.Set(0)
            get_para_end_Z.Set(0)
            if get_para_end_Y.AsDouble() == get_para_start_Y.AsDouble():                                  
                get_para_start_Y.Set(0)
                get_para_end_Y.Set(0)
            t2.Commit()
        if value_yz_jus == 0:
            t2 = Transaction (doc, "Chuyển start end y offset thành 0")
            t2.Start()
            get_para_Z.Set(0)    
            t2.Commit()                         

        if value_yz_jus == 1:
            t3 = Transaction (doc, "Chuyển yz dependent thành uniform")
            t3.Start()
            if get_para_end_Y.AsDouble() == get_para_start_Y.AsDouble():  
                yz_jus.Set(0)                                                       
            t3.Commit()
        else:
            pass
        yz_jus = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.YZ_JUSTIFICATION)
        if yz_jus.AsInteger() == 0:
            t4 = Transaction (doc, "Nhập giá trị y")
            t4.Start()
            get_para_Y = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.Y_OFFSET_VALUE)
            try:
                get_para_Y.Set(clone_para_start_Y)   
            except:
                get_para_Y.Set(clone_para_Y)                                                    
            t4.Commit()
    # trans_group.Assimilate()