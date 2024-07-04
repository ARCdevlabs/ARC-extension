# -*- coding: utf-8 -*-
import string
import importlib
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
    currentview = doc.ActiveView
    def create_floor(list_curve_loop, type, height_ofset, level_Id):
        try:
            floor = Autodesk.Revit.DB.Floor.Create(doc, list_curve_loop, type, level_Id)
            param = floor.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)
            param.Set(height_ofset)
        except:
           module.message_box("Không thể vẽ sàn cách nhiệt cho sàn dốc") 
        return floor

    t = Transaction (doc, "Vẽ sàn cách nhiệt")
    t.Start()
    Ele = module.get_selected_elements(uidoc,doc)
    select = uidoc.Selection
    list_line_floor= []

    def all_type_of_floor():
        all_ceiling_floor = FilteredElementCollector(doc).OfClass(FloorType).OfCategory(BuiltInCategory.OST_Floors)
        return all_ceiling_floor
    list_floor = all_type_of_floor()
    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                Separator, Button, CheckBox)
    components = [Label('Chọn type sàn cách nhiệt:'),
                    ComboBox('combobox1', [Autodesk.Revit.DB.Element.Name.GetValue(x) for x in list_floor]),
                #   CheckBox('checkbox1', 'Check this'), (khong can check box)
                    Separator(),
                    Button('Tạo cách nhiệt')]
    form = FlexForm('ARC tools', components)
    form.show()
    # User selects `Opt 1`, types 'Wood' in TextBox, and select Checkbox
    form.values
    selected_floor = form.values["combobox1"]
    for i in list_floor:
        type_name = Autodesk.Revit.DB.Element.Name.GetValue(i)
        if type_name == selected_floor:
            type_Id = i.Id
    for element in Ele:
        try:
            level_id = element.LevelId
            elevation_bottom = module.get_parameter_value_by_name(element, "Elevation at Bottom", is_UTF8 = False)
            if elevation_bottom:
                offset = float(elevation_bottom)
                true_offset = float(elevation_bottom)/304.8 - (doc.GetElement(level_id).Elevation)
            else:
                true_offset = 0
            ref = HostObjectUtils.GetBottomFaces(element)
            for i in ref:
                boundaryloops = element.GetGeometryObjectFromReference(i).GetEdgesAsCurveLoops()
            new_floor = create_floor(boundaryloops, type_Id ,true_offset, level_id)    
        except:
            pass
    t.Commit()
