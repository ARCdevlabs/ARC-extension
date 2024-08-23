
# -*- coding: utf-8 -*-
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
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
    active_view = module.Active_view(doc)

    def all_type_of_floor():
        all_type_of_floor = FilteredElementCollector(doc).OfClass(FloorType).OfCategory(BuiltInCategory.OST_Floors)
        return all_type_of_floor


    def get_all_element_of_category_in_view (idoc, view, builtin_category):
        # Đây là sample của OST_category
        # category_filter = ElementCategoryFilter(BuiltInCategory.OST_StructuralFraming)

        category_filter = DB.ElementCategoryFilter(builtin_category)
        beam_collector = DB.FilteredElementCollector(idoc, view.Id).WherePasses(category_filter)
        return beam_collector

    def create_new_area_plan (idoc, area_scheme_id, level_id):
        new_area_plan = Autodesk.Revit.DB.ViewPlan.CreateAreaPlan(idoc, area_scheme_id, level_id)
        return new_area_plan

    def create_new_area_boundary( idoc, sketchPlane, geometryCurve, areaView):
        new_area_boundary = idoc.NewAreaBoundaryLine(sketchPlane,geometryCurve, areaView)
        return new_area_boundary

    def create_area (idoc, area_view, uv_point):
        area = idoc.Create.NewArea(area_view, uv_point)
        return area

    list_floor = all_type_of_floor()
    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                Separator, Button, CheckBox)
    components = [Label('Select type of floor:'),
                    ComboBox('combobox1', [Autodesk.Revit.DB.Element.Name.GetValue(x) for x in list_floor]),
                    Label('Height offset:'),
                    TextBox('textbox1', Text="0"),
                    Separator(),
                    Button('Create Slab')]
    form = FlexForm('ARC', components)
    form.show()
    form.values
    try:
        selected_floor_type = form.values["combobox1"]
        height_offset = form.values["textbox1"]
    except: 
        # print(traceback.format_exc())
        sys.exit()
    level_of_view = active_view.GenLevel

    id_level_of_view = level_of_view.Id

    all_area_schemes = FilteredElementCollector(doc).OfClass(AreaScheme).ToElements()

    area_scheme = all_area_schemes[0] #Lấy area scheme đầu tiên

    trans_group = TransactionGroup(doc, "Create slab")
    trans_group.Start()

    from pyrevit import revit

    with revit.Transaction("Tạo area plan và đặt area separation", swallow_errors=True):

        area_plan = create_new_area_plan(doc,area_scheme.Id,id_level_of_view)   
        
        level_plane = level_of_view.GetPlaneReference()

        sketch_plane = SketchPlane.Create(doc, level_plane)

        curve_array = Autodesk.Revit.DB.CurveArray()

        list_area_separation = []
        list_area = []

        all_beam_in_view = get_all_element_of_category_in_view (doc, active_view, BuiltInCategory.OST_StructuralFraming)

        for i in all_beam_in_view:
            try:

                beam_id = i.Id

                curve = i.Location.Curve

                start_point = curve.GetEndPoint(0)

                end_point = curve.GetEndPoint(1)

                line = Autodesk.Revit.DB.Line.CreateBound(XYZ(start_point.X,start_point.Y,0),XYZ(end_point.X,end_point.Y,0))

                curve_array.Append(line)

            except:
                # print(traceback.format_exc())
                pass

        for cur in curve_array:
            area_separation = doc.Create.NewAreaBoundaryLine(sketch_plane, cur, area_plan)
            list_area_separation.append(area_separation)

    try:
        def main():
            # Bat dau vong lap lua chon
            while True:
                try:

                    def create_slab(area, floor_type, offset, level_Id):
                        try:

                            area_boundaries = area.GetBoundarySegments(SpatialElementBoundaryOptions())

                            curve_loop_list  = List[CurveLoop]()

                            for area_boundary in area_boundaries:
                                area_curve_loop = CurveLoop()
                                for boundary_segment in area_boundary:
                                    curve = boundary_segment.GetCurve()
                                    area_curve_loop.Append(curve)
                                curve_loop_list.Add(area_curve_loop)

                            if curve_loop_list:

                                slab = Autodesk.Revit.DB.Floor.Create(doc, curve_loop_list, floor_type, level_Id)

                                param = slab.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)

                                param_struc = slab.get_Parameter(BuiltInParameter.FLOOR_PARAM_IS_STRUCTURAL)

                                param_struc.Set(1)

                                param.Set(offset)

                            return slab
                        except:
                            return None
                                        
                    with revit.Transaction("tạo area khi pick vào ô dầm", swallow_errors=True):
                        try:

                            return_point = module.pick_point_with_nearest_snap(uidoc)

                        except:
                            
                            return_point = False

                        if return_point != False:
                            
                            UV_point = UV(return_point.X,return_point.Y)

                            new_area = create_area(doc,area_plan, UV_point)
                            list_area.append(new_area)

                        else:

                            new_area = None


                    list_type_floors = module.all_type_of_class_and_OST(doc, FloorType, BuiltInCategory.OST_Floors)
                    for floor in list_type_floors:
                        type_name = Autodesk.Revit.DB.Element.Name.GetValue(floor)
                        if str(type_name) == str(selected_floor_type):
                            type_floor = floor
                    type_floor_id = type_floor.Id
       
                    if new_area != None:
                        try:
                            height_offset_float = float(height_offset)/304.8
                        except:
                            height_offset_float = 0
                        with revit.Transaction("Tạo sàn từ area", swallow_errors=True):

                            create_slab (new_area, type_floor_id, height_offset_float, id_level_of_view)

                    else:
                        break

                except Exception as ex:
                    # print(traceback.format_exc())
                    if "Operation canceled by user." in str(ex):
                        break
                    else:
                        break
        main()

    except:
        # print(traceback.format_exc())
        pass
    try:
        t6 = Transaction (doc, "Xóa Area Plan")
        t6.Start()
        doc.Delete(area_plan.Id)
        for tung_area in list_area:
            try:
                doc.Delete(tung_area.Id)
            except:
                pass
        for tung_area_sp in list_area_separation:
            try:
                doc.Delete(tung_area_sp.Id)
            except:
                pass
        t6.Commit()
    except:
        pass
    trans_group.Assimilate()