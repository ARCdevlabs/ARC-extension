# -*- coding: utf-8 -*-
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
from pyrevit import revit,script
import nances
from nances import geometry
from nances import vectortransform, allinone,selection, visible,create
from Autodesk.Revit.DB import *
import tim_reference_column
import traceback
import setup_family_column_config #cần import dòng này, đây là tên của script config

if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    current_view = doc.ActiveView
    view_scale = current_view.Scale
    Curve = []

    def get_reference_by_name_in_family (instance, name):
        ref = instance.GetReferenceByName(name)
        return ref
    
    def get_reference_by_center_in_family (instance):
        list_ref_front_back_ref = instance.GetReferences(FamilyInstanceReferenceType.CenterFrontBack)
        list_ref_left_right_ref = instance.GetReferences(FamilyInstanceReferenceType.CenterLeftRight)
        for tung_ref_front_back in list_ref_front_back_ref:
            front_back_ref = tung_ref_front_back
        for tung_ref_left_right in list_ref_left_right_ref:
            left_right_ref = tung_ref_left_right
        return front_back_ref,left_right_ref
    
    def set_work_plane(uidoc):
        import nances
        current_view = uidoc.ActiveView
        try:
            nances.set_work_plane_for_view(current_view)
        except:
            pass
        
    def get_family_name (element):
        param = nances.get_builtin_parameter_by_name(element, DB.BuiltInParameter.ELEM_FAMILY_PARAM)
        value = param.AsValueString()
        return value
    
    logger = script.get_logger()

    my_config = script.get_config()

    source_setting_family_column = setup_family_column_config.load_configs_setup_family()

    source_setting_dim_in_need_in_plan_view = setup_family_column_config.load_configs_setup_dim_in_need_in_plan_view()

    source_setting_position_of_dim = setup_family_column_config.load_configs_setup_position_of_dim()

    source_offset_of_dim = setup_family_column_config.load_configs_setup_offset_dim()

    Ele = nances.get_elements(uidoc,doc, "Select Columns", noti = False)

    all_grid = selection.get_all_grid(doc,current_view)
    
    is_plan_view = current_view.ViewType in [ViewType.FloorPlan, ViewType.CeilingPlan, ViewType.EngineeringPlan, ViewType.AreaPlan ]

    is_section_elevation = current_view.ViewType in [ViewType.Section, ViewType.Elevation]

    list_new_dim = []
    list_dim_need_modify_text_top = []
    list_dim_need_modify_text_right = []

    list_error = []

    option_dim_combo_3 = source_setting_dim_in_need_in_plan_view[0]
    option_dim_combo_2 = source_setting_dim_in_need_in_plan_view[1]
    option_dim_combo_1 = source_setting_dim_in_need_in_plan_view[2]

    option_top_left = source_setting_position_of_dim[0]
    option_top_right = source_setting_position_of_dim[1]
    option_bot_left = source_setting_position_of_dim[2]
    option_bot_right = source_setting_position_of_dim[3]

    offset_of_dim = float(source_offset_of_dim[0])

    trans_group = TransactionGroup(doc, 'Dim column with fukashi')
    trans_group.Start()

    t1 = Transaction(doc, 'Set work plane')
    t1.Start()
    set_work_plane(uidoc)
    t1.Commit()


    if Ele:
        with revit.Transaction("Dim column with fukashi", swallow_errors=True):

            for tung_column in Ele:
                try:
                    try:
                        front_back_ref = (get_reference_by_center_in_family (tung_column))[0]
                    except:
                        list_error.append(get_family_name(tung_column) + ": " +"Invalid front/back center reference")
                        pass
                    try:
                        left_right_ref = (get_reference_by_center_in_family (tung_column))[1]
                    except:
                        list_error.append(get_family_name(tung_column) + ": " +"Invalid left/right center reference")
                        pass

                    point_location = tung_column.Location.Point

                    X_vector_chua_chuan_hoa = vectortransform.get_X_vector(tung_column)

                    Y_vector_chua_chuan_hoa = vectortransform.get_Y_vector(tung_column)

                    X_vector = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_tren_xuong_duoi(X_vector_chua_chuan_hoa,current_view)

                    Y_vector = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_tren_xuong_duoi(Y_vector_chua_chuan_hoa,current_view)

                    Y_plane = Plane.CreateByNormalAndOrigin(X_vector, point_location)

                    X_plane = Plane.CreateByNormalAndOrigin(Y_vector, point_location)

                    all_ref_top = ReferenceArray()
                    combo_ref_top_1 = ReferenceArray()
                    combo_ref_top_2 = ReferenceArray()
                    combo_ref_top_3 = ReferenceArray()

                    all_ref_right = ReferenceArray()
                    combo_ref_right_1 = ReferenceArray()
                    combo_ref_right_2 = ReferenceArray()
                    combo_ref_right_3 = ReferenceArray()

                    chieu_rong = geometry.tinh_chieu_rong_cot(tung_column, Y_vector)

                    chieu_cao = geometry.tinh_chieu_rong_cot(tung_column, X_vector)
                    
                    #Thông thường parameter "Dimension Line Snap Distance" có giá trị là 5mm
                    snap_dim_mm = 5 #tính bằng mm
                    
                    snap_dim_feet = snap_dim_mm  / 304.8  #tính bằng feet
                   
                    for grid_Y in all_grid:

                        list_grid_ref_top_2 = []

                        geo_all_grid = geometry.get_all_geometry_of_grids(grid_Y,current_view, DatumExtentType = DatumExtentType.ViewSpecific)
                    
                        for one_grid_curve in geo_all_grid:

                            for two_grid_curve in one_grid_curve:

                                grid_plane_Y = vectortransform.create_plane_follow_line(two_grid_curve)

                                check_pararel_beam_with_grid = vectortransform.are_planes_parallel(X_vector,grid_plane_Y.Normal)

                                if check_pararel_beam_with_grid:

                                    distance_grid_with_beam =  abs(vectortransform.distance_between_parallel_planes(grid_plane_Y, Y_plane))

                                    if distance_grid_with_beam < chieu_rong / 2:

                                        ref_grid_Y = Reference(grid_Y)

                                        all_ref_top.Append(ref_grid_Y)

                                        list_grid_ref_top_2.append(ref_grid_Y)


                        if len(list_grid_ref_top_2) > 0:
                            break

                    for grid_X in all_grid:

                        list_grid_ref_right = []

                        geo_all_grid_X = geometry.get_all_geometry_of_grids(grid_X, current_view, DatumExtentType = DatumExtentType.ViewSpecific)

                        for one_grid_curve_X in geo_all_grid_X:

                            for two_grid_curve_X in one_grid_curve_X:

                                grid_plane_X = vectortransform.create_plane_follow_line(two_grid_curve_X)

                                check_pararel_beam_with_grid_X = vectortransform.are_planes_parallel(Y_vector,grid_plane_X.Normal)

                                if check_pararel_beam_with_grid_X:

                                    distance_grid_with_beam_X =  abs(vectortransform.distance_between_parallel_planes(grid_plane_X, X_plane))

                                    if distance_grid_with_beam_X < chieu_cao / 2:

                                        ref_grid_X = Reference(grid_X)

                                        all_ref_right.Append(ref_grid_X)

                                        list_grid_ref_right.append(grid_X)

                        if len(list_grid_ref_right) > 0:

                            break

                    if is_plan_view:

                        try:

                            #Quy ước line top là line song song với vector X, line right là line song song với vector Y

                            line_ngang_center = vectortransform.line_for_dim_X(tung_column,current_view)

                            tong_hop_line_bot = vectortransform.tinh_toan_line_dim_cot_1_2_3 (line_ngang_center,Y_vector,chieu_cao/2, offset_of_dim, current_view)

                            line_bot_3 = tong_hop_line_bot[0]

                            line_bot_2 = tong_hop_line_bot[1]

                            line_bot_1 = tong_hop_line_bot[2]

                            line_doc_center = vectortransform.line_for_dim_Y(tung_column,current_view)

                            tong_hop_line_right = vectortransform.tinh_toan_line_dim_cot_1_2_3 (line_doc_center,X_vector,chieu_rong/2,offset_of_dim, current_view)

                            line_right_3 = tong_hop_line_right[0]

                            line_right_2 = tong_hop_line_right[1]

                            line_right_1 = tong_hop_line_right[2]
                            
                            tong_hop_line_top = vectortransform.tinh_toan_line_dim_cot_1_2_3 (line_ngang_center,-Y_vector,chieu_cao/2, offset_of_dim,current_view)

                            line_top_3 = tong_hop_line_top[0]

                            line_top_2 = tong_hop_line_top[1]

                            line_top_1 = tong_hop_line_top[2]

                            tong_hop_line_left = vectortransform.tinh_toan_line_dim_cot_1_2_3 (line_doc_center,-X_vector,chieu_rong/2, offset_of_dim, current_view)

                            line_left_3 = tong_hop_line_left[0]

                            line_left_2 = tong_hop_line_left[1]

                            line_left_1 = tong_hop_line_left[2]

                            if option_top_left:
                                line_ngang_1 = line_top_1
                                line_ngang_2 = line_top_2
                                line_ngang_3 = line_top_3

                                line_doc_1 = line_left_1
                                line_doc_2 = line_left_2
                                line_doc_3 = line_left_3

                            elif option_top_right:
                                line_ngang_1 = line_top_1
                                line_ngang_2 = line_top_2
                                line_ngang_3 = line_top_3

                                line_doc_1 = line_right_1
                                line_doc_2 = line_right_2
                                line_doc_3 = line_right_3

                            elif option_bot_left:
                                line_ngang_1 = line_bot_1
                                line_ngang_2 = line_bot_2
                                line_ngang_3 = line_bot_3

                                line_doc_1 = line_left_1
                                line_doc_2 = line_left_2
                                line_doc_3 = line_left_3

                            elif option_bot_right:
                                line_ngang_1 = line_bot_1
                                line_ngang_2 = line_bot_2
                                line_ngang_3 = line_bot_3

                                line_doc_1 = line_right_1
                                line_doc_2 = line_right_2
                                line_doc_3 = line_right_3                           
                        except:
                            # print(traceback.format_exc())
                            pass
                    # create.detail_line(doc, current_view, line_top_3)
                    # create.detail_line(doc, current_view, line_top_2)
                    # create.detail_line(doc, current_view, line_top_1)

                    # create.detail_line(doc, current_view, line_right_3)
                    # create.detail_line(doc, current_view, line_right_2)
                    # create.detail_line(doc, current_view, line_right_1)

                    # create.detail_line(doc, current_view, line_bot_3)
                    # create.detail_line(doc, current_view, line_bot_2)
                    # create.detail_line(doc, current_view, line_bot_1)

                    # create.detail_line(doc, current_view, line_left_3)
                    # create.detail_line(doc, current_view, line_left_2)
                    # create.detail_line(doc, current_view, line_left_1)

                    type_of_ele = tung_column.GetType()

                    tc_trai = 0
                    tc_phai = 0
                    tc_bot = 0
                    tc_top = 0

                    if str(type_of_ele) == "Autodesk.Revit.DB.FamilyInstance":

                        try:
                            tc_top = nances.get_parameter_value_by_name(tung_column, source_setting_family_column[8])
                        except:
                            
                            list_error.append(get_family_name(tung_column) + ": " +"Top fukashi parameter name not found")                
                            # print("Top fukashi parameter name not found")
                            pass
                        
                        try:
                            tc_bot = nances.get_parameter_value_by_name(tung_column, source_setting_family_column[9])
                        except:
                            list_error.append(get_family_name(tung_column) + ": " +"Bottom fukashi parameter name not found")             
                            # print("Bottom fukashi parameter name not found")
                            pass
                        
                        try:
                            tc_trai = nances.get_parameter_value_by_name(tung_column, source_setting_family_column[10])
                        except: 
                            list_error.append(get_family_name(tung_column) + ": " +"Left fukashi parameter name not found")             
                            # print("Left fukashi parameter name not found")
                            pass
                        
                        try:
                            tc_phai = nances.get_parameter_value_by_name(tung_column, source_setting_family_column[11])
                        except:
                            list_error.append(get_family_name(tung_column) + ": " +"Right fukashi parameter name not found")                     
                            # print("Right fukashi parameter name not found")
                            pass
                        
                        try:
                            ref_top = get_reference_by_name_in_family(tung_column,source_setting_family_column[0])
                        except:               
                            # print("Top reference name not found")
                            pass   
                        
                        try:             
                            ref_bot = get_reference_by_name_in_family(tung_column,source_setting_family_column[1])   
                        except:              
                            # print("Bottom reference name not found")
                            pass  
                        
                        try:                   
                            ref_trai = get_reference_by_name_in_family(tung_column,source_setting_family_column[2])
                        except:               
                            # print("Left reference name not found")
                            pass  
                        
                        try:
                            ref_phai = get_reference_by_name_in_family(tung_column,source_setting_family_column[3])
                        except:                
                            # print("Bottom reference name not found")
                            pass  
                        
                        try:
                            ref_fukashi_top = get_reference_by_name_in_family(tung_column,source_setting_family_column[4])
                        except:          
                            # print("Top fukashi reference name not found")
                            pass      

                        try:            
                            ref_fukashi_bot = get_reference_by_name_in_family(tung_column,source_setting_family_column[5])    
                        except:              
                            # print("Bottom fukashi reference name not found")
                            pass 

                        try:                     
                            ref_fukashi_trai = get_reference_by_name_in_family(tung_column,source_setting_family_column[6])
                        except:              
                            # print("Left fukashi reference name not found")
                            pass

                        try: 
                            ref_fukashi_phai = get_reference_by_name_in_family(tung_column,source_setting_family_column[7])
                        except:              
                            # print("Right fukashi reference name not found")
                            pass 

                    if is_plan_view:

                        #Tính cho dim top trước
                        #Combo 1_dim tổng
                        combo_ref_top_1.Append(ref_fukashi_trai)
                        combo_ref_top_1.Append(ref_fukashi_phai)

                        #Combo 2_dim chia tâm
                        combo_ref_top_2.Append(ref_fukashi_trai)
                        combo_ref_top_2.Append(ref_fukashi_phai)
                        try:
                            check_grid_Y_and_column_Y =[]
                            for check_ref_grid_Y in all_ref_top:
                                if ref_grid_Y == check_ref_grid_Y:
                                    combo_ref_top_2.Append(check_ref_grid_Y)
                                    check_grid_Y_and_column_Y.append(True)
                            if len(check_grid_Y_and_column_Y) == 0:
                                combo_ref_top_2.Append(left_right_ref)
                        except:
                            combo_ref_top_2.Append(left_right_ref)
                            pass

                        #Combo 3_dim tăng cường
                        combo_ref_top_3.Append(ref_fukashi_trai)
                        combo_ref_top_3.Append(ref_fukashi_phai)
                        # try:
                        #     check_grid_Y_and_column_Y =[]
                        #     for check_ref_grid_Y in all_ref_top:
                        #         if ref_grid_Y == check_ref_grid_Y:
                        #             combo_ref_top_3.Append(check_ref_grid_Y)
                        #             check_grid_Y_and_column_Y.append(True)
                        #     if len(check_grid_Y_and_column_Y) == 0:
                        #         combo_ref_top_3.Append(left_right_ref)
                        # except:
                        #     combo_ref_top_3.Append(left_right_ref)
                        #     pass
                        if float(tc_trai) > 0:
                            combo_ref_top_3.Append(ref_trai)
                        if float(tc_phai) > 0:
                            combo_ref_top_3.Append(ref_phai)      



                    '''Chia ra trường hợp có tăng cường và trường hợp không có tăng cường
                    Nếu có dim 3 thì line dim vẫn theo thứ tự.
                    Nếu không dim dim 3 thì line dim sẽ thay đổi chút.               
                    '''
                    if option_dim_combo_3 and combo_ref_top_3.Size > 2:
                        dim_top_3 = doc.Create.NewDimension(current_view, line_ngang_3, combo_ref_top_3)
                        list_new_dim.append(dim_top_3)
                        list_dim_need_modify_text_top.append(dim_top_3)
                        if option_dim_combo_2:
                            if combo_ref_top_2.Size > 2:
                                try:
                                    dim_top_2 = doc.Create.NewDimension(current_view, line_ngang_2, combo_ref_top_2)
                                    list_new_dim.append(dim_top_2)
                                    list_dim_need_modify_text_top.append(dim_top_2)
                                except Exception as e:
                                    if str(e) == "Invalid number of references.":
                                        list_error.append(get_family_name(tung_column) + ": " +"Invalid number of references.")
                                        pass

                            else: 
                                dim_top_2 = 0
                        # if option_dim_combo_1:
                        #     if combo_ref_top_1.Size >= 2:
                        #         try:
                        #             dim_top_1 = doc.Create.NewDimension(current_view, line_ngang_1, combo_ref_top_1)
                        #             list_new_dim.append(dim_top_1)
                        #         except Exception as e:
                        #             if str(e) == "Invalid number of references.":
                        #                 list_error.append(get_family_name(tung_column) + ": " +"Invalid number of references.")
                        #                 pass

                        #     else:
                        #         dim_top_1 = 0
                    else:
                        dim_top_3 = 0
                        if option_dim_combo_2:
                            if combo_ref_top_2.Size > 2:
                                try:
                                    dim_top_2 = doc.Create.NewDimension(current_view, line_ngang_3, combo_ref_top_2)
                                    list_new_dim.append(dim_top_2)
                                    list_dim_need_modify_text_top.append(dim_top_2)
                                except Exception as e:
                                    if str(e) == "Invalid number of references.":
                                        list_error.append(get_family_name(tung_column) + ": " +"Invalid number of references.")
                                        pass

                            else: 
                                dim_top_2 = 0
                        if option_dim_combo_1:
                            if combo_ref_top_1.Size >= 2:
                                try:
                                    dim_top_1 = doc.Create.NewDimension(current_view, line_ngang_2, combo_ref_top_1)
                                    list_new_dim.append(dim_top_1)
                                except Exception as e:
                                    if str(e) == "Invalid number of references.":
                                        list_error.append(get_family_name(tung_column) + ": " +"Invalid number of references.")
                                        pass

                            else:
                                dim_top_1 = 0





                    #Tính cho dim right
                    #Combo 1_dim tổng
                    combo_ref_right_1.Append(ref_fukashi_top)
                    combo_ref_right_1.Append(ref_fukashi_bot)

                    #Combo 2_dim chia tâm
                    combo_ref_right_2.Append(ref_fukashi_top)
                    combo_ref_right_2.Append(ref_fukashi_bot)
                    try:
                        check_grid_X_and_column_X =[]
                        for check_ref_grid_X in all_ref_right:
                            if ref_grid_X == check_ref_grid_X:
                                combo_ref_right_2.Append(check_ref_grid_X)
                                check_grid_X_and_column_X.append(True)
                        if len(check_grid_X_and_column_X) == 0:
                            combo_ref_right_2.Append(front_back_ref)
                    except:
                        combo_ref_right_2.Append(front_back_ref)
                        pass

                    #Combo 3_dim tăng cường
                    combo_ref_right_3.Append(ref_fukashi_top)
                    combo_ref_right_3.Append(ref_fukashi_bot)


                    # try:
                    #     check_grid_X_and_column_X =[]
                    #     for check_ref_grid_X in all_ref_right:
                    #         if ref_grid_X == check_ref_grid_X:
                    #             combo_ref_right_3.Append(check_ref_grid_X)
                    #             check_grid_X_and_column_X.append(True)
                    #     if len(check_grid_X_and_column_X) == 0:
                    #         combo_ref_right_3.Append(front_back_ref)
                    # except:
                    #     combo_ref_right_3.Append(front_back_ref)
                    #     pass
                    
                    if float(tc_top) > 0:
                        combo_ref_right_3.Append(ref_top)

                    if float(tc_bot) > 0:
                        combo_ref_right_3.Append(ref_bot)        


                    '''Chia ra trường hợp có tăng cường và trường hợp không có tăng cường
                    Nếu có dim 3 thì line dim vẫn theo thứ tự.
                    Nếu không dim dim 3 thì line dim sẽ thay đổi chút.                
                    '''        
                    if option_dim_combo_3 and combo_ref_right_3.Size > 2:
                        dim_right_3 = doc.Create.NewDimension(current_view, line_doc_3, combo_ref_right_3)
                        list_new_dim.append(dim_right_3)
                        list_dim_need_modify_text_right.append(dim_right_3)
                        if option_dim_combo_2:
                            if combo_ref_right_2.Size > 2:
                                try:
                                    dim_right_2 = doc.Create.NewDimension(current_view, line_doc_2, combo_ref_right_2)
                                    list_new_dim.append(dim_right_2)
                                    list_dim_need_modify_text_right.append(dim_right_2)
                                except Exception as e:
                                    if str(e) == "Invalid number of references.":
                                        list_error.append(get_family_name(tung_column) + ": " +"Invalid number of references.")
                                        pass

                            else: 

                                dim_right_2 = 0
                        # if option_dim_combo_1:
                        #     if combo_ref_right_1.Size >= 2:
                        #         try:
                        #             dim_right_1 = doc.Create.NewDimension(current_view, line_doc_1, combo_ref_right_1)
                        #             list_new_dim.append(dim_right_1)
                        #         except Exception as e:
                        #             if str(e) == "Invalid number of references.":
                        #                 list_error.append(get_family_name(tung_column) + ": " +"Invalid number of references.")
                        #                 pass
                        #     else:
                        #         dim_right_1 = 0
                    else:
                        dim_right_3 = 0
                        if option_dim_combo_2:
                            if combo_ref_right_2.Size > 2:
                                try:
                                    dim_right_2 = doc.Create.NewDimension(current_view, line_doc_3, combo_ref_right_2)
                                    list_new_dim.append(dim_right_2)
                                    list_dim_need_modify_text_right.append(dim_right_2)
                                except Exception as e:
                                    if str(e) == "Invalid number of references.":
                                        list_error.append(get_family_name(tung_column) + ": " +"Invalid number of references.")
                                        pass

                            else: 

                                dim_right_2 = 0
                        if option_dim_combo_1:
                            if combo_ref_right_1.Size >= 2:
                                try:
                                    dim_right_1 = doc.Create.NewDimension(current_view, line_doc_2, combo_ref_right_1)
                                    list_new_dim.append(dim_right_1)
                                except Exception as e:
                                    if str(e) == "Invalid number of references.":
                                        list_error.append(get_family_name(tung_column) + ": " +"Invalid number of references.")
                                        pass
                            else:
                                dim_right_1 = 0


                except Exception as e:
                    pass
                    if hasattr(tung_column,"Category"):
                        if hasattr(tung_column.Category,"Name"):                           
                            print (str(tung_column.Category.Name) + ":" + str(e))
                    else:
                        print (str(e))

        if len(list_dim_need_modify_text_top) > 0 :
            for tung_dim in list_dim_need_modify_text_top:
                try:
                    from nances import revit
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

                                allinone.move_text_dim_type_1_auto(tung_dim, current_view, return_point_lech, kich_co_chu = 1.8)   
                        
                except Exception as e:
                    print(traceback.format_exc())
                    pass
                
        if len(list_dim_need_modify_text_right) > 0 :
            for tung_dim in list_dim_need_modify_text_right:
                try:
                    from nances import revit
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

                                allinone.move_text_dim_type_1_auto(tung_dim, current_view, return_point_lech, kich_co_chu = 1.8)   
                        
                except Exception as e:
                    print(traceback.format_exc())
                    pass
                        
    set_error = list(set(list_error))
    if len(set_error) > 0:
        output = script.get_output()
        logger = script.get_logger()
        logger.warning("Please hold Shift and click to the tool to setup input family.\nHãy giữ nút shift và bấm vào tool để setting lại input")
        for tung_loi in set_error:
            print (tung_loi)   
    try:
        selection.select_sau_khi_chay_tool(list_new_dim,uidoc)
    except:
        print(traceback.format_exc())
        pass
    trans_group.Assimilate()

                    


