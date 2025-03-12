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
    list_khong_duoc_chuyen = []
    list_duoc_chuyen = []
    Ele = module.get_elements(uidoc,doc, 'Select Beams', noti = False)


    trans_group = TransactionGroup(doc, 'Switch Start End Z Offset to Start End Level Offset')
    trans_group.Start()

    for beam in Ele:
        get_para_start_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)
        get_para_end_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION)
        value_start_level_offset = get_para_start_level_offset.AsDouble()
        value_end_level_offset = get_para_end_level_offset.AsDouble()
        if round(value_start_level_offset,3) != 0 or round(value_end_level_offset,3) != 0:
            list_khong_duoc_chuyen.append((beam.Id).IntegerValue)
        else:
            
            list_duoc_chuyen.append(beam)
    
    with revit.Transaction('DisAllow Join', swallow_errors=True):
        for tung_beam in Ele:
            disallow_join_at_end(tung_beam, 0)
            disallow_join_at_end(tung_beam, 1)

    for beam in list_duoc_chuyen:
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
                get_para_start_Y = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.START_Y_OFFSET_VALUE)
                get_para_end_Y = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.END_Y_OFFSET_VALUE)

                clone_para_start_Y = get_para_start_Y.AsDouble()
                clone_para_end_Y = get_para_end_Y.AsDouble()
        
                get_para_start_level_offset.Set(get_para_start_Z.AsDouble())
                get_para_end_level_offset.Set(get_para_end_Z.AsDouble())

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

    with revit.Transaction('Allow Join', swallow_errors=True):
        for tung_beam in Ele:
            allow_join_at_end(tung_beam, 0)
            allow_join_at_end(tung_beam, 1)

    if len(list_khong_duoc_chuyen) > 0:
        print ("The Start level offset or End level offset should be = 0 to use this tool. Please check this ID: " "\n" + str(list_khong_duoc_chuyen))

    trans_group.Assimilate()