# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from Autodesk.Revit.UI.Selection import ObjectType
from nances import revit
import nances as module
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Ele = module.get_elements(uidoc,doc, 'Select Beams', noti = False)

    trans_group = TransactionGroup(doc, 'Switch Start End Level Offset to Z offset')
    trans_group.Start()
    for beam in Ele:
        clone_para_start_Y = 0
        clone_para_end_Y = 0
        yz_jus = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.YZ_JUSTIFICATION)
        get_para_start_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)
        get_para_end_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION)
        value_yz_jus = yz_jus.AsInteger()
        if value_yz_jus == 1:
            with revit.Transaction('Switch Start End Level Offset to Z offset', swallow_errors=True):
                get_para_start_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.START_Z_OFFSET_VALUE)
                get_para_end_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.END_Z_OFFSET_VALUE)

                get_para_start_Z.Set(get_para_start_level_offset.AsDouble())
                get_para_end_Z.Set(get_para_end_level_offset.AsDouble())
            
            with revit.Transaction('Chỉnh start end level offset về 0', swallow_errors=True):
                get_para_start_level_offset.Set(0)
                get_para_end_level_offset.Set(0)
        if value_yz_jus == 0:
            if get_para_start_level_offset.AsDouble() == get_para_end_level_offset.AsDouble():
                with revit.Transaction('Switch Start End Level Offset to Z offset', swallow_errors=True):
                    get_para_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.Z_OFFSET_VALUE)
                    get_para_Z.Set(get_para_start_level_offset.AsDouble())
            if get_para_start_level_offset.AsDouble() != get_para_end_level_offset.AsDouble():
                with revit.Transaction('Chuyển yz uniform thành yz dependent', swallow_errors=True):
                    yz_jus.Set(1)
                with revit.Transaction('Nhập start end z offset', swallow_errors=True):
                    get_para_start_Z.Set(get_para_start_level_offset.AsDouble())
                    get_para_end_Z.Set(get_para_end_level_offset.AsDouble())
                with revit.Transaction('Chỉnh start end level offset về 0', swallow_errors=True):
                    get_para_start_level_offset.Set(0)
                    get_para_end_level_offset.Set(0)
    trans_group.Assimilate()