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


"""Cũ"""


def get_wall_reference_by_magic(uid,index):
    format = "{0}:{1}:{2}"
    nine = -9999
    refString = str.Format(format,uid,nine,index)
    return refString


def get_wall_reference_by_type(uid,index):
    from Autodesk.Revit.DB import Reference
    format = "{0}:{1}:{2}"
    type = 'SURFACE'
    refString = str.Format(format,uid,index,type)
    return refString

def move_point_along_vector(point, vector, distance):
    new_point = point + vector.Normalize() * distance
    return new_point


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

    option_dim_only_combo_3 = False

    Ele = nances.get_elements(uidoc,doc, 'Select Beam', noti = False)

    list_new_dim =[]

    all_grid = get_all_grid()
    trans_group = TransactionGroup(doc, 'Dimension beam')
    trans_group.Start()
    for tung_beam in Ele:    
        t = Transaction(doc,"Dim beam")
        t.Start() 
        all_ref = ReferenceArray()
        ref_beam = Reference(tung_beam)
        combo_ref_1 = ReferenceArray()
        combo_ref_2 = ReferenceArray()
        combo_ref_3 = ReferenceArray()
        all_ref.Clear()

        center_plane = get_center_plane(tung_beam)
        center_plane_normal = center_plane.Normal

        chieu_rong = tinh_chieu_rong_dam(tung_beam)
  
        location_line = tung_beam.Location.Curve

        flat_location_line = project_line_to_plane (location_line, current_view) 

        flat_location_line_direction = flat_location_line.Direction

        chuan_hoa_vector_kieu_nguoc = vectortransform.chuan_hoa_vector_kieu_nguoc(flat_location_line_direction,current_view)

        line_combo_2 = get_rotate_90_location_line(location_line,current_view)
        
        #Thông thường parameter "Dimension Line Snap Distance" có giá trị là 5mm
        snap_dim_mm = 5 #tính bằng mm

        snap_dim_feet = snap_dim_mm  / 304.8  #tính bằng feet

        line_combo_1 = move_line_theo_vector_theo_ty_le_view(chuan_hoa_vector_kieu_nguoc, line_combo_2, snap_dim_feet, current_view)

        line_combo_3 = move_line_theo_vector_theo_ty_le_view(-chuan_hoa_vector_kieu_nguoc, line_combo_2, snap_dim_feet, current_view)

        for grid in all_grid:
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
                                all_ref.Append(ref_grid)
                                list_grid_ref.append(ref_grid)
            if len(list_grid_ref) > 0: #Dòng này thêm vào mục đích tránh cho việc dim thêm grid khác nữa.
                break
            

        type_of_ele = tung_beam.GetType()


        tc_trai = 0
        tc_phai = 0
        tc_bot = 0
        tc_top = 0
        if str(type_of_ele) == "Autodesk.Revit.DB.FamilyInstance":

            try:
                tc_top = nances.get_parameter_value_by_name(tung_beam, source_setting_family_beam[8])
            except:                
                # print("Top fukashi parameter name not found")
                pass
            
            try:
                tc_bot = nances.get_parameter_value_by_name(tung_beam, source_setting_family_beam[9])
            except:                
                # print("Bottom fukashi parameter name not found")
                pass
            
            try:
                tc_trai = nances.get_parameter_value_by_name(tung_beam, source_setting_family_beam[10])
            except:                
                # print("Left fukashi parameter name not found")
                pass
            
            try:
                tc_phai = nances.get_parameter_value_by_name(tung_beam, source_setting_family_beam[11])
            except:                
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

          
            # Trường hợp đã có sẵn tăng cường dầm rồi, dim 1 lần được 3 combo luôn.
            if not option_dim_only_combo_3:
                new_dim_combo_1 = doc.Create.NewDimension(current_view, line_combo_1, combo_ref_1)
                list_new_dim.append(new_dim_combo_1)
                new_dim_combo_2 = doc.Create.NewDimension(current_view, line_combo_2, combo_ref_2)
                list_new_dim.append(new_dim_combo_2)
                if float(tc_trai) > 0 or float(tc_phai) > 0:
                    new_dim_combo_3 = doc.Create.NewDimension(current_view, line_combo_3, combo_ref_3)
                    list_new_dim.append(new_dim_combo_3)

            # Trường hợp đã có sẵn tăng cường dầm rồi, dim 1 lần được 3 combo luôn.
            if option_dim_only_combo_3:   
                if float(tc_trai) > 0 or float(tc_phai) > 0:
                    new_dim_combo_3 = doc.Create.NewDimension(current_view, line_combo_3, combo_ref_3)
                    list_new_dim.append(new_dim_combo_3)


        # if is_section_elevation:

        #     la_phuong_ngang = vectortransform.co_phai_phuong_ngang_dai_khai(line, current_view)

        #     if la_phuong_ngang:
        #         if float(tc_trai) > 0:
        #             all_ref.Append(ref_trai)

        #         if float(tc_phai) > 0:
        #             all_ref.Append(ref_phai)
        #     else:
        #         if float(tc_top) > 0:
        #             all_ref.Append(ref_top)

        #         if float(tc_bot) > 0:
        #             all_ref.Append(ref_bot)


        select = uidoc.Selection
        listid = []

        for dim in list_new_dim:
            dim_id = dim.Id
            listid.append(dim_id)
        Icollection = List[ElementId](listid)
        select.SetElementIds(Icollection)
        
        t.Commit()

    trans_group.Assimilate()

#Sau khi chạy xong tool dim thì chạy tool auto move text dim type 1
if not option_dim_only_combo_3: #thêm điều kiện này cho trường hợp chưa thêm tăng cường mà chạy tool dim, không có dim thì tool Type 1 Auto sẽ bắt mình chọn dim.
    run_move_text_type_1 = uiapp.PostCommand(RevitCommandId.LookupCommandId("CustomCtrl_%CustomCtrl_%ARC drawing%Dimension%Type 1 Auto"))
if option_dim_only_combo_3:
    if float(tc_trai) > 0 or float(tc_phai) > 0:
        run_move_text_type_1 = uiapp.PostCommand(RevitCommandId.LookupCommandId("CustomCtrl_%CustomCtrl_%ARC drawing%Dimension%Type 1 Auto"))


