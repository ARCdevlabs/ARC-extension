import nances as module
if module.AutodeskData():
    import Autodesk
    from Autodesk.Revit.DB import Transaction,Level, BuiltInCategory, FilteredElementCollector, WallType, FamilySymbol, ElementId
    from Autodesk.Revit.UI.Selection import ObjectType
    import clr
    import sys
    clr.AddReference("System.Windows.Forms")
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document

    import_instance = module.get_element(uidoc,doc, 'Select Import Instance', noti = False)
    try:
        from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                    Separator, Button, CheckBox)
        components = [Label('Input name of layer'),
                        TextBox('textbox1', Text=""),
                        Separator(),
                        Button('Create Detail Line')]
        form = FlexForm('ARC', components)
        form.show()
        form.values

        layer_name = str(form.values["textbox1"])

        t = Transaction (doc, "Detail Line from DWG")
        t.Start()

        acview= module.Active_view(doc)
        dwg = import_instance[0]
        # Nhap layer cua line trong dwg
        # Khai bao option cua "get_Geometry"
        geo_opt = Autodesk.Revit.DB.Options()
        geo_opt.ComputeReferences = True
        geo_opt.IncludeNonVisibleObjects = True
        geo_opt.View = acview
        list_curve=[]
        # get_Geometry cua tat ca line trong file dwg
        geometry = dwg.get_Geometry(geo_opt)
        for geo_inst in geometry:
            geo_elem = geo_inst.GetInstanceGeometry()
            for polyline in geo_elem:
                element = doc.GetElement(polyline.GraphicsStyleId)
                if not element:
                    continue
                try:
                    # Kiem tra layer cua line trong file dwg thong qua "GraphicsStyleCategory.Name"
                    # Dung de ve cac doi tuong "polyline"
                    is_target_layer = element.GraphicsStyleCategory.Name == layer_name
                    is_polyline = polyline.GetType().Name == "PolyLine"
                    if is_polyline and is_target_layer:
                        begin = None
                        for pts in polyline.GetCoordinates():
                            if not begin:
                                begin = pts
                                continue
                            end = pts
                            line = Autodesk.Revit.DB.Line.CreateBound(begin, end)
                            list_curve.append(line)
                            det_line = doc.Create.NewDetailCurve(acview, line)
                            begin = pts

                    # Dung de ve cac doi tuong "line"
                    is_line = polyline.GetType().Name == "Line"
                    if is_line and is_target_layer:
                            straight_line = polyline
                            list_curve.append(straight_line)
                            det_line = doc.Create.NewDetailCurve(acview, straight_line)
                    # Dung de ve cac doi tuong "arc"
                    is_arc = polyline.GetType().Name == "Arc"
                    if is_arc and is_target_layer:
                        arc = polyline
                        list_curve.append(arc)
                        det_line = doc.Create.NewDetailCurve(acview, arc) #Neu khong ve detail line thi thoi khong dung
                except:
                    pass
        t.Commit()
    except:
        pass