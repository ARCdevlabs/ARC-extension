# -*- coding: utf-8 -*-
import Autodesk
import nances
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
from nances import revit,vectortransform

if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    active_view = nances.Active_view(doc)

    def xac_dinh_phuong_doc_ngang(lines):
        list_ngang = []
        list_doc = []
        for line in lines:
            try:
                direction = line.Direction
                if abs(direction.X) < abs(direction.Y):
                    list_doc.append(line)            
                else:
                    list_ngang.append(line)
            except:
                pass
        return list_doc, list_ngang

    def check_huong (line):
        check = False
        try:
            huong_line = line.Direction
            point1 = line.GetEndPoint(0)
            point2 = line.GetEndPoint(1)
            if abs(huong_line.X) < abs(huong_line.Y):
                if point1.Y < point2.Y:
                    check = True      
                else:
                    check = False
            elif point1.X < point2.X:
                check = True
            else: 
                check = False
            if not check:
                reversed_line = line.CreateReversed()
                return reversed_line
            else:
                return line
        except:
            # import traceback
            # print(traceback.format_exc())
            pass

    def midpoint(point1, point2):
        """Tính trung điểm của hai điểm trong không gian 3D."""
        return XYZ(
            (point1.X + point2.X) / 2,
            (point1.Y + point2.Y) / 2,
            (point1.Z + point2.Z) / 2
        )
    def get_center_line(line_1, line_2):
        sp1 = line_1.GetEndPoint(0)
        ep1 = line_1.GetEndPoint(1)
        sp2 = line_2.GetEndPoint(0)
        ep2 = line_2.GetEndPoint(1)
        smp = midpoint(sp1, sp2)
        emp = midpoint(ep1, ep2)
        line = Autodesk.Revit.DB.Line.CreateBound(smp, emp)
        return line
    
    def create_beam(curve,beam_type,level):
        beam = doc.Create.NewFamilyInstance(curve, beam_type, level, Autodesk.Revit.DB.Structure.StructuralType.Beam)
        get_para_start_level_offset = nances.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)
        get_para_end_level_offset = nances.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION)
        get_para_start_level_offset.Set(0)
        get_para_end_level_offset.Set(0)
        return beam
    
    def active_symbol(element):
        try:
            if element.IsActive == False:
                element.Activate()
        except:
            pass
        return 

    
    def are_vector_parallel(vector_1, vector_2):
        tolerance=0.0001
        cross_product = vector_1.CrossProduct(vector_2)
        return cross_product.GetLength() < tolerance
    

    def tim_group_so_luong_song_song_nhieu_nhat (lines):
        '''Dùng thuật toán bucket sorting để tìm ra group có số lượng element song song nhiều nhất'''
        parallel_groups = []
        for element in lines:
            found_group = False
            # direction = element.Location.LocationCurve
            direction = element.Direction
            for group in parallel_groups:            
                # Kiểm tra xem vector của dầm có song song với dầm trong nhóm không
                if are_vector_parallel(group[0], direction):
                    group.append(element)
                    found_group = True
                    break

            # Nếu không tìm thấy nhóm nào, tạo nhóm mới
            if not found_group:
                parallel_groups.append([direction, element])
        try:
            largest_group = max(parallel_groups, key=lambda g: len(g))
        except:
            pass
        return largest_group[1:] # Bỏ qua giá trị đầu tiên vì giá trị đầu tiên là vector, không phải line.
    
    def are_lines_colinear(line1, line2, tol=0.001):
        # Vector chỉ phương của mỗi line
        dir1 = (line1.GetEndPoint(1) - line1.GetEndPoint(0)).Normalize()
        dir2 = (line2.GetEndPoint(1) - line2.GetEndPoint(0)).Normalize()

        # Kiểm tra 2 vector có cùng phương hoặc ngược phương
        same_direction = dir1.IsAlmostEqualTo(dir2, tol) or dir1.IsAlmostEqualTo(-dir2, tol)

        if not same_direction:
            return False

        # Vector nối từ điểm đầu của line1 tới điểm đầu của line2
        vec_between = line2.GetEndPoint(0) - line1.GetEndPoint(0)

        # Nếu vec_between cùng phương với dir1 → cùng nằm trên 1 đường thẳng
        # Vì nếu 3 điểm thẳng hàng → vector nối giữa 2 điểm nằm trên cùng phương với hướng line
        return vec_between.CrossProduct(dir1).IsZeroLength()

    def merge_lines(lines):
        merged = []
        visited = set()

        for i, line in enumerate(lines):
            if i in visited:
                continue
            points = [line.GetEndPoint(0), line.GetEndPoint(1)]
            visited.add(i)

            changed = True
            while changed:
                changed = False
                for j, other_line in enumerate(lines):
                    if j in visited:
                        continue
                    if are_lines_colinear(line, other_line):
                        visited.add(j)
                        pt1 = other_line.GetEndPoint(0)
                        pt2 = other_line.GetEndPoint(1)
                        if not any(pt.IsAlmostEqualTo(pt1) for pt in points):
                            points.append(pt1)
                        if not any(pt.IsAlmostEqualTo(pt2) for pt in points):
                            points.append(pt2)
                        changed = True

            # Sắp xếp điểm theo trục để nối thành đoạn thẳng duy nhất
            points.sort(key=lambda p: (p.X, p.Y, p.Z))
            new_line = Line.CreateBound(points[0], points[-1])
            merged.append(new_line)
        return merged   
    
    def are_parallel(line1, line2, tol=0.001):
        dir1 = (line1.GetEndPoint(1) - line1.GetEndPoint(0)).Normalize()
        dir2 = (line2.GetEndPoint(1) - line2.GetEndPoint(0)).Normalize()
        return dir1.IsAlmostEqualTo(dir2, tol) or dir1.IsAlmostEqualTo(-dir2, tol)

    def get_two_longest_parallel_lines(lines):
        max_pair = (None, None)
        max_total_length = 0

        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                line1 = lines[i]
                line2 = lines[j]
                if are_parallel(line1, line2):
                    total_length = line1.Length + line2.Length
                    if total_length > max_total_length:
                        max_total_length = total_length
                        max_pair = (line1, line2)
        
        return max_pair


    class LineSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
        def AllowElement(self, element):
            return element.Category.Name in "Lines, 線分"

    def pick_lines_by_rectangle():
        from nances import forms
        with forms.WarningBar(title='Quét chuột và chọn 2 detail line để vẽ dầm'):
            selection = uidoc.Selection
            selected_elements = selection.PickElementsByRectangle(LineSelectionFilter(), "Chọn các line")
        return selected_elements       

    def all_type_of_framing():
        all_type_of_framing = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_StructuralFraming)
        return all_type_of_framing
    

    def get_all_grid_in_current_view(doc, view):
        collector = FilteredElementCollector(doc, view.Id) \
                    .OfClass(Grid) \
                    .WhereElementIsNotElementType()  # Chỉ lấy instances

        return list(collector)
    
    def get_all_geometry_of_grids(grids, view, DatumExtentType = DatumExtentType.ViewSpecific ):
        all_geometry = []
        DatumExtentType = DatumExtentType.ViewSpecific
        for grid in grids:
            try:
                geometry_element = grid.GetCurvesInView(DatumExtentType, view)
                all_geometry.append(geometry_element[0])
                # for tung_geometry in geometry_element:
                #     all_geometry.append(tung_geometry)
                
            except:
                pass
        return all_geometry
    
    def find_intersection(line1, line2, level_elevation):
        """Tìm giao điểm của 2 đường thẳng trên mặt phẳng XY."""
        p1, p2 = line1.GetEndPoint(0), line1.GetEndPoint(1)
        p3, p4 = line2.GetEndPoint(0), line2.GetEndPoint(1)

        x1, y1 = p1.X, p1.Y
        x2, y2 = p2.X, p2.Y
        x3, y3 = p3.X, p3.Y
        x4, y4 = p4.X, p4.Y

        # Tính toán mẫu số
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        # Nếu mẫu số = 0, hai đường thẳng song song hoặc trùng nhau
        if abs(denominator) < 1e-9:
            return None  

        # Tìm giá trị t
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator

        # Tọa độ giao điểm
        x_inter = x1 + t * (x2 - x1)
        y_inter = y1 + t * (y2 - y1)

        return XYZ(x_inter, y_inter, level_elevation)  # Z luôn bằng 0 vì đường nằm trên mặt phẳng XY
    
    
    def get_nearby_beams(beams, reference_line, radius=5000/304.8):
        """Lọc các dầm trong bán kính 'radius' từ điểm đầu và cuối của reference_line."""
        start_point = reference_line.GetEndPoint(0)  # Điểm đầu của line
        end_point = reference_line.GetEndPoint(1)    # Điểm cuối của line

        nearby_beams = []

        for beam in beams:
            try:
            # Lấy tọa độ trung tâm của dầm
                location = beam.Location.Curve
                if not location:
                    continue

                if isinstance(location, Line):
                    beam_midpoint = (location.GetEndPoint(0) + location.GetEndPoint(1)) / 2
                else:
                    beam_midpoint = location.Point  # Nếu là LocationPoint thì lấy trực tiếp

                # Kiểm tra khoảng cách từ điểm đầu & cuối đến beam
                dist_to_start = beam_midpoint.DistanceTo(start_point)
                dist_to_end = beam_midpoint.DistanceTo(end_point)

                if dist_to_start <= radius or dist_to_end <= radius:
                    nearby_beams.append(beam)
            except:
                pass
        return nearby_beams
    
    def get_nearest_point(points, reference_point, extend_value):
        min_distance = float('inf')
        nearest_point = None
        
        for point in points:
            distance = point.DistanceTo(reference_point)
            if distance < min_distance:
                min_distance = distance
                if min_distance < extend_value:
                    nearest_point = point
        return nearest_point
    
    def extend_line_lan_1(line, beams, extend_length, grids, view, level_elevation):

        """Mở rộng line về hai phía 300mm, nếu gặp Beam thì dừng lại ở điểm giao nhau"""
        # Lấy điểm đầu và cuối của Line
        p1, p2 = line.GetEndPoint(0), line.GetEndPoint(1)

        list_intersect_point = []
        list_nearby_beams = get_nearby_beams (beams,line)
        list_grid_lines = get_all_geometry_of_grids(grids, view, DatumExtentType = DatumExtentType.ViewSpecific)    
        list_beam_line = []
        for beam in list_nearby_beams:
            beam_line = beam.Location.Curve
            list_beam_line.append(beam_line)
        grid_lines_and_beams_line = list_beam_line + list_grid_lines
        # Tìm điểm giao giữa line mở rộng và mặt của beam
        for tung_line in grid_lines_and_beams_line: 
            intersection = find_intersection(line,tung_line,level_elevation)
            if intersection:
                list_intersect_point.append(intersection)
        

        nearest_point = get_nearest_point(list_intersect_point,p1, extend_length)
        if nearest_point:

            tim_diem_gan_intersect_point = vectortransform.nearest_point(nearest_point, p1, p2)

            if tim_diem_gan_intersect_point == "StartPoint":
                new_line = DB.Line.CreateBound(nearest_point,p2)
            elif tim_diem_gan_intersect_point == "EndPoint":
                new_line = DB.Line.CreateBound(p1,nearest_point)
        else:
            new_line = line
        return new_line
    
    def extend_line_lan_2(line, beams, extend_length,grids, view,level_elevation):

        # Lấy điểm đầu và cuối của Line
        p1, p2 = line.GetEndPoint(0), line.GetEndPoint(1)

        list_intersect_point = []
        list_nearby_beams = get_nearby_beams (beams,line)
        list_grid_lines = get_all_geometry_of_grids(grids, view, DatumExtentType = DatumExtentType.ViewSpecific)    
        list_beam_line = []
        for beam in list_nearby_beams:
            beam_line = beam.Location.Curve
            list_beam_line.append(beam_line)
        grid_lines_and_beams_line = list_beam_line + list_grid_lines
        # Tìm điểm giao giữa line mở rộng và mặt của beam
        for tung_line in grid_lines_and_beams_line: 
            intersection = find_intersection(line,tung_line,level_elevation)
            if intersection:
                list_intersect_point.append(intersection)

        nearest_point = get_nearest_point(list_intersect_point,p2, extend_length)

        if nearest_point:
            tim_diem_gan_intersect_point = nances.vectortransform.nearest_point(nearest_point, p1, p2)
            if tim_diem_gan_intersect_point == "StartPoint":
                new_line = DB.Line.CreateBound(nearest_point,p2)
            elif tim_diem_gan_intersect_point == "EndPoint":
                new_line = DB.Line.CreateBound(p1,nearest_point)
        else:
            new_line = line
        return new_line

    from pyrevit import script
    logger = script.get_logger()
    my_config = script.get_config("setting_type_beam_by_detail_line")
    import setting_config
    all_type_beam = all_type_of_framing()
    selected_type_beam = None
    try:
        get_source = setting_config.load_configs()
        source_beam_type = get_source[0][0]
        source_phuong_dam = get_source[0][1]
        extend_mm = float(get_source[0][2])
        if source_phuong_dam == "Phương dọc":
            phuong_dam = 0
        if source_phuong_dam == "Phương ngang":
            phuong_dam = 1
        if source_phuong_dam == "Tự do":
            phuong_dam = 2
        if source_beam_type:
            for tung_type in all_type_beam:
                type_name = DB.Element.Name.GetValue(tung_type)
                if type_name == source_beam_type:
                    selected_type_beam = tung_type
                    break
            if  selected_type_beam == None:
                selected_type_beam = tung_type
    except:
        selected_type_beam = all_type_beam.FirstElement()
        phuong_dam = 2
        extend_mm = float(2500)
    def main():
    # Bat dau vong lap lua chon
        run = True
        while run == True:
            try:  
                line_da_chuan_hoa = []
                pick_line = pick_lines_by_rectangle()
                Ele = pick_line
                for tung_line in Ele:
                    location_line = tung_line.Location.Curve
                    line_chuan = check_huong (location_line)
                    line_da_chuan_hoa.append(line_chuan)

                loc_phuong_doc_ngang = xac_dinh_phuong_doc_ngang(line_da_chuan_hoa)

                if phuong_dam == 0:
                    danh_sach_phuong_doc = loc_phuong_doc_ngang[0] #nếu là phương ngang thì list[1]
                if phuong_dam == 1:
                    danh_sach_phuong_doc = loc_phuong_doc_ngang[1] #nếu là phương ngang thì list[1]
                if phuong_dam == 2:
                    danh_sach_phuong_doc = line_da_chuan_hoa

                group_song_song = tim_group_so_luong_song_song_nhieu_nhat (danh_sach_phuong_doc)     
                merge_cac_line_nam_cung_duong_thang = merge_lines(group_song_song)  
                hai_line_song_song_va_dai_nhat = get_two_longest_parallel_lines(merge_cac_line_nam_cung_duong_thang)
                

                level = active_view.GenLevel
                beam_type = selected_type_beam
                
                # beams = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()
                # current_view = doc.ActiveView
                beams = FilteredElementCollector(doc, active_view.Id) \
                    .OfCategory(BuiltInCategory.OST_StructuralFraming) \
                    .WhereElementIsNotElementType() \
                    .ToElements()
                center_line = get_center_line(hai_line_song_song_va_dai_nhat[0],hai_line_song_song_va_dai_nhat[1])
                # center_line = get_center_line(group_song_song[0],group_song_song[1])
                start_point = center_line.GetEndPoint(0)
                end_point = center_line.GetEndPoint(1)
                level_elevation = level.Elevation
                new_start_point = XYZ(start_point.X,start_point.Y,level.Elevation)
                new_end_point = XYZ(end_point.X,end_point.Y,level.Elevation)
                new_center_line_in_level = Autodesk.Revit.DB.Line.CreateBound(new_start_point, new_end_point)
                grids = get_all_grid_in_current_view(doc,active_view)
                
                extend = extend_mm/304.8
                
                new_line_lan_1 = extend_line_lan_1(new_center_line_in_level, beams, extend,grids,active_view,level_elevation)
                new_line_lan_2 = extend_line_lan_2(new_line_lan_1, beams, extend,grids,active_view,level_elevation)
                

                with revit.Transaction('Create Beam By Detail Line', swallow_errors=True):
                    active_symbol(beam_type)
                    # det_line = doc.Create.NewDetailCurve(active_view, center_line)
                    create_beam(new_line_lan_2,beam_type,level)
                    # create_beam(center_line,beam_type,level)
            except Exception as ex:
                # import traceback
                # print(traceback.format_exc())
                pass
                if "The user aborted the pick operation." in str(ex):
                    run = False
                    break
                # else:
                #     run = False
                #     break
    main()

