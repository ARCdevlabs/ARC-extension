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
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        AcView= module.Active_view(doc)
        t = Transaction(doc, "Color Cad Vn03 Red")
        t.Start()
        Ele = module.get_selected_elements(uidoc, doc)
        #Check view have ViewTemplate or not, if not => don't need to Enable Temporary view
        #Select Color
        ColorCad = Autodesk.Revit.DB.Color(255,000,0)
        #Get FillPattern by name
        GetFillPattern = Autodesk.Revit.DB.FillPatternElement.GetFillPatternElementByName(doc,FillPatternTarget.Drafting,"<Solid fill>")
        #Def OverrideFraming (Color)
        """ Cad """
        for i in Ele:
            OverrideCad = Autodesk.Revit.DB.OverrideGraphicSettings()
            OverrideCad.SetProjectionLineColor(ColorCad)
            SetColorCad = AcView.SetElementOverrides(i.Id,OverrideCad)
        t.Commit()
except:
    pass        