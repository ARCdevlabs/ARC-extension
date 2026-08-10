# -*- coding: utf-8 -*-
import Autodesk
import nances
import traceback
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
import Autodesk.Revit.UI as UI
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
import sys
if nances.AutodeskData():
    try:
        def set_work_plane_for_view(view):
            current_work_plane = view.SketchPlane
            if current_work_plane is None:
                try:
                    if view.ViewType in [ViewType.FloorPlan, ViewType.EngineeringPlan, ViewType.CeilingPlan]:
                        plane = Plane.CreateByNormalAndOrigin(XYZ.BasisZ, XYZ.Zero)
                    elif view.ViewType == ViewType.Section:
                        plane = Plane.CreateByNormalAndOrigin(view.ViewDirection, view.Origin)
                    sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(view.Document, plane)
                    view.SketchPlane = sketch_plane
                except:
                    return False
            return True

                                 
        def create_dim(view, line, ref):
            dim = doc.Create.NewDimension(view, line, ref)
            return dim

        def move_point_along_vector(point, vector, distance):
            new_point = point + vector.Normalize() * distance
            return new_point

        def pick_point_with_nearest_snap():    
            snap_settings = UI.Selection.ObjectSnapTypes.Nearest
            prompt = "Bấm vào vị trí mà cần bố trí dim"
            click_point = None
            try:
                from nances import forms
                with forms.WarningBar(title='Click 1 điểm bất kì để bố trí dim'):
                    click_point = uidoc.Selection.PickPoint(snap_settings, prompt) 
            except:
                # print(traceback.format_exc())
                pass
            return click_point

        def are_vector_parallel(vector_1, vector_2):
            tolerance=0.0001
            cross_product = vector_1.CrossProduct(vector_2)
            return cross_product.GetLength() < tolerance


        from Autodesk.Revit.DB import BuiltInCategory

        class LineAndGridSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):

            def AllowElement(self, element):
                if element.Category is None:
                    return False

                return element.Category.Id.IntegerValue in (
                    int(BuiltInCategory.OST_Lines),
                    int(BuiltInCategory.OST_Grids)
                )

            def AllowReference(self, reference, point):
                return False

        from Autodesk.Revit.DB import DetailLine, Grid

        class DetailLineAndGridSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):

            def AllowElement(self, element):
                return isinstance(element, DetailLine) or isinstance(element, Grid)

            def AllowReference(self, reference, point):
                return False


        def get_all_elements_by_category_in_model(idoc,ost_builtin_category):
            collector = FilteredElementCollector(idoc).OfCategory(ost_builtin_category).WhereElementIsNotElementType()
            return list(collector)


        def get_all_elements_by_category_in_view(idoc, view, ost_builtin_category):
            from Autodesk.Revit.DB import FilteredElementCollector
            collector = (FilteredElementCollector(idoc, view.Id).OfCategory(ost_builtin_category).WhereElementIsNotElementType())
            return list(collector)
                

        def pick_lines_and_grid_by_rectangle():
            from nances import forms
            with forms.WarningBar(title='Quét chuột để chọn các line cần dim'):
                selection = uidoc.Selection
                selected_elements = selection.PickElementsByRectangle(DetailLineAndGridSelectionFilter(), "Chọn các line")
            return selected_elements
                
        def get_direction_of_beam(beam):
            location_curve = beam.Location.Curve
            start_point = location_curve.GetEndPoint(0)
            end_point = location_curve.GetEndPoint(1)
            vector_beam = XYZ(end_point.X - start_point.X,end_point.Y - start_point.Y,0)    
            return vector_beam

        def get_location_curve_of_line_and_grid(element):
            if element.Category.Name in "Lines, 線分":
                location_curve = element.Location.Curve
                start_point = location_curve.GetEndPoint(0)
                end_point = location_curve.GetEndPoint(1)
                start_point_Z0 = XYZ(start_point.X, start_point.Y,0)
                end_point_Z0 = XYZ(end_point.X, end_point.Y,0)
                line = DB.Line.CreateBound(start_point_Z0,end_point_Z0)
            else:
                curve = element.Curve
                start_point = curve.GetEndPoint(0)
                end_point = curve.GetEndPoint(1)
                start_point_Z0 = XYZ(start_point.X, start_point.Y,0)
                end_point_Z0 = XYZ(end_point.X, end_point.Y,0)
                line = DB.Line.CreateBound(start_point_Z0,end_point_Z0)
            return line

        import math
        from Autodesk.Revit.DB import XYZ

        TOL = 0.1 / 304.8      # 0.1 mm -> feet
        ANGLE_TOL = 1e-6

        def is_same_line(line1, line2):

            dir1 = line1.Direction.Normalize()
            dir2 = line2.Direction.Normalize()

            # kiểm tra cùng phương
            angle = dir1.AngleTo(dir2)

            if angle > ANGLE_TOL and abs(angle - math.pi) > ANGLE_TOL:
                return False

            # lấy 1 điểm của line1
            p1 = line1.GetEndPoint(0)

            # lấy 1 điểm của line2
            p2 = line2.GetEndPoint(0)

            # vector nối 2 điểm
            v = p2 - p1

            # khoảng cách vuông góc
            distance = v.CrossProduct(dir1).GetLength()

            return distance < TOL

        def remove_duplicate_lines(doi_tuong_line, lines):
            #Danh sách đưa vào cần phải sorted trước cho tất cả grid đứng đầu danh sách, rồi mới line sẽ nằm sau. Khi đó, sẽ ưu tiên lấy các grid trước và loại bỏ các line trùng với grid

            ket_qua_line_tinh_toan = []

            ket_qua_line_revit = []

            for tung_doi_tuong_line,line in zip (doi_tuong_line, lines):

                duplicated = False

                for keep_line in ket_qua_line_tinh_toan:

                    if is_same_line(line, keep_line):

                        duplicated = True

                        break

                if not duplicated:
                    ket_qua_line_tinh_toan.append(line)
                    ket_qua_line_revit.append(tung_doi_tuong_line)

            return ket_qua_line_revit, ket_qua_line_tinh_toan
        

        def get_direction_of_line_or_grid(element):
            category_name_lan = element.Category.Name
            if category_name_lan in "Lines, 線分":
                direction = get_direction_of_beam(element)
            else:
                direction = element.Curve.Direction
            return direction
        
              
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        current_view = doc.ActiveView
        
        list_ref_element_da_chon = []

        line_elements_list = get_all_elements_by_category_in_view(doc, current_view, BuiltInCategory.OST_Lines)

        # list_line = []
        # list_grid = []

        trans_group = TransactionGroup(doc, 'Dim position of detail line')
        trans_group.Start()

        t = Transaction(doc, 'Set work plane')
        t.Start()
        set_work_plane = set_work_plane_for_view(current_view)
        t.Commit()

        if set_work_plane:

            if line_elements_list:

                selected_lines_grids = pick_lines_and_grid_by_rectangle()
                
                for moi_element in selected_lines_grids:
        
                    category_name = moi_element.Category.Name

                    if category_name in "Lines, 線分":        

                        ref_cua_element = Reference(moi_element)   

                        list_ref_element_da_chon.append(ref_cua_element)  

                        # list_line.append(ref_cua_element)    

                    else:

                        ref_cua_element = Reference(moi_element)    

                        list_ref_element_da_chon.append(ref_cua_element)   

                        # list_grid.append(ref_cua_element)    

            list_ref_cua_doi_tuong = list_ref_element_da_chon

            ref_array = ReferenceArray()

            covert_reference_to_element = []

            for i in list_ref_cua_doi_tuong:

                element_id = i.ElementId

                covert_reference_to_element.append(doc.GetElement(element_id))

            '''Dùng thuật toán bucket sorting để tìm ra group có số lượng dầm song song nhiều nhất'''

            parallel_groups = []

            for tung_doi_tuong in covert_reference_to_element:

                found_group = False

                direction = get_direction_of_line_or_grid(tung_doi_tuong)

                for group in parallel_groups:  

                    # Kiểm tra xem vector của dầm có song song với dầm trong nhóm không
                    if are_vector_parallel(group[0], direction):
                        group.append(tung_doi_tuong)
                        found_group = True
                        break
                # Nếu không tìm thấy nhóm nào, tạo nhóm mới
                if not found_group:
                    parallel_groups.append([direction, tung_doi_tuong])
            try:
                largest_group = max(parallel_groups, key=lambda g: len(g))
            except:
                sys.exit()
            
            # print("Nhóm có số dầm song song nhiều nhất: ")
            # for beam in largest_group[1:]: # Bỏ qua vector đầu tiên
            #     print("Dầm ID: {}".format(beam.Id))
            
            for tung_element in largest_group[1:]: # Bỏ qua giá trị đầu tiên vì giá trị đầu tiên là vector, không phải dầm.
                
                category_name = tung_element.Category.Name

                if category_name in "Lines, 線分":
                    
                    vector_beam = get_direction_of_beam(tung_element) 

                    break 
                
            vector_beam_lam_chuan_Z0 = XYZ(vector_beam.X, vector_beam.Y,0)
            
            list_dam_song_song = []
            list_doi_tuong_song_song = []
            list_vector_song_song = []
            for tung_element in covert_reference_to_element:
                try:
                    category_name = tung_element.Category.Name

                    direction = get_direction_of_line_or_grid(tung_element)

                    direction_Z0 = XYZ(direction.X, direction.Y,0)

                    if direction:

                        check_song_song = are_vector_parallel (vector_beam_lam_chuan_Z0, direction_Z0)

                        if check_song_song:

                            list_doi_tuong_song_song.append(tung_element)
                         
                except:
                    pass
            list_line_tinh_toan_se_dim = []

            from Autodesk.Revit.DB import Grid, DetailLine

            list_doi_tuong_song_song_sorted = sorted(list_doi_tuong_song_song,key=lambda x: 0 if isinstance(x, Grid) else 1)      #Sort để cho grid là số 0, sẽ sắp xếp toàn bộ grid ở trước danh sách, còn line là số 1 sẽ đứng sau.

            for grid_va_line_se_dim in list_doi_tuong_song_song_sorted:

                location_line_Z0 = get_location_curve_of_line_and_grid(grid_va_line_se_dim)

                list_line_tinh_toan_se_dim.append(location_line_Z0)

            ket_qua_loc = remove_duplicate_lines(list_doi_tuong_song_song_sorted,list_line_tinh_toan_se_dim)

            for tung_doi_tuong_line_grid in ket_qua_loc[0]:

                ref_doi_tuong = Reference(tung_doi_tuong_line_grid)

                ref_array.Append(ref_doi_tuong) 

            pick = pick_point_with_nearest_snap()

            xoay_vector_90_do = XYZ(-vector_beam_lam_chuan_Z0.Y, vector_beam_lam_chuan_Z0.X, vector_beam.Z)

            new_point = move_point_along_vector(pick,xoay_vector_90_do, 1)

            line = Line.CreateBound(pick,new_point)
    
            t = Transaction(doc,"Dim position of beam")

            t.Start()

            try:

                dim = create_dim(current_view,line,ref_array)

                t.Commit()
            except:
                # print(traceback.format_exc())
                t.RollBack()
    except:
        # print(traceback.format_exc())
        pass
    trans_group.Assimilate()