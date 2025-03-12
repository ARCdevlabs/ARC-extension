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
    def disallow_join_at_end(element, ind):
        Autodesk.Revit.DB.Structure.StructuralFramingUtils.DisallowJoinAtEnd(element,ind)
        return
    
    def allow_join_at_end(element, ind):
        Autodesk.Revit.DB.Structure.StructuralFramingUtils.AllowJoinAtEnd(element,ind)
        return
    Ele = module.get_elements(uidoc,doc, 'Select Beams', noti = False)
    list_khong_duoc_chuyen = []
    list_duoc_chuyen = []

    for beam in Ele:
        get_para_start_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)
        get_para_end_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION)
        value_para_start_Z = 0
        value_para_end_Z = 0
        value_para_Z = 0
        try:
            get_para_start_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.START_Z_OFFSET_VALUE)
            value_para_start_Z = get_para_start_Z.AsDouble()
        except:
            pass
        try:
            get_para_end_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.END_Z_OFFSET_VALUE)
            value_para_end_Z = get_para_end_Z.AsDouble() 
        except:
            pass
        try:
            get_para_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.Z_OFFSET_VALUE)
            value_para_Z = get_para_Z.Asdouble()
        except:
            pass

        if value_para_start_Z != 0 or value_para_end_Z != 0 or value_para_Z != 0:
            list_khong_duoc_chuyen.append((beam.Id).IntegerValue)
        else:
            list_duoc_chuyen.append(beam)

    trans_group = TransactionGroup(doc, 'Switch Start End Level Offset to Z offset')
    trans_group.Start()
    

    with revit.Transaction('DisAllow Join', swallow_errors=True):
        for beam in Ele: #List này là Ele bởi vì để tránh trường hợp dầm bị nhảy khi chạy tool
            disallow_join_at_end(beam, 0)
            disallow_join_at_end(beam, 1)

    for beam in list_duoc_chuyen:
        yz_jus = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.YZ_JUSTIFICATION)
        get_para_start_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)
        get_para_end_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION)
        value_yz_jus = yz_jus.AsInteger()
        if value_yz_jus == 1:
            with revit.Transaction('Switch Start End Level Offset to Z offset', swallow_errors=True):
                get_para_start_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.START_Z_OFFSET_VALUE)
                get_para_end_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.END_Z_OFFSET_VALUE)
                if get_para_start_Z.AsDouble() != 0 or get_para_end_Z.AsDouble() != 0:
                    # list_khong_duoc_chuyen.append((beam.Id).IntegerValue)
                    pass
                else:
                    get_para_start_Z.Set(get_para_start_level_offset.AsDouble())
                    get_para_end_Z.Set(get_para_end_level_offset.AsDouble())
            
                # with revit.Transaction('Chỉnh start end level offset về 0', swallow_errors=True):
                #     get_para_start_level_offset.Set(0)
                #     get_para_end_level_offset.Set(0)
        if value_yz_jus == 0:
            get_para_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.Z_OFFSET_VALUE)
            if get_para_Z.AsDouble() != 0:
                # list_khong_duoc_chuyen.append((beam.Id).IntegerValue)
                pass
            else:
                if get_para_start_level_offset.AsDouble() == get_para_end_level_offset.AsDouble():
                    with revit.Transaction('Switch Start End Level Offset to Z offset', swallow_errors=True):
                        # get_para_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.Z_OFFSET_VALUE)
                        get_para_Z.Set(get_para_start_level_offset.AsDouble())
                if get_para_start_level_offset.AsDouble() != get_para_end_level_offset.AsDouble():
                    with revit.Transaction('Chuyển yz uniform thành yz dependent', swallow_errors=True):
                        yz_jus.Set(1)
                    with revit.Transaction('Nhập start end z offset', swallow_errors=True):
                        get_para_start_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.START_Z_OFFSET_VALUE)
                        get_para_end_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.END_Z_OFFSET_VALUE)
                        get_para_start_Z.Set(get_para_start_level_offset.AsDouble())
                        get_para_end_Z.Set(get_para_end_level_offset.AsDouble())
                    # with revit.Transaction('Chỉnh start end level offset về 0', swallow_errors=True):
                    #     get_para_start_level_offset.Set(0)
                    #     get_para_end_level_offset.Set(0)
    with revit.Transaction('Chỉnh start end level offset về 0', swallow_errors=True):
        for tung_beam in list_duoc_chuyen:
            get_para_start_level_offset = module.get_builtin_parameter_by_name(tung_beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)
            get_para_end_level_offset = module.get_builtin_parameter_by_name(tung_beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION)
            get_para_start_level_offset.Set(0)
            get_para_end_level_offset.Set(0)
    with revit.Transaction('Allow Join', swallow_errors=True):
        for beam in Ele: #List này là Ele bởi vì để tránh trường hợp dầm bị nhảy khi chạy tool
            allow_join_at_end(beam, 0)
            allow_join_at_end(beam, 1)

    if len(list_khong_duoc_chuyen) > 0:
        print ("The Z offset value should be = 0 to use this tool. Please check this ID: " "\n" + str(list_khong_duoc_chuyen))

    trans_group.Assimilate()