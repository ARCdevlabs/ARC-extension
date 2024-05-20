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
        import Autodesk
        from Autodesk.Revit.DB import *
        from Autodesk.Revit.UI.Selection.Selection import PickObject
        from Autodesk.Revit.UI.Selection  import ObjectType
        from Autodesk.Revit.DB import Element
        from System.Collections.Generic import *
        #Get UIDocument
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        acview= module.Active_view(doc)
        t = Transaction(doc, "Turn on link cad in View Temporary")
        t.Start()
        print "Đây là test"
        Checkviewtemplate = str(acview.ViewTemplateId)
        #Check view have ViewTemplate or not, if not => don't need to Enable Temporary view
        if Checkviewtemplate != "-1":
            tem = acview.EnableTemporaryViewPropertiesMode(acview.Id)
        listcate = doc.Settings.Categories
        for i in listcate: 
            if i.Name == "Sections":
                if acview.GetCategoryHidden(i.Id):
                    hide = acview.SetCategoryHidden(i.Id,False)
                else: 
                    hide = acview.SetCategoryHidden(i.Id,True)
                break
            else:
                continue
        t.Commit()  
except:
    pass        
