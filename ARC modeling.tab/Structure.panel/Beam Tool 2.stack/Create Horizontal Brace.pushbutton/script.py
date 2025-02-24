# -*- coding: utf-8 -*-
import string
import importlib
import Autodesk.Revit
import Autodesk.Revit.DB
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
    try:
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        active_view = module.Active_view(doc)
        view_direction = active_view.ViewDirection
        if view_direction.Z == 1 and str(active_view.ViewType) != "ThreeD":
            def distance_3d(point1, point2):
                import math
                return math.sqrt(
                    (point2.X - point1.X) ** 2 +
                    (point2.Y - point1.Y) ** 2 +
                    (point2.Z - point1.Z) ** 2)

            def find_corners(points):
                n = len(points)
                # Tính tọa độ trung bình
                x_avg = sum([p.X for p in points]) / n
                y_avg = sum([p.Y for p in points]) / n
                z_avg = sum([p.Z for p in points]) / n
            
                avg_point = XYZ(x_avg, y_avg, z_avg)

                # Tính khoảng cách từ trung tâm đến mỗi điểm
                distances = [(point, distance_3d(point, avg_point)) for point in points]
                
                # Sắp xếp các điểm theo khoảng cách giảm dần
                distances.sort(key=lambda x: x[1], reverse=True)
                
                # Lấy 4 điểm xa nhất, tức là 4 điểm góc
                corners = [d[0] for d in distances[:4]]
            
                return corners
            
            def active_symbol(element):
                try:
                    if element.IsActive == False:  
                        element.Activate()
                        # print (element.Activate())
                except:
                    # print(traceback.format_exc())
                    return 
            def create_beam(idoc, curve,beam_type,level, offset):
                active_symbol(beam_type)
                beam = idoc.Create.NewFamilyInstance(curve, beam_type, level, Autodesk.Revit.DB.Structure.StructuralType.Beam)
                param_start_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)
                param_end_offset = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION)
                param_start_offset.Set(offset/304.8)
                param_end_offset.Set(offset/304.8)
                return beam

            def all_type_of_framing():
                all_type_of_framing = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_StructuralFraming)
                return all_type_of_framing

            def get_all_element_of_category_in_view (idoc, view, builtin_category):
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

            list_type_framing = all_type_of_framing()

            from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                        Separator, Button, CheckBox)
            components = [Label('Select type of Brace:'),
                            ComboBox('combobox1', [Autodesk.Revit.DB.Element.Name.GetValue(x) for x in list_type_framing]),
                            Label('Height offset:'),
                            TextBox('textbox1', Text="0"),
                            Separator(),
                            Button('Create Brace')]
            
            form = FlexForm('ARC', components)
            form.show()
            form.values

            try:
                height_offset = float(form.values["textbox1"])
                selected_framing_type = form.values["combobox1"]
            except: 
                sys.exit()

            level_of_view = active_view.GenLevel
            id_level_of_view = level_of_view.Id
            all_area_schemes = FilteredElementCollector(doc).OfClass(AreaScheme).ToElements()
            area_scheme = all_area_schemes[0] #Lấy area scheme đầu tiên

            # Lấy type của Brace.
            for framing_type in list_type_framing:
                type_name = Autodesk.Revit.DB.Element.Name.GetValue(framing_type)
                if str(type_name) == str(selected_framing_type):
                    type_framing = framing_type

            trans_group = TransactionGroup(doc, "Create Horizontal Brace")
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

                            def create_horizontal_brace(idoc, input_area,type_beam,level,height):
                                try:
                                    direction_all_bounding_line = []
                                    all_end_point = []
                                    area_boundaries = input_area.GetBoundarySegments(SpatialElementBoundaryOptions())
                                    curve_loop_list  = List[CurveLoop]()
                                    for area_boundary in area_boundaries:
                                        area_curve_loop = CurveLoop()
                                        for boundary_segment in area_boundary:
                                            curve = boundary_segment.GetCurve()
                                            direction_curve = curve.Direction
                                            direction_all_bounding_line.append(  str (round( abs(direction_curve.X),1)) + str (round( abs(direction_curve.Y),1)) + str (round( abs(direction_curve.Z),1))  )
                                            all_end_point.append(curve.GetEndPoint(0))
                                            area_curve_loop.Append(curve)
                                        curve_loop_list.Add(area_curve_loop)
                                    corners = find_corners(all_end_point)

                                    for i in range(len(corners)):
                                        for j in range(i + 1, len(corners)):
                                            boun_line =  Autodesk.Revit.DB.Line.CreateBound(corners[i],corners[j])
                                            string_of_direction = str (round( abs(boun_line.Direction.X),1)) +str (round( abs(boun_line.Direction.Y),1)) + str (round( abs(boun_line.Direction.Z),1))
                                            # print string_of_direction, direction_all_bounding_line
                                            if string_of_direction not in direction_all_bounding_line:
                                                # detail_line = idoc.Create.NewDetailCurve(active_view,boun_line)                       
                                                new_beam = create_beam(idoc, boun_line, type_beam, level, height)   
                                                                    
                                    return
                                
                                except:
                                    # print(traceback.format_exc())
                                    return None
                                                
                            with revit.Transaction("Tạo area khi pick vào ô dầm", swallow_errors=True):
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


                            if new_area != None:

                                with revit.Transaction("Tạo giằng từ area", swallow_errors=True):
                                    
                                    create_horizontal_brace (doc, new_area,type_framing,level_of_view,height_offset)

                            else:
                                break

                        except:                            
                            # print(traceback.format_exc())
                            break


                # Khởi tạo vòng lặp While cho tới khi dừng         
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
        else:
            module.message_box("Please use the tool in plan view.") 
    except:
        pass