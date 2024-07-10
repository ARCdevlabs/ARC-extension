# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))

from nances import vectortransform

import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit import revit, DB, UI
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
Currentview = doc.ActiveView

def get_floor_sub_element_edge(floor):
    edge_list = []
    option = Options()
    option.ComputeReferences = True
    for geometryObject in floor.get_Geometry(option):
        if isinstance(geometryObject, Solid):
            for edge in geometryObject.Edges:
                        edge_list.append(edge)
    return edge_list

def get_floor_sub_element_edges_by_face(floor):
    edge_list = []
    option = Options()
    option.ComputeReferences = True
    for geometryObject in floor.get_Geometry(option):
        if isinstance(geometryObject, Solid):
            for face in geometryObject.Faces:
                for edgeArray in face.EdgeLoops:
                    for edge in edgeArray:
                        edge_list.append(edge)
    return edge_list

def spot_elevation (idoc, view, ref, point, bend, end,ref_point, leader):
    spot = idoc.Create.NewSpotElevation(view, ref, point, bend, end,ref_point, leader)
    return spot


try:
    transaction_group = TransactionGroup(doc, "Spot elevation Floor")
    transaction_group.Start()

    pick = uidoc.Selection.PickObject(ObjectType.Element)
    floor = doc.GetElement(pick.ElementId)
    if floor:
        edges = get_floor_sub_element_edges_by_face(floor)

        slab_shape_editor = floor.SlabShapeEditor.SlabShapeVertices

    list_point_ref = []
    list_point_location_key = []

    t_1 = Transaction (doc, "Tạo spot elevation")
    t_1.Start()
    list_new_spot = []
    dict_point_ref_and_xyz = {}

    bend_D = 10

    nghieng = True

    nghieng_60_do = 5

    shoulder_D = 10

    for edge in edges:

        start_point_ref = edge.GetEndPointReference(0)
        end_point_ref = edge.GetEndPointReference(1)

        curve_of_edge = edge.AsCurve()

        start_point_curve = curve_of_edge.GetEndPoint(0)
        end_point_curve = curve_of_edge.GetEndPoint(1)

        # start_point_curve_key = (round((start_point_curve.X),2), round((start_point_curve.Y),2)))
        # end_point_curve_key = (round((end_point_curve.X),2), round((end_point_curve.Y),2))

        start_point_curve_key = (round((start_point_curve.Y),2), round((start_point_curve.Z),2))
        end_point_curve_key = (round((end_point_curve.Y),2), round((start_point_curve.Z),2))

        list_point_ref.append(start_point_ref)
        list_point_ref.append(end_point_ref)

        list_point_location_key.append(start_point_curve_key)
        list_point_location_key.append(end_point_curve_key)

    for i, j in zip(list_point_location_key,list_point_ref):
        dict_point_ref_and_xyz[i] = j
    
    ket_qua_dict_point_ref_and_xyz = {}
    n = 0
    for sub_element_point in slab_shape_editor:
        n += 1
        toa_do_sub_element_point = sub_element_point.Position
        key = (round((toa_do_sub_element_point.X),2), round((toa_do_sub_element_point.Y),2))
        if key in dict_point_ref_and_xyz:
            ket_qua_dict_point_ref_and_xyz[toa_do_sub_element_point] = dict_point_ref_and_xyz[key]

    keys = ket_qua_dict_point_ref_and_xyz.keys()
    values = ket_qua_dict_point_ref_and_xyz.values()
    for toa_do_sub_point, ref_point in zip(keys,values):

        up_direction = Currentview.UpDirection

        view_direction = Currentview.ViewDirection
        

        bend = module.move_point_along_vector(toa_do_sub_point, up_direction, bend_D * Currentview.Scale /304.8)

        # xoay_vector_90 = XYZ(up_direction.Y,up_direction.X,up_direction.Z)

        xoay_vector_90 = vectortransform.rotate_vector(up_direction, view_direction, -90)

        if nghieng == True:
            bend = module.move_point_along_vector(bend, xoay_vector_90, nghieng_60_do * Currentview.Scale /304.8)
        else:
            bend = bend

        shoulder = module.move_point_along_vector(bend, xoay_vector_90, shoulder_D * Currentview.Scale /304.8)

        new_spot_elevation = spot_elevation(doc, Currentview, ref_point, toa_do_sub_point,
                        bend, shoulder,toa_do_sub_point, True)
        list_new_spot.append(new_spot_elevation)

    module.get_current_selection(uidoc,list_new_spot)
    t_1.Commit()

    # t_2 = Transaction (doc, "Xóa spot dư")
    # t_2.Start()

    # spot_elevations_dict = {}
    # for spot in list_new_spot:
    #     # Lấy vị trí của Spot Elevation
    #     location_point = spot.Origin
    #     point_key = (location_point.X, location_point.Y)

    #     # # Nếu vị trí đã tồn tại trong dictionary, xóa Spot Elevation
    #     # if point_key in spot_elevations_dict:
    #     #     doc.Delete(spot.Id)
    #     # else: 
    #     #     # Nếu vị trí chưa tồn tại, thêm vào dictionary
    #     #     spot_elevations_dict[point_key] = spot.Id

    #     if point_key in spot_elevations_dict:
    #         existing_spot_id, existing_z = spot_elevations_dict[point_key]
    #     # Nếu giá trị Z hiện tại cao hơn giá trị Z đã lưu, cập nhật dictionary và xóa Spot Elevation cũ
    #         if location_point.Z > existing_z:
    #             spot_elevations_dict[point_key] = (spot.Id, location_point.Z)
    #             doc.Delete(existing_spot_id)
    #         else:
    #             # Nếu giá trị Z hiện tại thấp hơn hoặc bằng, xóa Spot Elevation hiện tại
    #             doc.Delete(spot.Id)
    #     else:
    #         # Nếu vị trí chưa tồn tại, thêm vào dictionary
    #         spot_elevations_dict[point_key] = (spot.Id, location_point.Z) #point_key tương đương với key trong hàm dict
    #                                                                         # (spot.Id, location_point.Z) tương đương với value trong hàm dict
    #                                                                         # Value có thể có nhiều value bên trong, hoặc 1 value.


    # # Ham dict
    #         # new_dict = {key1: value1, key2: value2,..., keyN: valueN}
    #         # person = {
    #         #         'name': 'Nguyễn Thanh Sơn',
    #         #         'age': 28,
    #         #         'male': True,
    #         #         'status': 'single'        
    #         #         }

    # t_2.Commit()
    transaction_group.Assimilate()
except:
    import traceback
    print(traceback.format_exc())
    pass