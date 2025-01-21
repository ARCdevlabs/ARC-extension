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
if module.AutodeskData():
    try:
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        Ele = module.get_elements(uidoc,doc, 'Select Beams', noti = False)

        trans_group = TransactionGroup(doc, 'Switch Start End Z Offset')
        trans_group.Start()
        for beam in Ele:
            # get_para_start_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)
            # get_para_end_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION)
            # value_get_para_start_level_offset = get_para_start_level_offset.AsDouble()
            # value_get_para_end_level_offset = get_para_end_level_offset.AsDouble()
            # if str(value_get_para_end_level_offset) == "0.0":
            #     if str(value_get_para_end_level_offset) == "0.0":
            t = Transaction (doc, "Switch Start End Z")
            yz_jus = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.YZ_JUSTIFICATION)
            get_para_start_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.START_Z_OFFSET_VALUE)
            get_para_end_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.END_Z_OFFSET_VALUE)
            get_para_Z = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.Z_OFFSET_VALUE)
            get_para_start_Y = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.START_Y_OFFSET_VALUE)
            get_para_end_Y = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.END_Y_OFFSET_VALUE)
            get_para_Y = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.Y_OFFSET_VALUE)

            get_para_start_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)
            get_para_end_level_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION)
            value_yz_jus = yz_jus.AsInteger()
            t.Start()
            if value_yz_jus == 1:
                get_para_start_level_offset.Set(get_para_start_Z.AsDouble())
                get_para_end_level_offset.Set(get_para_end_Z.AsDouble())
            else:
                get_para_start_level_offset.Set(get_para_Z.AsDouble())
                get_para_end_level_offset.Set(get_para_Z.AsDouble())
            t.Commit()
    
            clone_para_start_Y = get_para_start_Y.AsDouble()
            clone_para_end_Y = get_para_end_Y.AsDouble()

            t2 = Transaction (doc, "Setting")
            t2.Start()
            if value_yz_jus == 1:
                get_para_start_Z.Set(0)
                get_para_end_Z.Set(0)
                if get_para_end_Y.AsDouble() == get_para_start_Y.AsDouble():                                    
                    get_para_start_Y.Set(0)
                    get_para_end_Y.Set(0)
            else:
                get_para_Z.Set(0)                             
            t2.Commit()

            t3 = Transaction (doc, "Setting2")
            t3.Start()
            if value_yz_jus == 1:
                if get_para_end_Y.AsDouble() == get_para_start_Y.AsDouble():  
                    yz_jus.Set(0)                                                       
            t3.Commit()
            
            t4 = Transaction (doc, "Setting3")
            t4.Start()
            if yz_jus.AsInteger() == 0:
                get_para_Y.Set(clone_para_start_Y)                                                       
            t4.Commit()
        trans_group.Assimilate()
    except:
        pass