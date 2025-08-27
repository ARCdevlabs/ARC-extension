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
    
    def disallow_join_at_end(element):
        Autodesk.Revit.DB.Structure.StructuralFramingUtils.DisallowJoinAtEnd(element, 0)
        Autodesk.Revit.DB.Structure.StructuralFramingUtils.DisallowJoinAtEnd(element, 1)
    def allow_join_at_end(element):
        Autodesk.Revit.DB.Structure.StructuralFramingUtils.AllowJoinAtEnd(element, 0)
        Autodesk.Revit.DB.Structure.StructuralFramingUtils.AllowJoinAtEnd(element, 1)

    try:  
        Ele = nances.get_elements(uidoc,doc, 'Select Beam', noti = False)
        beams = FilteredElementCollector(doc, active_view.Id) \
    .OfCategory(BuiltInCategory.OST_StructuralFraming) \
    .WhereElementIsNotElementType() \
    .ToElements()
        detail_line = []
        # trans_group = TransactionGroup(doc, 'Extend Beams')
        # trans_group.Start()
        from nances import revit
        with revit.Transaction('nhập tên transaction', swallow_errors=True):
            try:
                for tung_beam in Ele:
                        location_line = tung_beam.Location.Curve
                        id_level_of_beam = nances.get_builtin_parameter_by_name(tung_beam, DB.BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM).AsElementId()
                        level_of_beam = doc.GetElement(id_level_of_beam)
                        start_point = location_line.GetEndPoint(0)
                        end_point = location_line.GetEndPoint(1)
                        level_elevation = level_of_beam.Elevation
                        new_start_point = XYZ(start_point.X,start_point.Y,level_of_beam.Elevation)
                        new_end_point = XYZ(end_point.X,end_point.Y,level_of_beam.Elevation)
                        new_center_line_in_level = Autodesk.Revit.DB.Line.CreateBound(new_start_point, new_end_point)
                        grids = get_all_grid_in_current_view(doc,active_view)
                        extend_mm = 700
                        extend = extend_mm/304.8
                        new_line_lan_1 = extend_line_lan_1(new_center_line_in_level, beams, extend,grids,active_view,level_elevation)
                        new_line_lan_2 = extend_line_lan_2(new_line_lan_1, beams, extend,grids,active_view,level_elevation)
                        start_point_cung_cao_do = XYZ(new_line_lan_2.GetEndPoint(0).X, new_line_lan_2.GetEndPoint(0).Y,location_line.GetEndPoint(0).Z) 
                        end_point_cung_cao_do = XYZ(new_line_lan_2.GetEndPoint(1).X, new_line_lan_2.GetEndPoint(1).Y,location_line.GetEndPoint(1).Z)           
                        line_cung_cao_do_ban_dau =  Autodesk.Revit.DB.Line.CreateBound(start_point_cung_cao_do, end_point_cung_cao_do)                     
                        # disallow_join_at_end(tung_beam)
                        # t = Transaction(doc, 'Extend Beams')
                        # t.Start()
                        if location_line.Length != line_cung_cao_do_ban_dau.Length:
                            tung_beam.Location.Curve = line_cung_cao_do_ban_dau
                    # detail_line.append(doc.Create.NewDetailCurve(active_view,new_line_lan_2))
                        allow_join_at_end(tung_beam)
                        # t.Commit()
            except:
                import traceback
                print(traceback.format_exc())
                pass
            # trans_group.Assimilate()
    except Exception as ex:
        import traceback
        print(traceback.format_exc())
        pass


