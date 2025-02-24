
import string
import importlib
from webbrowser import get
#Get UIDocument

ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    collector = FilteredElementCollector(doc)
    get_all_view = collector.OfClass(View).ToElements()


    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                Separator, Button, CheckBox)
    components = [Label('Enter the name of sample view:'),
                    TextBox('textbox1', Text=""),
                #   CheckBox('checkbox1', 'Check this'), (khong can check box)
                    Separator(),
                    Button('Ok')]
    form = FlexForm('ARC tools', components)
    form.show()
    # User selects `Opt 1`, types 'Wood' in TextBox, and select Checkbox
    form.values
    selected_view = form.values["textbox1"]

    for view in get_all_view:
        if type(view) != "ViewSheet":
            if selected_view == str(view.Name):
                other_view = view
    currentview = doc.ActiveView
    currentview_level = currentview.GenLevel.ProjectElevation
    # other_view = doc.GetElement(ElementId(7046534))
    other_view_level = other_view.GenLevel.ProjectElevation
    difference = float(currentview_level) - float(other_view_level)
    t = Transaction (doc, "Get Floor's Boundary")
    t.Start()
    sketchloop = []
    detailline= []
    Ele = module.get_selected_elements(uidoc,doc)
    DatumExtentType = Autodesk.Revit.DB.DatumExtentType.ViewSpecific
    for i in Ele:
        try:
            # curve_in_current_view = i.GetCurvesInView(DatumExtentType,currentview)
            list_curve = i.GetCurvesInView(DatumExtentType,other_view)
            curve = list_curve[0]
            #need to change to line in plan view because some floor is not on a plane.
            Startpoint = curve.GetEndPoint(0)
            Endpoint = curve.GetEndPoint(1)
            PlaPoint1 = XYZ(Startpoint.X, Startpoint.Y, Startpoint.Z+ difference)
            PlaPoint2 = XYZ(Endpoint.X, Endpoint.Y, Endpoint.Z + difference)
            L1 = Line.CreateBound(PlaPoint1,PlaPoint2)
            set_curve_in_view = i.SetCurveInView(DatumExtentType, currentview, L1)
        except:
            pass
    t.Commit()
    