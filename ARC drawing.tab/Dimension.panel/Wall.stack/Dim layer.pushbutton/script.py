# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
import traceback
import math
import nances
from nances import vectortransform,geometry,selection, revit,visible

if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    current_view = doc.ActiveView

    def get_wall_width(wall):

        compound_structure = wall.WallType.GetCompoundStructure()

        core_width = 0.0
        exterior_width = 0.0
        interior_width = 0.0

        if compound_structure is not None:

            first_core_layer = (compound_structure.GetFirstCoreLayerIndex())

            last_core_layer = (compound_structure.GetLastCoreLayerIndex())

            # Core layers
            for i in range(first_core_layer,last_core_layer + 1): #lấy toàn bộ chiều dày của các layer trong core và cộng dồn lại bằng hàm +=

                core_width += (compound_structure.GetLayerWidth(i))

            # Các layer phía trước core
            for i in range(first_core_layer): #có nghĩa là range từ (0 cho đến ví dụ là 2)

                interior_width += (compound_structure.GetLayerWidth(i))

            # Các layer phía sau core
            for i in range(last_core_layer + 1,compound_structure.LayerCount):

                exterior_width += (compound_structure.GetLayerWidth(i))

        return core_width,interior_width,exterior_width

    def check_goc_cua_dam_tuong_so_voi_view_direction(element,view):
        view_direction = view.ViewDirection
        location_curve = element.Location.Curve
        start_point = location_curve.GetEndPoint(0)
        end_point = location_curve.GetEndPoint(1)
        location_line = DB.Line.CreateBound(start_point,end_point)
        location_line_direction = location_line.Direction
        xac_dinh_goc = vectortransform.angle_between_vectors(location_line_direction,view_direction)
        tri_tuyet_doi = abs(xac_dinh_goc)
        if (0 <= tri_tuyet_doi <= 1) or (179 <= tri_tuyet_doi <= 181):
            return True
        else: 
            return False

    def loc_grid_nam_ben_trong_dam_tuong(view,list_grids,element):
        center_plane = vectortransform.get_center_plane(element)
        center_plane_normal = center_plane.Normal
        chieu_rong = geometry.tinh_chieu_rong_dam(element)
        all_ref_grid = ReferenceArray()
        all_ref_grid.Clear()   
        ref_grid = None   
        for grid in list_grids:             
            list_grid_ref = []  
            get_hide_isolate = visible.check_hide_isolate(grid,view)
            get_hidden_element = visible.check_hidden(grid,view)
            if get_hide_isolate and get_hidden_element:
                geo_all_grid = geometry.get_all_geometry_of_grids(grid,view,DatumExtentType.ViewSpecific)
                for one_grid_curve in geo_all_grid:
                    for two_grid_curve in one_grid_curve:             
                        grid_plane = vectortransform.create_plane_follow_line_in_view(two_grid_curve,view)
                        check_pararel_beam_with_grid = vectortransform.are_planes_parallel(center_plane_normal,grid_plane.Normal)
                        if check_pararel_beam_with_grid:
                            distance_grid_with_beam =  abs(vectortransform.distance_between_parallel_planes(grid_plane, center_plane))
                            if distance_grid_with_beam < (chieu_rong/2):                        
                                ref_grid = Reference(grid)
                                all_ref_grid.Append(ref_grid)
                                list_grid_ref.append(ref_grid)
            if len(list_grid_ref) > 0: #Dòng này thêm vào mục đích tránh cho việc dim thêm grid khác nữa.
                break
        return all_ref_grid, ref_grid
    
    def get_wall_reference_string_by_magic(uid,index):
        format = "{0}:{1}:{2}"
        nine = -9999
        refString = str.Format(format,uid,nine,index)
        return refString

    def get_all_wall_reference_by_magic(idoc,uid,layer_count):
        format = "{0}:{1}:{2}"
        nine = -9999
        list_ref =[]
        for tung_index in range(1,layer_count+1):
            refString = str.Format(format,uid,nine,tung_index)
            ref = Reference.ParseFromStableRepresentation(idoc,refString)
            list_ref.append(ref)
        return list_ref

    def tao_cac_cap_reference(references):
        from itertools import combinations
        return list(combinations(references,2))

    def get_side_wall_reference (idoc, wall, shellLayerType):
        sideFaces = DB.HostObjectUtils.GetSideFaces(wall,shellLayerType)
        wallRef = sideFaces[0]
        return wallRef

    def tao_dim_tong_tuong (idoc, view, line_combo):

        wall_reference = ReferenceArray()

        get_wall_reference_exterior = get_side_wall_reference(doc, wall, ShellLayerType.Exterior)                
        get_wall_reference_interior = get_side_wall_reference(doc, wall, ShellLayerType.Interior)

        wall_reference.Append(get_wall_reference_exterior)
        wall_reference.Append(get_wall_reference_interior)
               
        with revit.Transaction('Tạo hàng loạt dim', swallow_errors=True):
            dim = idoc.Create.NewDimension(view, line_combo, wall_reference)

        return dim

    def tao_dim_chia_tam_tuong (idoc, view, line_combo,center_ref):

        wall_reference = ReferenceArray()

        get_wall_reference_exterior = get_side_wall_reference(doc, wall, ShellLayerType.Exterior)                
        get_wall_reference_interior = get_side_wall_reference(doc, wall, ShellLayerType.Interior)

        wall_reference.Append(center_ref)
        wall_reference.Append(get_wall_reference_exterior)
        wall_reference.Append(get_wall_reference_interior)
               
        with revit.Transaction('Tạo hàng loạt dim', swallow_errors=True):
            dim = idoc.Create.NewDimension(view, line_combo, wall_reference)

        return dim

    def tao_dim_layer_tuong (idoc, view, list_combo_reference, line_combo, wall_width):
              
        core_width = wall_width[0]

        interior_width = wall_width[1]

        exterior_width = wall_width[2]

        list_all_dim = []

        list_valid_dim = []
    
        count_dim_core = 0

        count_dim_interior = 0

        count_dim_exterior = 0
        
        for tung_cap_ref in list_combo_reference: 
            with revit.Transaction('Tạo hàng loạt dim', swallow_errors=True):
                wall_reference = ReferenceArray()
                wall_reference.Append(tung_cap_ref[0])
                wall_reference.Append(tung_cap_ref[1])

                dim = idoc.Create.NewDimension(view, line_combo, wall_reference)

                list_all_dim.append(dim)

                get_value_of_dim = dim.Value

                if count_dim_core == 0:
                    if round(core_width,3) == round(get_value_of_dim,3) and round(get_value_of_dim,3) > 0:                                
                        count_dim_core += 1
                        list_valid_dim.append(dim)
                        continue
                if count_dim_interior == 0:
                    if round(interior_width,3) == round(get_value_of_dim,3) and round(get_value_of_dim,3) > 0:                              
                        count_dim_interior += 1
                        list_valid_dim.append(dim)
                        continue                                                  

                if count_dim_exterior == 0:
                    if round(exterior_width,3) == round(get_value_of_dim,3) and round(get_value_of_dim,3) > 0:                              
                        count_dim_exterior += 1
                        list_valid_dim.append(dim)
                        continue      
                            
        new_list_valid_dim = []

        with revit.Transaction('Xoá dim không khả dụng', swallow_errors=True):                            
            for tung_dim in list_all_dim:
                if tung_dim not in list_valid_dim:
                    idoc.Delete(tung_dim.Id)
                else:
                    new_list_valid_dim.append(tung_dim)

        list_ref = []
        list_ref_string = []

        for tung_dim_kha_di in new_list_valid_dim:
            references = tung_dim_kha_di.References

            for tung_ref in references:
                ref_string = tung_ref.ConvertToStableRepresentation(doc)

                if ref_string not in list_ref_string:
                    list_ref.append(tung_ref)
                    list_ref_string.append(ref_string)

        new_wall_reference = ReferenceArray()

        for tung_ref_lan_2 in list_ref:
            new_wall_reference.Append(tung_ref_lan_2)
        with revit.Transaction('Tạo lại dim gộp những dim lẻ khả dụng', swallow_errors=True):  
            dim = idoc.Create.NewDimension(current_view, line_combo, new_wall_reference) 

        with revit.Transaction('Xoá dim riêng lẻ trước đó', swallow_errors=True):  
            for tung_dim_kha_di in new_list_valid_dim:
                idoc.Delete(tung_dim_kha_di.Id)    
        return dim

    def check_goc_cua_dam_so_voi_view_direction(dam,view):
        view_direction = view.ViewDirection
        location_curve = dam.Location.Curve
        start_point = location_curve.GetEndPoint(0)
        end_point = location_curve.GetEndPoint(1)
        location_line = DB.Line.CreateBound(start_point,end_point)
        location_line_direction = location_line.Direction
        xac_dinh_goc = vectortransform.angle_between_vectors(location_line_direction,view_direction)
        tri_tuyet_doi = abs(xac_dinh_goc)
        if (0 <= tri_tuyet_doi <= 1) or (179 <= tri_tuyet_doi <= 181):
            return True
        else: 
            return False

    Ele = nances.get_elements(uidoc,doc, "Select Walls", noti = False)

    trans_group = TransactionGroup(doc, 'Dim kich thuoc tuong')
    trans_group.Start()

    is_legend = current_view.ViewType == ViewType.Legend
    is_plan_view = current_view.ViewType in [ViewType.FloorPlan, ViewType.CeilingPlan, ViewType.EngineeringPlan, ViewType.AreaPlan ]
    is_section_elevation = current_view.ViewType in [ViewType.Section, ViewType.Elevation]

    all_grid = selection.get_all_grid(doc,current_view)

    if Ele:
        list_new_dim = []
        for wall in Ele:
            try:                
                unique_id = wall.UniqueId

                chieu_rong = geometry.tinh_chieu_rong_dam(wall)
                center_plane = vectortransform.get_center_plane(wall)
                center_plane_normal = center_plane.Normal

                call_def_get_all_ref_grid= loc_grid_nam_ben_trong_dam_tuong(current_view,all_grid,wall)
                all_ref = call_def_get_all_ref_grid[0]
                ref_grid = call_def_get_all_ref_grid[1]
                   
                string_face_center_core = get_wall_reference_string_by_magic(unique_id,4) #Co ve -9999 va id 4 luon luon la tam tuong

                ref_center_core_wall = Reference.ParseFromStableRepresentation(doc,string_face_center_core) 

                ref_core = ref_center_core_wall

                try:
                    for check_ref_grid in all_ref:
                        if check_ref_grid == ref_grid:
                            ref_core = check_ref_grid
                except:
                    pass
                
                wall_width =  get_wall_width(wall)

                core_width = wall_width[0]

                interior_width = wall_width[1]

                exterior_width = wall_width[2]

                location_line = wall.Location.Curve

                #Thông thường parameter "Dimension Line Snap Distance" có giá trị là 5mm

                snap_dim_mm = 5 #tính bằng mm
                
                snap_dim_feet = snap_dim_mm  / 304.8  #tính bằng feet

                get_all_ref_wall = get_all_wall_reference_by_magic(doc,unique_id,7) 

                list_combo_reference = tao_cac_cap_reference(get_all_ref_wall)

                list_all_dim = []

                list_valid_dim = []
            
                count_dim_core = 0

                count_dim_interior = 0

                count_dim_exterior = 0

                if is_plan_view:      
                    flat_location_line = vectortransform.project_line_to_plane (location_line, current_view) 

                    flat_location_line_direction = flat_location_line.Direction

                    chuan_hoa_vector_kieu_nguoc = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_tren_xuong_duoi(flat_location_line_direction,current_view)          

                    line_combo_2 = vectortransform.get_rotate_90_location_line(location_line,current_view)
                    
                    line_combo_1 = vectortransform.move_line_theo_vector_theo_ty_le_view(chuan_hoa_vector_kieu_nguoc, line_combo_2, snap_dim_feet, current_view)

                    line_combo_3 = vectortransform.move_line_theo_vector_theo_ty_le_view(chuan_hoa_vector_kieu_nguoc, line_combo_2, -snap_dim_feet, current_view)

                    if exterior_width !=0 or interior_width != 0:

                        dim_layer_tren_mat_bang = tao_dim_layer_tuong (doc, current_view, list_combo_reference, line_combo_1, wall_width)
                        list_new_dim.append(dim_layer_tren_mat_bang)

                    dim_center_tren_mat_bang = tao_dim_chia_tam_tuong (doc,current_view,line_combo_2,ref_core)
                    list_new_dim.append(dim_center_tren_mat_bang)

                    dim_tong_tren_mat_bang = tao_dim_tong_tuong (doc, current_view, line_combo_3)
                    list_new_dim.append(dim_tong_tren_mat_bang)

                if is_section_elevation:

                    if check_goc_cua_dam_so_voi_view_direction(wall,current_view): #phòng trường hợp dim dầm nhìn thấy theo phương song song với mặt cắt mà cũng dim vào. dễ gây ra lỗi
                
                        view_scale = current_view.Scale

                        right_direction = current_view.RightDirection

                        up_direction = current_view.UpDirection
                        
                        trung_diem = geometry.tinh_diem_trung_tam_bounding_box(wall)

                        plane_man_hinh = vectortransform.tao_plane_man_hinh (current_view)

                        giong_len_plane_cua_view = vectortransform.project_point_to_plane_by_view(trung_diem, plane_man_hinh, current_view)

                        move_point_qua_phai = vectortransform.move_point_along_vector(giong_len_plane_cua_view, right_direction, 1)

                        line_ngang_ngay_tam = DB.Line.CreateBound(giong_len_plane_cua_view,move_point_qua_phai)
                        
                        move_point_len_tren = vectortransform.move_point_along_vector(giong_len_plane_cua_view, up_direction, 1)

                        line_doc_ngay_tam = DB.Line.CreateBound(giong_len_plane_cua_view,move_point_len_tren)

                        chieu_cao_tuong = geometry.tinh_chieu_cao_dam(wall)

                        offset_tinh_tu_base_tuong = 1000/304.8
                        
                        tinh_toan_offset_tinh_tu_mat_dam_phuong_chieu_cao = ((chieu_cao_tuong/2) - offset_tinh_tu_base_tuong) / view_scale #chia trước cho scale vì def move_line_theo_vector_theo_ty_le_view nhân scale lên lại.

                        line_combo_C =  vectortransform.move_line_theo_vector_theo_ty_le_view(-up_direction , line_ngang_ngay_tam, tinh_toan_offset_tinh_tu_mat_dam_phuong_chieu_cao, current_view)
                        
                        line_combo_B =  vectortransform.move_line_theo_vector_theo_ty_le_view(-up_direction, line_combo_C, snap_dim_feet, current_view)

                        line_combo_A =  vectortransform.move_line_theo_vector_theo_ty_le_view(-up_direction, line_combo_B, snap_dim_feet, current_view)

                        if exterior_width !=0 or interior_width != 0:

                            dim_layer_tren_mat_cat = tao_dim_layer_tuong (doc, current_view, list_combo_reference, line_combo_A, wall_width)
                            list_new_dim.append(dim_layer_tren_mat_cat)

                        dim_center_tren_mat_cat = tao_dim_chia_tam_tuong (doc,current_view,line_combo_B,ref_core)
                        list_new_dim.append(dim_center_tren_mat_cat)

                        dim_tong_tren_mat_cat = tao_dim_tong_tuong (doc, current_view, line_combo_C)

                        list_new_dim.append(dim_tong_tren_mat_cat)    

                        # with revit.Transaction('nhập tên transaction', swallow_errors=True):
                        #     detail_curve_of_location_curve = doc.Create.NewDetailCurve(current_view,line_ngang_ngay_tam)            
            except:
                # print(traceback.format_exc())
                pass
        #Select tat ca dim moi, dung de chay tool sua text dim    
        try:
            nances.selection.select_sau_khi_chay_tool (list_new_dim,uidoc)
        except:
            pass
        
    trans_group.Assimilate()