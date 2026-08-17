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
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Ele = module.get_elements(uidoc,doc, "Select Dimension or Tag", noti = False)
    if Ele:
        t = Transaction (doc, "Leader Dim/Tag")
        t.Start()
        for i in Ele:
            try:
                if i.Category.Name in "Dimensions, 寸法": 
                    try:
                        check = module.get_builtin_parameter_by_name(i,BuiltInParameter.DIM_LEADER)
                        if check.AsInteger() == 1:
                            check.Set(0)
                        else:
                            check.Set(1)
                    except:

                        pass
                else:
                    try:
                        check_para_leader = module.get_builtin_parameter_by_name(i,BuiltInParameter.LEADER_LINE)
                        param_tag = i.get_Parameter(BuiltInParameter.LEADER_LINE)
                        if check_para_leader.AsInteger() == 1:
                            param_tag.Set(0)
                        else:
                            param_tag.Set(1)
                            i.LeaderEndCondition = LeaderEndCondition.Free
                    except:
                        pass
            except:
                pass
        t.Commit()        
    
