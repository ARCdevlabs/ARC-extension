# -*- coding: utf-8 -*-
__doc__ = 'nguyenthanhson1712@gmail.com'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib
try:
    ARC = string.ascii_lowercase
    begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
    module = importlib.import_module(str(begin))
    import Autodesk
    from Autodesk.Revit.DB import *
    from System.Collections.Generic import *
    if module.AutodeskData():
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        Ele = module.get_selected_elements(uidoc,doc)
        if not Ele:
            import sys
            sys.exit()
        t = Transaction (doc, "Leader Dim/Tag")
        t.Start()
        for i in Ele:
            # category = module.get_builtin_parameter_by_name(i,BuiltInParameter.ELEM_CATEGORY_PARAM_MT)
            # print category.AsValueString()

            if i.Category.Name in "Dimensions, 寸法": 
                try:
                    check = module.get_builtin_parameter_by_name(i,BuiltInParameter.DIM_LEADER)
                    param_dim = i.get_Parameter(BuiltInParameter.DIM_LEADER)
                    if check.AsInteger() == 1:
                        param_dim.Set(0)
                    else:
                        param_dim.Set(1)
                except:
                    pass
            else:
                try:
                    check = module.get_builtin_parameter_by_name(i,BuiltInParameter.LEADER_LINE)
                    param_tag = i.get_Parameter(BuiltInParameter.LEADER_LINE)
                    if check.AsInteger() == 1:
                        param_tag.Set(0)
                    else:
                        param_tag.Set(1)
                        i.LeaderEndCondition = LeaderEndCondition.Free
                except:
                    pass
        t.Commit()        
except:
    pass        
