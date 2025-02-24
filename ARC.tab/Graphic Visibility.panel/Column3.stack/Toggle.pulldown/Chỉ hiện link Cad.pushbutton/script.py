__doc__ = 'python for revit api'
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
        from Autodesk.Revit.UI.Selection.Selection import PickObject
        from Autodesk.Revit.UI.Selection  import ObjectType
        from Autodesk.Revit.DB import*
        import Autodesk
        from Autodesk.Revit.DB import *
        from System.Collections.Generic import *
        import math
        from rpw.ui.forms import Alert
        #Get UIDocument
        uidoc = __revit__.ActiveUIDocument
        #Get Document 
        doc = uidoc.Document
        sketchloop = []
        acview= module.Active_view(doc)
        t = Transaction (doc, "Select section box")
        t.Start()
        filter = Autodesk.Revit.DB.ElementClassFilter(ImportInstance)
        get_dependent_element = acview.GetDependentElements(filter)
        if len(get_dependent_element) > 0:
            acview.IsolateElementsTemporary(get_dependent_element)
        else:
            Alert("Don't have link cad in this view",title="Warning",header= "Something wrong")
        t.Commit()
except:
    pass     
