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
        from Autodesk.Revit.DB import *
        from System.Collections.Generic import *
        #Get UIDocument
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        acview= module.Active_view(doc)
        t = Transaction(doc, "Turn on link cad in View Temporary")
        t.Start()
        #Check view have ViewTemplate or not, if not => don't need to Enable Temporary view
        Checkviewtemplate = str(acview.ViewTemplateId)
        if Checkviewtemplate != "-1":
            tem = acview.EnableTemporaryViewPropertiesMode(acview.Id)
        check = acview.AreImportCategoriesHidden
        if check == True:
            acview.AreImportCategoriesHidden = False
        else:
            acview.AreImportCategoriesHidden = True
        t.Commit()  
except:
    pass      