# -*- coding: utf-8 -*-
import Autodesk
import nances
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit import script
from nances import geometry,vectortransform,selection,allinone, visible
import setup_family_beam_config #cần import dòng này, đây là tên của script config
import traceback
import math

def get_family_name (element):
    param = nances.get_builtin_parameter_by_name(element, DB.BuiltInParameter.ELEM_FAMILY_PARAM)
    value = param.AsValueString()
    return value

def loc_grid_nam_ben_trong_dam(grids):
    for grid in grids:
        list_grid_ref = []
        get_hide_isolate = visible.check_hide_isolate(current_view, grid)
        get_hidden_element = visible.check_hidden(grid,current_view)
        if get_hide_isolate and get_hidden_element:
            geo_all_grid = geometry.get_all_geometry_of_grids(grid, DatumExtentType)
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

def check_is_max_bounding_box_with_host_level (element,level):
    try:
        bounding_box = element.get_BoundingBox(None)
        max_pt = bounding_box.Max
        z_point_max = max_pt.Z
        if round(level.Elevation,3) == round(z_point_max,3):
            return True
        else:
            return False
    except:
        return True

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

def set_work_plane(uidoc):
    import nances
    current_view = uidoc.ActiveView
    try:
        nances.set_work_plane_for_view(current_view)
    except:
        pass


def get_reference_by_name_in_family (instance, name):
    ref = instance.GetReferenceByName(name)
    return ref

logger = script.get_logger()

my_config = script.get_config()

source_setting_family_beam = setup_family_beam_config.load_configs_setup_family()

source_setting_dim_in_need_in_plan_view = setup_family_beam_config.load_configs_setup_dim_in_need_in_plan_view()

source_setting_dim_in_need_in_section_view = setup_family_beam_config.load_configs_setup_dim_in_need_in_section_view()

source_setting_type_dim_in_section_view = setup_family_beam_config.load_configs_setup_type_dim_in_section_view()

if nances.AutodeskData():
    uiapp = __revit__
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document

    current_view = uidoc.ActiveView
    is_legend = current_view.ViewType == ViewType.Legend
    is_plan_view = current_view.ViewType in [ViewType.FloorPlan, ViewType.CeilingPlan, ViewType.EngineeringPlan, ViewType.AreaPlan ]
    is_section_elevation = current_view.ViewType in [ViewType.Section, ViewType.Elevation]

    option_dim_combo_3 = source_setting_dim_in_need_in_plan_view[0]
    option_dim_combo_2 = source_setting_dim_in_need_in_plan_view[1]
    option_dim_combo_1 = source_setting_dim_in_need_in_plan_view[2]

    option_dim_combo_A = source_setting_dim_in_need_in_section_view[0]
    option_dim_combo_B = source_setting_dim_in_need_in_section_view[1]
    option_dim_combo_C = source_setting_dim_in_need_in_section_view[2]
    option_dim_combo_D = source_setting_dim_in_need_in_section_view[3]
    option_dim_combo_E = source_setting_dim_in_need_in_section_view[4]

    option_type_1 = source_setting_type_dim_in_section_view[0]
    option_type_2 = source_setting_type_dim_in_section_view[1]

    Ele = nances.get_elements(uidoc,doc, 'Select Beams', noti = False)

    list_new_dim =[]
    list_dim_need_modify_text = []

    all_grid = selection.get_all_grid(doc,current_view)

    trans_group = TransactionGroup(doc, 'Dimension beam_new version')
    trans_group.Start()

    list_error = []

    try:
        t1 = Transaction(doc, 'Set work plane')
        t1.Start()
        set_work_plane(uidoc)
        t1.Commit()
    except Exception as e:
        print(e)
        pass
    
    for tung_beam in Ele:
        try: 
            all_ref = ReferenceArray()
            ref_beam = Reference(tung_beam)
            combo_ref_1 = ReferenceArray()
            combo_ref_2 = ReferenceArray()
            combo_ref_3 = ReferenceArray()

            #ref theo mat cat
            combo_ref_A = ReferenceArray()
            combo_ref_B = ReferenceArray()
            combo_ref_C = ReferenceArray()
            combo_ref_D_type_1 = ReferenceArray()
            combo_ref_D_type_2 = ReferenceArray()
            combo_ref_E_type_1 = ReferenceArray()
            combo_ref_E_type_2 = ReferenceArray()

            all_ref.Clear()

            center_plane = vectortransform.get_center_plane(tung_beam)
            center_plane_normal = center_plane.Normal

            chieu_rong = geometry.tinh_chieu_rong_dam(tung_beam)

            location_line = tung_beam.Location.Curve

            #Thông thường parameter "Dimension Line Snap Distance" có giá trị là 5mm
            snap_dim_mm = 5 #tính bằng mm
            
            snap_dim_feet = snap_dim_mm  / 304.8  #tính bằng feet

            for grid in all_grid:
                list_grid_ref = []
                get_hide_isolate = visible.check_hide_isolate(grid, current_view)
                get_hidden_element = visible.check_hidden(grid,current_view)

                if get_hide_isolate and get_hidden_element:
                    geo_all_grid = geometry.get_all_geometry_of_grids(grid, current_view, DatumExtentType)
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

                flat_location_line = vectortransform.project_line_to_plane (location_line, current_view) 

                flat_location_line_direction = flat_location_line.Direction

                chuan_hoa_vector_kieu_nguoc = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_tren_xuong_duoi(flat_location_line_direction,current_view)

                line_combo_2 = vectortransform.get_rotate_90_location_line(location_line,current_view)
                
                line_combo_1 = vectortransform.move_line_theo_vector_theo_ty_le_view(chuan_hoa_vector_kieu_nguoc, line_combo_2, snap_dim_feet, current_view)

                line_combo_3 = vectortransform.move_line_theo_vector_theo_ty_le_view(-chuan_hoa_vector_kieu_nguoc, line_combo_2, snap_dim_feet, current_view)
            
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
                    list_error.append(get_family_name(tung_beam) + ": " +"Top fukashi parameter name not found")                
                    # print("Top fukashi parameter name not found")
                    pass
                
                try:
                    tc_bot = nances.get_parameter_value_by_name(tung_beam, source_setting_family_beam[9])
                except:
                    list_error.append(get_family_name(tung_beam) + ": " "Bottom fukashi parameter name not found")             
                    # print("Bottom fukashi parameter name not found")
                    pass
                
                try:
                    tc_trai = nances.get_parameter_value_by_name(tung_beam, source_setting_family_beam[10])
                except: 
                    list_error.append(get_family_name(tung_beam) + ": " "Left fukashi parameter name not found")             
                    # print("Left fukashi parameter name not found")
                    pass
                
                try:
                    tc_phai = nances.get_parameter_value_by_name(tung_beam, source_setting_family_beam[11])
                except:
                    list_error.append(get_family_name(tung_beam) + ": " "Right fukashi parameter name not found")                     
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

                cross_angle = nances.get_builtin_parameter_by_name(tung_beam,BuiltInParameter.STRUCTURAL_BEND_DIR_ANGLE)

                value_cross_angle = cross_angle.AsDouble()

                if value_cross_angle > -0.001 and value_cross_angle < 0.001:
                    try:
                        t = Transaction(doc,"Dim beam")
                        t.Start() 
                        # Trường hợp đã có sẵn tăng cường dầm rồi, dim 1 lần được 3 combo luôn.
                        if  option_dim_combo_1:
                            new_dim_combo_1 = doc.Create.NewDimension(current_view, line_combo_1, combo_ref_1)
                            list_new_dim.append(new_dim_combo_1)
                            list_dim_need_modify_text.append(new_dim_combo_1)
                        if option_dim_combo_2:
                            new_dim_combo_2 = doc.Create.NewDimension(current_view, line_combo_2, combo_ref_2)

                            list_new_dim.append(new_dim_combo_2)
                            list_dim_need_modify_text.append(new_dim_combo_2)

                        if option_dim_combo_3:    
                            if float(tc_trai) > 0 or float(tc_phai) > 0:
                                new_dim_combo_3 = doc.Create.NewDimension(current_view, line_combo_3, combo_ref_3)
                                list_new_dim.append(new_dim_combo_3)
                                list_dim_need_modify_text.append(new_dim_combo_3)
                        t.Commit()
                    except Exception as e:
                        t.RollBack()
                        list_error.append(str(e))
                        pass
                        
                        
            if is_section_elevation:
                
                view_scale = current_view.Scale

                right_direction = current_view.RightDirection

                up_direction = current_view.UpDirection
                
                trung_diem = geometry.tinh_diem_trung_tam_bounding_box(tung_beam)

                plane_man_hinh = vectortransform.tao_plane_man_hinh (current_view)

                giong_len_plane_cua_view = vectortransform.project_point_to_plane_by_view(trung_diem, plane_man_hinh, current_view)

                move_point_qua_phai = vectortransform.move_point_along_vector(giong_len_plane_cua_view, right_direction, 1)

                line_ngang_ngay_tam = DB.Line.CreateBound(giong_len_plane_cua_view,move_point_qua_phai)
                
                move_point_len_tren = vectortransform.move_point_along_vector(giong_len_plane_cua_view, up_direction, 1)

                line_doc_ngay_tam = DB.Line.CreateBound(giong_len_plane_cua_view,move_point_len_tren)

                chieu_cao_dam = geometry.tinh_chieu_cao_dam(tung_beam)
                
                #Line dim phương ngang
                #Thêm hàm để so sánh cao độ dầm so với level. Thông thường dầm dưới 1F thì là dầm móng. Còn dầm trên 1F là dầm thường.
                # if 0 > giong_len_plane_cua_view.Z: #không dùng cách này nữa vì đôi khi dầm 1F không phải dầm móng mà dim cũng kì
                if chieu_cao_dam * 304.8  > 1600:   #Dùng cách nếu dầm cao hơn 1600 (gồm cả tăng cường thì coi như đó là dầm móng, phương pháp này cũng hên xui)
                    line_combo_C = line_ngang_ngay_tam  
                else:
                    tinh_toan_offset_tinh_tu_mat_dam_phuong_chieu_cao = (chieu_cao_dam/2 + 450/304.8) / view_scale #chia trước cho scale vì def move_line_theo_vector_theo_ty_le_view nhân scale lên lại.
                    line_combo_C =  vectortransform.move_line_theo_vector_theo_ty_le_view(-up_direction , line_ngang_ngay_tam, tinh_toan_offset_tinh_tu_mat_dam_phuong_chieu_cao, current_view)
                
                line_combo_B =  vectortransform.move_line_theo_vector_theo_ty_le_view(-up_direction, line_combo_C, snap_dim_feet, current_view)

                line_combo_A =  vectortransform.move_line_theo_vector_theo_ty_le_view(-up_direction, line_combo_B, snap_dim_feet, current_view)

                #Line dim phương dọc
                
                tinh_toan_offset_tinh_tu_mat_dam_theo_chieu_rong = (chieu_rong/2 + 600/304.8) / view_scale #chia trước cho scale vì def move_line_theo_vector_theo_ty_le_view nhân scale lên lại.
                
                line_combo_E =  vectortransform.move_line_theo_vector_theo_ty_le_view(right_direction , line_doc_ngay_tam, tinh_toan_offset_tinh_tu_mat_dam_theo_chieu_rong, current_view)

                line_combo_D =  vectortransform.move_line_theo_vector_theo_ty_le_view(right_direction , line_combo_E, snap_dim_feet, current_view)
                
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

                #Combo D 1_dim tăng cường
                combo_ref_D_type_1.Append(ref_fukashi_bot)
                if not check_is_max_bounding_box_with_host_level (tung_beam,host_level):
                    combo_ref_D_type_1.Append(ref_fukashi_top)      
                combo_ref_D_type_1.Append(Reference(host_level))

                #Combo E_1 dim tăng cường
                combo_ref_E_type_1.Append(ref_fukashi_bot)
                combo_ref_E_type_1.Append(ref_fukashi_top) 
                if float(tc_top) > 0:
                    combo_ref_E_type_1.Append(ref_top)
                if float(tc_bot) > 0:
                    combo_ref_E_type_1.Append(ref_bot)        

                #Combo D_dim tăng cường
                combo_ref_D_type_2.Append(ref_fukashi_bot)
                combo_ref_D_type_2.Append(Reference(host_level))

                #Combo E_dim tăng cường
                combo_ref_E_type_2.Append(ref_fukashi_bot)
                if not check_is_max_bounding_box_with_host_level (tung_beam,host_level):
                    combo_ref_E_type_2.Append(ref_top) 
                combo_ref_E_type_2.Append(Reference(host_level))

                if float(tc_bot) > 0:
                    combo_ref_E_type_2.Append(ref_bot)            

                t = Transaction(doc,"Dim beam in section")
                t.Start() 
                try:
                    
                    if check_goc_cua_dam_so_voi_view_direction(tung_beam,current_view): #phòng trường hợp dim dầm nhìn thấy theo phương song song với mặt cắt mà cũng dim vào. dễ gây ra lỗi
                        if option_dim_combo_C:
                            if float(tc_trai) > 0 or float(tc_phai) > 0:
                                new_dim_combo_C = doc.Create.NewDimension(current_view, line_combo_C, combo_ref_C)
                                list_new_dim.append(new_dim_combo_C)
                                list_dim_need_modify_text.append(new_dim_combo_C)

                        if option_dim_combo_B:
                            
                                new_dim_combo_B = doc.Create.NewDimension(current_view, line_combo_B, combo_ref_B)
                                list_new_dim.append(new_dim_combo_B)
                                list_dim_need_modify_text.append(new_dim_combo_B)

                        if option_dim_combo_A:
                            new_dim_combo_A = doc.Create.NewDimension(current_view, line_combo_A, combo_ref_A)
                            list_new_dim.append(new_dim_combo_A)

                    if option_dim_combo_D:
                        if option_type_1:
                            new_dim_combo_D = doc.Create.NewDimension(current_view, line_combo_D, combo_ref_D_type_1)
                            list_new_dim.append(new_dim_combo_D)
                        elif option_type_2:
                            new_dim_combo_D = doc.Create.NewDimension(current_view, line_combo_D, combo_ref_D_type_2)
                            list_new_dim.append(new_dim_combo_D)

                    if option_dim_combo_E:
                        if option_type_1:
                            new_dim_combo_E = doc.Create.NewDimension(current_view, line_combo_E, combo_ref_E_type_1)
                            list_new_dim.append(new_dim_combo_E)

                        elif option_type_2:
                            new_dim_combo_E = doc.Create.NewDimension(current_view, line_combo_E, combo_ref_E_type_2)
                            list_new_dim.append(new_dim_combo_E)

                    t.Commit()

                #     detail_curve_of_location_curve = doc.Create.NewDetailCurve(current_view,line_combo_C)
                except:                
                    pass
                    t.RollBack()
        except Exception as e:
            pass
            if hasattr(tung_beam,"Category"):
                if hasattr(tung_beam.Category,"Name"):
                    print (str(tung_beam.Category.Name) + ":" + str(e))
            else:
                print (str(e))
            
    set_error = list(set(list_error))
    if len(set_error) > 0:
        output = script.get_output()
        logger = script.get_logger()
        logger.warning("Please hold Shift and click to the tool to setup input family.\nHãy giữ nút shift và bấm vào tool để setting lại input")
        for tung_loi in set_error:
            print (tung_loi)                          
    if len(list_dim_need_modify_text) > 0 :
        # run_move_text_type_1 = uiapp.PostCommand(RevitCommandId.LookupCommandId("CustomCtrl_%CustomCtrl_%ARC drawing%Dimension%Type 1 Auto"))
        for tung_dim in list_dim_need_modify_text:
            try:
                from pyrevit import revit
                with revit.Transaction('Move text dim auto', swallow_errors=True):

                    view_direction = current_view.ViewDirection

                    dim_line = tung_dim.Curve

                    vector_of_dim = dim_line.Direction

                    vector_da_chuan_hoa = allinone.chuan_hoa_vector(vector_of_dim, current_view)

                    all_segment_position = allinone.get_all_segment_position(tung_dim)

                    diem_trung_binh = allinone.get_average_point(all_segment_position)

                    return_point_chinh_giua = vectortransform.move_point_along_vector(diem_trung_binh, vector_da_chuan_hoa, 0.01)

                    number_of_segments =  tung_dim.NumberOfSegments

                    if number_of_segments == 3:

                        allinone.move_text_dim_type_1_auto (tung_dim, current_view, return_point_chinh_giua, kich_co_chu = 1.8)    

                    if number_of_segments == 2:

                        tinh_toan = allinone.tinh_toan_can_thiet_move_text_dim_2_seg (tung_dim,return_point_chinh_giua, vector_da_chuan_hoa, current_view)  #0 là segment bên phải, 1 là segment bên phải

                        if tinh_toan[0] and tinh_toan[1]: #0 là segment bên phải, 1 là segment bên phải
                            
                            allinone.move_text_dim_type_1_auto (tung_dim, current_view, return_point_chinh_giua, kich_co_chu = 1.8)   

                        if tinh_toan[0] and not tinh_toan [1]: #0 là segment bên phải, 1 là segment bên phải

                            return_point_lech = vectortransform.move_point_along_vector(diem_trung_binh, vector_da_chuan_hoa, 5)

                            allinone.move_text_dim_type_1_auto (tung_dim, current_view, return_point_lech, kich_co_chu = 1.8)   

                        if not tinh_toan [0] and tinh_toan[1]: #0 là segment bên phải, 1 là segment bên phải

                            return_point_lech = vectortransform.move_point_along_vector(diem_trung_binh, vector_da_chuan_hoa, -5)

                            allinone.move_text_dim_type_1_auto (tung_dim, current_view, return_point_lech, kich_co_chu = 1.8)   
                    

            except Exception as e:
                print(traceback.format_exc())
                pass
    try:
        selection.select_sau_khi_chay_tool(list_new_dim,uidoc)
    except:
        pass
    trans_group.Assimilate() 
