# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
import traceback
import math
import nances as module
from nances import vectortransform,geometry,selection

if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    #Get Document 
    doc = uidoc.Document
    Currentview = doc.ActiveView
    Curve = []

    def create_plane_from_point_and_normal(point, normal):
        plane = Plane(normal, point)
        return plane

    def are_planes_parallel(normal1, normal2):
        tolerance=0.0000001
        cross_product = normal1.CrossProduct(normal2)
        return cross_product.GetLength() < tolerance

    def distance_between_planes(normal1, point_on_plane1, normal2):
        vector_between_planes = point_on_plane1 - (point_on_plane1.DotProduct(normal2) - normal2.DotProduct(normal1)) / normal1.DotProduct(normal2) * normal1
        distance = vector_between_planes.GetLength()
        return distance
    def get_point_at_center_line(wall):
        wall_location = wall.Location
        wall_location_curve = wall_location.Curve
        start_point = wall_location_curve.GetEndPoint(0)
        return start_point
    
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


    def distance_to_plane(point, plane):
        distance = plane.Normal.DotProduct(point - plane.Origin)
        return distance
    def distance_between_parallel_planes(plane1, plane2):
        point_on_plane = XYZ(0, 0, 0)
        distance1 = abs(distance_to_plane(point_on_plane, plane1))
        distance2 = abs(distance_to_plane(point_on_plane, plane2))
        distance = (distance1 - distance2)
        return distance

    def get_wall_width(wall):

        compound_structure = wall.WallType.GetCompoundStructure()

        core_width = 0.0
        exterior_width = 0.0
        interior_width = 0.0

        if compound_structure is not None:

            first_core_layer = (compound_structure.GetFirstCoreLayerIndex())

            last_core_layer = (compound_structure.GetLastCoreLayerIndex())

            # Core layers
            for i in range(first_core_layer,last_core_layer + 1):

                core_width += (compound_structure.GetLayerWidth(i))

            # Các layer phía trước core
            for i in range(first_core_layer):

                interior_width += (compound_structure.GetLayerWidth(i))

            # Các layer phía sau core
            for i in range(last_core_layer + 1,compound_structure.LayerCount):

                exterior_width += (compound_structure.GetLayerWidth(i))
        return core_width,interior_width,exterior_width


    def get_wall_reference_by_magic(uid,index):
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
    
    Ele = module.get_elements(uidoc,doc, "Select Walls", noti = False)

    trans_group = TransactionGroup(doc, 'Dim kich thuoc tuong')
    trans_group.Start()
    from nances import revit
    if Ele:
        list_new_dim = []
        for wall in Ele:
            try:
                wall_width =  get_wall_width(wall)

                core_width = wall_width[0]

                interior_width = wall_width[1]

                exterior_width = wall_width[2]

                # print core_width*304.8, interior_width*304.8, exterior_width*304.8

                location_line = wall.Location.Curve

                flat_location_line = vectortransform.project_line_to_plane (location_line, Currentview) 

                flat_location_line_direction = flat_location_line.Direction

                chuan_hoa_vector_kieu_nguoc = vectortransform.chuan_hoa_vector_tu_trai_qua_phai_tren_xuong_duoi(flat_location_line_direction,Currentview)

                #Thông thường parameter "Dimension Line Snap Distance" có giá trị là 5mm
                snap_dim_mm = 5 #tính bằng mm
                
                snap_dim_feet = snap_dim_mm  / 304.8  #tính bằng feet

                line_combo_2 = vectortransform.get_rotate_90_location_line(location_line,Currentview)
                
                line_combo_1 = vectortransform.move_line_theo_vector_theo_ty_le_view(chuan_hoa_vector_kieu_nguoc, line_combo_2, snap_dim_feet, Currentview)

                line_combo_3 = vectortransform.move_line_theo_vector_theo_ty_le_view(chuan_hoa_vector_kieu_nguoc, line_combo_2, -snap_dim_feet, Currentview)

                # wall_reference = ReferenceArray()

                unique_id = wall.UniqueId

                # get_wall_reference_exterior = GetClosestWallReference_sua_lai(doc, wall, ShellLayerType.Exterior)                
                # get_wall_reference_interior = GetClosestWallReference_sua_lai(doc, wall, ShellLayerType.Interior)

                # wall_reference.Append(get_wall_reference_exterior)
                # wall_reference.Append(get_wall_reference_interior)

                get_all_ref_wall = get_all_wall_reference_by_magic(doc,unique_id,7) 

                list_combo_reference = tao_cac_cap_reference(get_all_ref_wall)

                list_all_dim = []
                list_valid_dim = []
            
                count_dim_core = 0
                count_dim_interior = 0
                count_dim_exterior = 0

                for tung_cap_ref in list_combo_reference: 
                    with revit.Transaction('Tao dim tam thoi', swallow_errors=True):
                        wall_reference = ReferenceArray()
                        wall_reference.Append(tung_cap_ref[0])
                        wall_reference.Append(tung_cap_ref[1])

                        dim = doc.Create.NewDimension(Currentview, line_combo_1, wall_reference)
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

                with revit.Transaction('nhập tên transaction1', swallow_errors=True):                            
                    for tung_dim in list_all_dim:
                        if tung_dim not in list_valid_dim:
                            doc.Delete(tung_dim.Id)
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
                with revit.Transaction('tao lai dim', swallow_errors=True):  
                      dim = doc.Create.NewDimension(Currentview, line_combo_1, new_wall_reference) 

                with revit.Transaction('xoa dim khong can thiet', swallow_errors=True):  
                    for tung_dim_kha_di in new_list_valid_dim:
                        doc.Delete(tung_dim_kha_di.Id)
            except:
                pass

    trans_group.Assimilate()