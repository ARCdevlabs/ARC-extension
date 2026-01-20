# -*- coding: utf-8 -*-
import Autodesk
import nances
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit import script
from nances import geometry,vectortransform
import setup_family_beam_config #cần import dòng này, đây là tên của script config
import traceback
import math
from Autodesk.Revit.UI import RevitCommandId

"""def viết thêm"""
def tinh_chieu_rong_dam(beam):
    #Lấy vector trục dầm

    # Xác định vector vuông góc với trục dầm

    # Chiếu các điểm bounding box lên vector đó

    # Lấy max – min → ra chiều rộng

    loc_curve = beam.Location.Curve
    direction_beam = (loc_curve.GetEndPoint(1) - loc_curve.GetEndPoint(0)).Normalize() #chuan hoa vector huong dam
    Z = XYZ.BasisZ
    width_direction = direction_beam.CrossProduct(Z).Normalize() #ket qua la vector

    bbox = beam.get_BoundingBox(None)
    min_pt = bbox.Min
    max_pt = bbox.Max
    points = [
    XYZ(min_pt.X, min_pt.Y, min_pt.Z),
    XYZ(min_pt.X, min_pt.Y, max_pt.Z),
    XYZ(min_pt.X, max_pt.Y, min_pt.Z),
    XYZ(min_pt.X, max_pt.Y, max_pt.Z),
    XYZ(max_pt.X, min_pt.Y, min_pt.Z),
    XYZ(max_pt.X, min_pt.Y, max_pt.Z),
    XYZ(max_pt.X, max_pt.Y, min_pt.Z),
    XYZ(max_pt.X, max_pt.Y, max_pt.Z),
    ]
    projections = [p.DotProduct(width_direction) for p in points]  
    
    #Ta đổ bóng (chiếu) từng điểm point lên vector vuông góc với dầm và
    #lấy khoảng cách có dấu từ gốc tọa độ đến điểm chiếu. (khoảng cách lúc này rất lớn vì tính từ mốc 0,0,0)
  
    width = max(projections) - min(projections) #Hàm này sẽ triệt tiêu khoảng cách tính từ tọa độ.

    return width

def tinh_chieu_cao_dam(beam):
    # Vector phương thẳng đứng
    height_direction = XYZ.BasisZ  # (0,0,1)

    # Bounding box của dầm
    bbox = beam.get_BoundingBox(None)
    min_pt = bbox.Min
    max_pt = bbox.Max

    # 8 điểm của bounding box
    points = [
        XYZ(min_pt.X, min_pt.Y, min_pt.Z),
        XYZ(min_pt.X, min_pt.Y, max_pt.Z),
        XYZ(min_pt.X, max_pt.Y, min_pt.Z),
        XYZ(min_pt.X, max_pt.Y, max_pt.Z),
        XYZ(max_pt.X, min_pt.Y, min_pt.Z),
        XYZ(max_pt.X, min_pt.Y, max_pt.Z),
        XYZ(max_pt.X, max_pt.Y, min_pt.Z),
        XYZ(max_pt.X, max_pt.Y, max_pt.Z),
    ]

    # Chiếu các điểm lên trục Z
    projections = [p.DotProduct(height_direction) for p in points]

    # Chiều cao = max - min
    height = max(projections) - min(projections)

    return height


def tinh_diem_trung_tam_bounding_box(element):
    bbox = element.get_BoundingBox(None)
    min_pt = bbox.Min
    max_pt = bbox.Max
    trung_diem = (min_pt + max_pt ) /2
    return trung_diem

def get_geometry_to_solid(element):
    options = Options()
    options.ComputeReferences = True
    options.DetailLevel = ViewDetailLevel.Fine  
    curves = CurveArray() #khong can lay curve thi bo qua
    solids = []
    all_geometry =  element.get_Geometry(options)
    for tung_loai_geometry in all_geometry: # Curve
        if isinstance(tung_loai_geometry, Curve):
            curves.Append(tung_loai_geometry)
            continue
        # Solid
        if isinstance(tung_loai_geometry, Solid):
            # loại bỏ solid rỗng
            if tung_loai_geometry.Volume > 0:
                solids.append(tung_loai_geometry)
            continue
        if isinstance(tung_loai_geometry, GeometryInstance):
            # transformed_geometry = tung_loai_geometry.GetInstanceGeometry(tung_loai_geometry.Transform)  #Dong nay khong can dung nua        
            transformed_geometry = tung_loai_geometry.GetInstanceGeometry()    
            for tung_dang_geometry in transformed_geometry:
                # loại bỏ solid rỗng
                if hasattr(tung_dang_geometry, "Volume"):
                    if tung_dang_geometry.Volume > 0:
                        solids.append(tung_dang_geometry)
    return solids #Trả về dạng list các solid

def get_face_from_solid(solid):
    list_faces =[]
    if hasattr(solid, "Faces"):
        for face in solid.Faces:
            if str(type(face)) == "<type 'PlanarFace'>":
                list_faces.append(face)
    return list_faces

def project_point_to_plane_by_view(point, plane, view):
    #Gióng point lên plane theo hướng NGƯỢC ViewDirection
    P = point
    D = -view.ViewDirection.Normalize()   # hướng gióng

    P0 = plane.Origin
    N = plane.Normal.Normalize()

    denom = D.DotProduct(N)
    if abs(denom) < 1e-9:
        return None  # song song → không cắt plane

    t = (P0 - P).DotProduct(N) / denom
    projected_point = P + D.Multiply(t)

    return projected_point

def rotate_line_around_view_direction(line, view, angle_deg):
    """
    Xoay line quanh ViewDirection một góc angle_deg (độ)
    """
    # điểm xoay (lấy midpoint)
    P = (line.GetEndPoint(0) + line.GetEndPoint(1)) / 2

    # trục xoay
    axis_dir = view.ViewDirection.Normalize()
    axis = Line.CreateUnbound(P, axis_dir)

    # transform xoay
    angle_rad = math.radians(angle_deg)
    transform = Transform.CreateRotationAtPoint(axis_dir, angle_rad, P)

    # line mới sau khi xoay
    new_line = line.CreateTransformed(transform)

    return new_line

def tao_plane_man_hinh (view):
    origin = view.Origin
    vector_direction = view.ViewDirection
    plane_man_hinh = vectortransform.create_plane_from_point_and_normal(origin,vector_direction)
    return plane_man_hinh

def project_line_to_plane (line, view): #mục đích tạo 1 line phẳng trên view màn hình
    view_direction = view.ViewDirection
    start = line.GetEndPoint(0)
    end = line.GetEndPoint(1)
    plane_man_hinh = vectortransform.create_plane_from_point_and_normal(start,view_direction)
    flat_start = project_point_to_plane_by_view(start,plane_man_hinh,view)
    flat_end = project_point_to_plane_by_view(end,plane_man_hinh,view)
    flat_line =  Line.CreateBound(flat_start,flat_end)
    return flat_line

def get_rotate_90_location_line(line, view):
    start = line.GetEndPoint(0)
    end = line.GetEndPoint(1)
    view_direction = view.ViewDirection
    plane_man_hinh = vectortransform.create_plane_from_point_and_normal(start,view_direction) #mặt phẳng đại diện cho màn hình.
    flat_start = project_point_to_plane_by_view(start,plane_man_hinh,view)
    flat_end = project_point_to_plane_by_view(end,plane_man_hinh,view)
    flat_line =  Line.CreateBound(flat_start,flat_end)
    rotate_line = rotate_line_around_view_direction(flat_line, view, 90)
    return rotate_line


def get_center_plane (wall):
    wall_location = wall.Location
    wall_location_curve = wall_location.Curve
    start_point = wall_location_curve.GetEndPoint(0)
    endpoint = wall_location_curve.GetEndPoint(1)
    mid_point = wall_location_curve.Evaluate(0.5, True)
    offset_mid_point = XYZ(start_point.X, start_point.Y, mid_point.Z +10000)
    point1 = start_point
    point2 = endpoint
    point3 =offset_mid_point
    vector1 = point2 - point1
    vector2 = point3 - point1
    normal_vector = vector1.CrossProduct(vector2).Normalize()
    plane = Plane.CreateByNormalAndOrigin(normal_vector, mid_point)
    return plane

def move_line_theo_vector_theo_ty_le_view(vector_de_move_line, line, snap_dim, view):
    start = line.GetEndPoint(0)
    end = line.GetEndPoint(1)
    view_scale = view.Scale
    # snap_dim = (5*(5/3)) * (1/304.8)* view_scale #1mm bang 0.003084
    khoang_cach_move = snap_dim * view_scale
    move_start_point = vectortransform.move_point_along_vector(start, vector_de_move_line, khoang_cach_move)
    move_end_point = vectortransform.move_point_along_vector(end, vector_de_move_line, khoang_cach_move)
    new_line = DB.Line.CreateBound(move_start_point, move_end_point)
    return new_line


def tinh_toan_can_thiet_move_text_dim (dim, view):
    seg_1_value = float(dim.Segments.Item[0].Value * 304.8)
    seg_2_value = float(dim.Segments.Item[1].Value * 304.8)
    round_format_value_1 = round(seg_1_value,2)
    round_format_value_2 = round(seg_2_value,2)
    formatted_value_1 = str(round_format_value_1).rstrip('0').rstrip('.')
    formatted_value_2 = str(round_format_value_2).rstrip('0').rstrip('.')
    len_formatted_value_1 = len(formatted_value_1)
    len_formatted_value_2 = len(formatted_value_2)
    one_unit_width = 2 #Chieu rong 1 don vi text
    width_text_1 = float(len_formatted_value_1 * one_unit_width * (view.Scale))
    width_text_2 = float(len_formatted_value_2 * one_unit_width * (view.Scale))
    if seg_1_value < width_text_1 or seg_2_value < width_text_2: 

        can_chinh_text_dim = True 
    else:
        can_chinh_text_dim = False

    return can_chinh_text_dim

def select_sau_khi_chay_tool (list_elements, uidoc):
    if len(list_elements) > 0:
        select = uidoc.Selection
        list_id = []
        for tung_element in list_elements:
            element_id = tung_element.Id
            list_id.append(element_id)
        Icollection = List[ElementId](list_id)
        select.SetElementIds(Icollection)
    return

def loc_grid_nam_ben_trong_dam(grids):
    for grid in grids:
        list_grid_ref = []
        get_hide_isolate = check_hide_isolate(current_view, grid)
        get_hidden_element = check_hidden(grid,current_view)
        if get_hide_isolate and get_hidden_element:
            geo_all_grid = get_all_geometry_of_grids(grid, DatumExtentType)
            for one_grid_curve in geo_all_grid:
                for two_grid_curve in one_grid_curve:
                    grid_plane = vectortransform.create_plane_follow_line(two_grid_curve)
                    check_pararel_beam_with_grid = vectortransform.are_planes_parallel(center_plane_normal,grid_plane.Normal)
                    if check_pararel_beam_with_grid:
                        distance_grid_with_beam =  abs(vectortransform.distance_between_parallel_planes(grid_plane, center_plane))
                        if distance_grid_with_beam < (chieu_rong/2):
                            ref_grid = Reference(grid)
                            # all_ref.Append(ref_grid)
                            list_grid_ref.append(ref_grid)
        if len(list_grid_ref) > 0: #Dòng này thêm vào mục đích tránh cho việc dim thêm grid khác nữa.
            break
    return list_grid_ref

"""Cũ"""

def get_all_grid():
    collector = FilteredElementCollector(doc).OfClass(Grid)
    grids = collector.ToElements()
    return grids
def get_all_geometry_of_grids(grid, DatumExtentType = DatumExtentType.ViewSpecific):
    all_geometry = []
    DatumExtentType = DatumExtentType.ViewSpecific
    try:
        geometry_element = grid.GetCurvesInView(DatumExtentType,current_view)
        all_geometry.append(geometry_element)
    except:
        pass
    return all_geometry

def check_hide_isolate(view, element):
    view_mode = TemporaryViewMode.TemporaryHideIsolate
    boolean = view.IsElementVisibleInTemporaryViewMode(view_mode, element.Id)
    return boolean
def check_hidden(element, view):
    boolean = element.IsHidden(view)
    not_boolean = not(boolean)
    return not_boolean


logger = script.get_logger()

my_config = script.get_config()

source_setting_family_beam = setup_family_beam_config.load_configs_setup_family()

source_setting_dim_in_need = setup_family_beam_config.load_configs_setup_dim_in_need()


if nances.AutodeskData():
    uiapp = __revit__
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document

    def get_reference_by_name_in_family (instance, name):
        ref = instance.GetReferenceByName(name)
        return ref

    current_view = uidoc.ActiveView
    is_legend = current_view.ViewType == ViewType.Legend
    is_plan_view = current_view.ViewType in [ViewType.FloorPlan, ViewType.CeilingPlan, ViewType.EngineeringPlan]
    is_section_elevation = current_view.ViewType in [ViewType.Section, ViewType.Elevation]

    option_dim_combo_3 = source_setting_dim_in_need[0]
    option_dim_combo_2 = source_setting_dim_in_need[1]
    option_dim_combo_1 = source_setting_dim_in_need[2]

    Ele = nances.get_elements(uidoc,doc, 'Select Beams', noti = False)

    list_new_dim =[]

    all_grid = get_all_grid()
    trans_group = TransactionGroup(doc, 'Dimension beam_new version')
    trans_group.Start()
    list_error = []
    for tung_beam in Ele:  
        all_ref = ReferenceArray()
        ref_beam = Reference(tung_beam)
        combo_ref_1 = ReferenceArray()
        combo_ref_2 = ReferenceArray()
        combo_ref_3 = ReferenceArray()

        #ref theo mat cat
        combo_ref_A = ReferenceArray()
        combo_ref_B = ReferenceArray()
        combo_ref_C = ReferenceArray()
        combo_ref_D = ReferenceArray()
        combo_ref_E = ReferenceArray()

        all_ref.Clear()

        center_plane = get_center_plane(tung_beam)
        center_plane_normal = center_plane.Normal

        chieu_rong = tinh_chieu_rong_dam(tung_beam)

        location_line = tung_beam.Location.Curve

        #Thông thường parameter "Dimension Line Snap Distance" có giá trị là 5mm
        snap_dim_mm = 5 #tính bằng mm
        
        snap_dim_feet = snap_dim_mm  / 304.8  #tính bằng feet

        for grid in all_grid:
            list_grid_ref = []
            get_hide_isolate = check_hide_isolate(current_view, grid)
            get_hidden_element = check_hidden(grid,current_view)

            if get_hide_isolate and get_hidden_element:
                geo_all_grid = get_all_geometry_of_grids(grid, DatumExtentType)
                for one_grid_curve in geo_all_grid:
                    for two_grid_curve in one_grid_curve:
                        grid_plane = vectortransform.create_plane_follow_line_in_view (two_grid_curve,current_view)
                        check_pararel_beam_with_grid = vectortransform.are_planes_parallel(center_plane_normal,grid_plane.Normal)
                        if check_pararel_beam_with_grid:
                            distance_grid_with_beam =  abs(vectortransform.distance_between_parallel_planes(grid_plane, center_plane))
                            if distance_grid_with_beam < (chieu_rong/2):
                                ref_grid = Reference(grid)
                                all_ref.Append(ref_grid)
                                list_grid_ref.append(ref_grid)
            if len(list_grid_ref) > 0: #Dòng này thêm vào mục đích tránh cho việc dim thêm grid khác nữa.
                break

        if is_plan_view:
            flat_location_line = project_line_to_plane (location_line, current_view) 

            flat_location_line_direction = flat_location_line.Direction

            chuan_hoa_vector_kieu_nguoc = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_duoi_len_tren(flat_location_line_direction,current_view)

            line_combo_2 = get_rotate_90_location_line(location_line,current_view)
            
            line_combo_1 = move_line_theo_vector_theo_ty_le_view(chuan_hoa_vector_kieu_nguoc, line_combo_2, snap_dim_feet, current_view)

            line_combo_3 = move_line_theo_vector_theo_ty_le_view(-chuan_hoa_vector_kieu_nguoc, line_combo_2, snap_dim_feet, current_view)

            # for grid in all_grid:
            #     list_grid_ref = []
            #     get_hide_isolate = check_hide_isolate(current_view, grid)
            #     get_hidden_element = check_hidden(grid,current_view)

            #     if get_hide_isolate and get_hidden_element:
            #         geo_all_grid = get_all_geometry_of_grids(grid, DatumExtentType)
            #         for one_grid_curve in geo_all_grid:
            #             for two_grid_curve in one_grid_curve:
            #                 grid_plane = vectortransform.create_plane_follow_line_in_view (two_grid_curve,current_view)
            #                 check_pararel_beam_with_grid = vectortransform.are_planes_parallel(center_plane_normal,grid_plane.Normal)
            #                 if check_pararel_beam_with_grid:
            #                     distance_grid_with_beam =  abs(vectortransform.distance_between_parallel_planes(grid_plane, center_plane))
            #                     if distance_grid_with_beam < (chieu_rong/2):
            #                         ref_grid = Reference(grid)
            #                         all_ref.Append(ref_grid)
            #                         list_grid_ref.append(ref_grid)
            #     if len(list_grid_ref) > 0: #Dòng này thêm vào mục đích tránh cho việc dim thêm grid khác nữa.
            #         break
            
        type_of_ele = tung_beam.GetType()


        tc_trai = 0
        tc_phai = 0
        tc_bot = 0
        tc_top = 0

        if str(type_of_ele) == "Autodesk.Revit.DB.FamilyInstance":

            try:
                param_host_level = nances.get_builtin_parameter_by_name(tung_beam,BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM)
                host_level_id = param_host_level.AsElementId()
                host_level = doc.GetElement(host_level_id)
            except:            
                # print("Top fukashi parameter name not found")
                pass
            
            try:
                tc_top = nances.get_parameter_value_by_name(tung_beam, source_setting_family_beam[8])
            except:
                list_error.append("Top fukashi parameter name not found")                
                # print("Top fukashi parameter name not found")
                pass
            
            try:
                tc_bot = nances.get_parameter_value_by_name(tung_beam, source_setting_family_beam[9])
            except:
                list_error.append("Bottom fukashi parameter name not found")             
                # print("Bottom fukashi parameter name not found")
                pass
            
            try:
                tc_trai = nances.get_parameter_value_by_name(tung_beam, source_setting_family_beam[10])
            except: 
                list_error.append("Left fukashi parameter name not found")             
                # print("Left fukashi parameter name not found")
                pass
            
            try:
                tc_phai = nances.get_parameter_value_by_name(tung_beam, source_setting_family_beam[11])
            except:
                list_error.append("Right fukashi parameter name not found")                     
                # print("Right fukashi parameter name not found")
                pass
            
            try:
                ref_top = get_reference_by_name_in_family(tung_beam,source_setting_family_beam[0])
            except:               
                # print("Top reference name not found")
                pass   
            
            try:             
                ref_bot = get_reference_by_name_in_family(tung_beam,source_setting_family_beam[1])   
            except:              
                # print("Bottom reference name not found")
                pass  
            
            try:                   
                ref_trai = get_reference_by_name_in_family(tung_beam,source_setting_family_beam[2])
            except:               
                # print("Left reference name not found")
                pass  
            
            try:
                ref_phai = get_reference_by_name_in_family(tung_beam,source_setting_family_beam[3])
            except:                
                # print("Bottom reference name not found")
                pass  
            
            try:
                ref_fukashi_top = get_reference_by_name_in_family(tung_beam,source_setting_family_beam[4])
            except:          
                # print("Top fukashi reference name not found")
                pass      

            try:            
                ref_fukashi_bot = get_reference_by_name_in_family(tung_beam,source_setting_family_beam[5])    
            except:              
                # print("Bottom fukashi reference name not found")
                pass 

            try:                     
                ref_fukashi_trai = get_reference_by_name_in_family(tung_beam,source_setting_family_beam[6])
            except:              
                # print("Left fukashi reference name not found")
                pass

            try: 
                ref_fukashi_phai = get_reference_by_name_in_family(tung_beam,source_setting_family_beam[7])
            except:              
                # print("Right fukashi reference name not found")
                pass 

        if is_plan_view:

            #Combo 1_dim tổng
            combo_ref_1.Append(ref_fukashi_trai)
            combo_ref_1.Append(ref_fukashi_phai)

            #Combo 2_dim chia tâm
            combo_ref_2.Append(ref_fukashi_trai)
            combo_ref_2.Append(ref_fukashi_phai)
            try:
                check_grid_and_beam =[]
                for check_ref_grid in all_ref:
                    if ref_grid == check_ref_grid:
                        combo_ref_2.Append(check_ref_grid)
                        check_grid_and_beam.append(True)
                if len(check_grid_and_beam) == 0:
                    combo_ref_2.Append(ref_beam)
            except:
                combo_ref_2.Append(ref_beam)
                pass

            #Combo 3_dim tăng cường
            combo_ref_3.Append(ref_fukashi_trai)
            combo_ref_3.Append(ref_fukashi_phai)
            if float(tc_trai) > 0:
                combo_ref_3.Append(ref_trai)
            if float(tc_phai) > 0:
                combo_ref_3.Append(ref_phai)

            t = Transaction(doc,"Dim beam")
            t.Start() 
            try:
                # Trường hợp đã có sẵn tăng cường dầm rồi, dim 1 lần được 3 combo luôn.
                if  option_dim_combo_1:
                    new_dim_combo_1 = doc.Create.NewDimension(current_view, line_combo_1, combo_ref_1)
                    list_new_dim.append(new_dim_combo_1)
                if option_dim_combo_2:
                    new_dim_combo_2 = doc.Create.NewDimension(current_view, line_combo_2, combo_ref_2)

                    #Dòng này dùng để tính toán xem dim số 2 có cần phải move text không?
                    if tinh_toan_can_thiet_move_text_dim (new_dim_combo_2, current_view): 
                        list_new_dim.append(new_dim_combo_2)

                if option_dim_combo_3:    
                    if float(tc_trai) > 0 or float(tc_phai) > 0:
                        new_dim_combo_3 = doc.Create.NewDimension(current_view, line_combo_3, combo_ref_3)
                        list_new_dim.append(new_dim_combo_3)
                t.Commit()
            except:                
                pass
                t.RollBack()

        if is_section_elevation:
            
            view_scale = current_view.Scale

            right_direction = current_view.RightDirection

            up_direction = current_view.UpDirection
            
            trung_diem = tinh_diem_trung_tam_bounding_box(tung_beam)

            plane_man_hinh = tao_plane_man_hinh (current_view)

            giong_len_plane_cua_view = project_point_to_plane_by_view(trung_diem, plane_man_hinh, current_view)

            move_point_qua_phai = vectortransform.move_point_along_vector(giong_len_plane_cua_view, right_direction, 1)

            line_ngang_ngay_tam = DB.Line.CreateBound(giong_len_plane_cua_view,move_point_qua_phai)
            
            move_point_len_tren = vectortransform.move_point_along_vector(giong_len_plane_cua_view, up_direction, 1)

            line_doc_ngay_tam = DB.Line.CreateBound(giong_len_plane_cua_view,move_point_len_tren)

            chieu_cao_dam = tinh_chieu_cao_dam(tung_beam)
               
            #Line dim phương ngang
            #Thêm hàm để so sánh cao độ dầm so với level. Thông thường dầm dưới 1F thì là dầm móng. Còn dầm trên 1F là dầm thường.
            if 0 > giong_len_plane_cua_view.Z:
                line_combo_C = line_ngang_ngay_tam  
            else:
                tinh_toan_offset_tinh_tu_mat_dam_phuong_chieu_cao = (chieu_cao_dam/2 + 450/304.8) / view_scale #chia trước cho scale vì def move_line_theo_vector_theo_ty_le_view nhân scale lên lại.
                line_combo_C =  move_line_theo_vector_theo_ty_le_view(-up_direction , line_ngang_ngay_tam, tinh_toan_offset_tinh_tu_mat_dam_phuong_chieu_cao, current_view)
            
            line_combo_B =  move_line_theo_vector_theo_ty_le_view(-up_direction, line_combo_C, snap_dim_feet, current_view)

            line_combo_A =  move_line_theo_vector_theo_ty_le_view(-up_direction, line_combo_B, snap_dim_feet, current_view)

            #Line dim phương dọc
            
            tinh_toan_offset_tinh_tu_mat_dam_theo_chieu_rong = (chieu_rong/2 + 450/304.8) / view_scale #chia trước cho scale vì def move_line_theo_vector_theo_ty_le_view nhân scale lên lại.
            
            line_combo_E =  move_line_theo_vector_theo_ty_le_view(right_direction , line_doc_ngay_tam, tinh_toan_offset_tinh_tu_mat_dam_theo_chieu_rong, current_view)

            line_combo_D =  move_line_theo_vector_theo_ty_le_view(right_direction , line_combo_E, snap_dim_feet, current_view)
            
            #Combo A_dim tổng phương ngang
            combo_ref_A.Append(ref_fukashi_trai)
            combo_ref_A.Append(ref_fukashi_phai)

            #Combo B_dim chia tâm
            combo_ref_B.Append(ref_fukashi_trai)
            combo_ref_B.Append(ref_fukashi_phai)
            try:
                check_grid_and_beam =[]
                for check_ref_grid in all_ref:
                    if ref_grid == check_ref_grid:
                        combo_ref_B.Append(check_ref_grid)
                        check_grid_and_beam.append(True)
                if len(check_grid_and_beam) == 0:
                    combo_ref_B.Append(ref_beam)
            except:
                combo_ref_B.Append(ref_beam)
                pass

            #Combo C_dim tăng cường
            combo_ref_C.Append(ref_fukashi_trai)
            combo_ref_C.Append(ref_fukashi_phai)
            if float(tc_trai) > 0:
                combo_ref_C.Append(ref_trai)
            if float(tc_phai) > 0:
                combo_ref_C.Append(ref_phai)

            #Combo D_dim tăng cường
            combo_ref_D.Append(ref_fukashi_bot)
            combo_ref_D.Append(ref_fukashi_top)      
            combo_ref_D.Append(Reference(host_level))
     

            #Combo E_dim tăng cường
            combo_ref_E.Append(ref_fukashi_bot)
            combo_ref_E.Append(ref_fukashi_top) 
            if float(tc_top) > 0:
                combo_ref_E.Append(ref_top)
            if float(tc_bot) > 0:
                combo_ref_E.Append(ref_bot)            

            t = Transaction(doc,"Dim beam in section")
            t.Start() 
            try:
                
                new_dim_combo_C = doc.Create.NewDimension(current_view, line_combo_C, combo_ref_C)

                new_dim_combo_B = doc.Create.NewDimension(current_view, line_combo_B, combo_ref_B)

                if tinh_toan_can_thiet_move_text_dim (new_dim_combo_B, current_view): 
                    list_new_dim.append(new_dim_combo_B)

                new_dim_combo_A = doc.Create.NewDimension(current_view, line_combo_A, combo_ref_A)

                new_dim_combo_D = doc.Create.NewDimension(current_view, line_combo_D, combo_ref_D)

                new_dim_combo_E = doc.Create.NewDimension(current_view, line_combo_E, combo_ref_E)

                list_new_dim.append(new_dim_combo_C)
                list_new_dim.append(new_dim_combo_E)

                t.Commit()

            #     detail_curve_of_location_curve = doc.Create.NewDetailCurve(current_view,line_combo_C)
            except:                
                pass
                t.RollBack()

    select_sau_khi_chay_tool (list_new_dim, uidoc)

    set_error = list(set(list_error))
    if len(set_error) > 0:
        output = script.get_output()
        logger = script.get_logger()
        logger.warning("Please hold Shift and click to the tool to setup input family")
        for tung_loi in set_error:
            print tung_loi                      
    trans_group.Assimilate()    
    if len(list_new_dim) > 0 :
        run_move_text_type_1 = uiapp.PostCommand(RevitCommandId.LookupCommandId("CustomCtrl_%CustomCtrl_%ARC drawing%Dimension%Type 1 Auto"))

    