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
import sys
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

    def get_list_curve_from_floor(idoc,floor):
        curve_loop_list   = List[CurveLoop]()
        curve_loop = CurveLoop()
        sketch_id = floor.SketchId
        sketch = idoc.GetElement(sketch_id)
        # all_sketch = sketch.GetAllElements()
        profile = sketch.Profile
        list_curve_loop_array = profile
        for curve_loop_array in list_curve_loop_array:
            for edge in curve_loop_array:
                try:
                    curve_loop.Append(edge)
                except:
                    pass
        curve_loop_list.Add(curve_loop)
        return curve_loop_list
    
    def create_wall_from_floor(doc, list_curve_loop, wall_type, level, base_offset, height_offset):
        for curve_loop in list_curve_loop:
            for moi_curve in curve_loop:
                curve = moi_curve
                para_width = wall_type.get_Parameter(Autodesk.Revit.DB.BuiltInParameter.WALL_ATTR_WIDTH_PARAM).AsDouble()
                offset_curve = curve.CreateOffset(float(para_width)/(2), Autodesk.Revit.DB.XYZ.BasisZ)
                wall = Wall.Create(doc, offset_curve, level.Id, False)

                para_base_constraint = wall.get_Parameter(Autodesk.Revit.DB.BuiltInParameter.WALL_BASE_CONSTRAINT)
                para_base_constraint.Set(level.Id)                   
                para_base_offset = wall.get_Parameter(Autodesk.Revit.DB.BuiltInParameter.WALL_BASE_OFFSET)
                para_base_offset.Set(base_offset)

                para_top_constraint = wall.get_Parameter(Autodesk.Revit.DB.BuiltInParameter.WALL_HEIGHT_TYPE)
                para_top_constraint.Set(level.Id)                   
                para_top_offset = wall.get_Parameter(Autodesk.Revit.DB.BuiltInParameter.WALL_TOP_OFFSET)
                para_top_offset.Set(height_offset)

                wall.WallType = wall_type                    
        return wall   
    
    def all_wall_type ()  :   
        wall_type = FilteredElementCollector(doc).OfClass(WallType).ToElements()
        return wall_type    

    Ele = module.get_elements(uidoc,doc, "Select Slabs to create Insulation", noti = False)
    floor = []
    for i in Ele:
        if str(i.Category.Name) in "Floors , 床":
            floor.append(i)
    if len(floor) == 0:
        module.message_box("Please select the slab to create Insulation")
        sys.exit()
    def all_type_of_floor():
        all_ceiling_floor = DB.FilteredElementCollector(doc).OfClass(DB.FloorType).OfCategory(DB.BuiltInCategory.OST_Floors)
        return all_ceiling_floor
    list_floor = all_type_of_floor()

    list_wall_type = all_wall_type()

    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                Separator, Button, CheckBox)
    components = [
                    Label('Select Type Floor Insulation:'),
                    ComboBox('combobox1', [Autodesk.Revit.DB.Element.Name.GetValue(x) for x in list_floor]),
                    Separator(),
                    CheckBox('checkbox1', 'Include Wall?'),
                    Label('Select Type Wall Insulation:'),
                    ComboBox('combobox2', [Autodesk.Revit.DB.Element.Name.GetValue(x) for x in list_wall_type]),
                    Label('Height of Wall:'),
                    TextBox('textbox1', Text="450"),
                    Separator(),
                    Button('Create Insulation')
                ]
    form = FlexForm('ARC', components)
    form.show()
    form.values
    try:
        selected_floor = form.values["combobox1"]
        selected_type_wall = form.values["combobox2"]
        height_wall = form.values["textbox1"]
        create_wall = form.values["checkbox1"]
    except:
        sys.exit()
    for i in list_wall_type:
        type_name = Autodesk.Revit.DB.Element.Name.GetValue(i)
        if type_name == selected_type_wall:
            type_wall = i
    for i in list_floor:
        type_name = Autodesk.Revit.DB.Element.Name.GetValue(i)
        if type_name == selected_floor:
            type_Id = i.Id
    trans_group = TransactionGroup(doc, 'Create Insulation')
    trans_group.Start()

    for element in floor:
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
            t_0 = Transaction (doc, "Create Insulation_floor")
            t_0.Start()
            new_floor = create_floor(boundaryloops, type_Id ,true_offset, level_id)    
            t_0.Commit()
        except:
            pass
        if create_wall:
            list_curve_loop_of_floor = get_list_curve_from_floor(doc,new_floor)
            cao_tuong = float(height_wall)
            new_floor_elevation_bottom = module.get_builtin_parameter_by_name(new_floor, DB.BuiltInParameter.STRUCTURAL_ELEVATION_AT_BOTTOM)
            if new_floor_elevation_bottom:
                offset = new_floor_elevation_bottom.AsDouble()
                true_offset = offset- (doc.GetElement(level_id).Elevation)
            else:
                true_offset = 0
            t_1 = Transaction (doc, "Create Insulation_wall")
            t_1.Start()
            create_wall_from_floor(doc, list_curve_loop_of_floor, type_wall, doc.GetElement(level_id), true_offset - (cao_tuong/304.8), true_offset)
            t_1.Commit()

    trans_group.Assimilate()
