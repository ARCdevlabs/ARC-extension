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
from System.Collections.Generic import *

import traceback
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    currentview = doc.ActiveView
    def create_floor(list_curve_loop, type, height_ofset, level_Id):
        try:
            floor = Autodesk.Revit.DB.Floor.Create(doc, list_curve_loop, type, level_Id)
            param = floor.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)
            param.Set(height_ofset)
            return floor
        except:
            from pyrevit.coreutils import applocales
            current_applocale = applocales.get_current_applocale()
            if str(current_applocale) == "日本語 / Japanese (ja)":
                message = "勾配床に断熱床を入力できません。"
            else:
                message = "Không thể vẽ sàn cách nhiệt cho sàn dốc"
            module.message_box(message) 

    Ele = module.get_elements(uidoc,doc, "Select Slabs to create Insulation", noti = False)
    select = uidoc.Selection
    list_line_floor= []

    def all_type_of_floor():
        all_ceiling_floor = DB.FilteredElementCollector(doc).OfClass(DB.FloorType).OfCategory(DB.BuiltInCategory.OST_Floors)
        return all_ceiling_floor
    list_floor = all_type_of_floor()
    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                Separator, Button, CheckBox)
    components = [Label('Select Type Floor Insulation'),
                    ComboBox('combobox1', [Autodesk.Revit.DB.Element.Name.GetValue(x) for x in list_floor]),
                    Separator(),
                    Button('Create Insulation')]
    form = FlexForm('ARC', components)
    form.show()
    # User selects `Opt 1`, types 'Wood' in TextBox, and select Checkbox
    form.values
    selected_floor = form.values["combobox1"]
    for i in list_floor:
        type_name = Autodesk.Revit.DB.Element.Name.GetValue(i)
        if type_name == selected_floor:
            type_Id = i.Id
    t = Transaction (doc, "Create Insulation")
    t.Start()
    for element in Ele:
        try:
            level_id = element.LevelId
            elevation_bottom = module.get_builtin_parameter_by_name(element, DB.BuiltInParameter.STRUCTURAL_ELEVATION_AT_BOTTOM)
            if elevation_bottom:
                offset = elevation_bottom.AsDouble()
                true_offset = offset- (doc.GetElement(level_id).Elevation)
            else:
                true_offset = 0
            ref = DB.HostObjectUtils.GetBottomFaces(element)
            for i in ref:
                boundaryloops = element.GetGeometryObjectFromReference(i).GetEdgesAsCurveLoops()
            new_floor = create_floor(boundaryloops, type_Id ,true_offset, level_id)    
        except:

            pass
    t.Commit()
