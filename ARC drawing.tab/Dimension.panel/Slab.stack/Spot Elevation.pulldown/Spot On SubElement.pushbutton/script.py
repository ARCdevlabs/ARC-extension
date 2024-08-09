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
import Autodesk.Revit.DB as DB
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

def get_new_XY (spot):
    cspot_ori = spot.Origin
    cnew_X = round(cspot_ori.X,3)
    cnew_Y = round(cspot_ori.Y,3)

    cnew_XY = str(cnew_X) + str(cnew_Y)
    return cnew_XY

def get_new_XYZ (spot):
    cspot_ori = spot.Origin
    cnew_X = round(cspot_ori.X,3)
    cnew_Y = round(cspot_ori.Y,3)
    cnew_Z = round(cspot_ori.Z,3)
    cnew_XYZ = str(cnew_X) + str(cnew_Y) + str(cnew_Z)
    return cnew_XYZ

def get_new_XYZ_point (input_point):
    cnew_X = round(input_point.X,3)
    cnew_Y = round(input_point.Y,3)
    cnew_Z = round(input_point.Z,3)
    cnew_XYZ = str(cnew_X) + str(cnew_Y) + str(cnew_Z)
    return cnew_XYZ

def get_new_Z (spot):
    cspot_ori = spot.Origin
    cnew_Z = round(cspot_ori.Z,3)
    return cnew_Z


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

    list_point = []

    list_ref_point = []

    for edge in edges:

        start_point_ref = edge.GetEndPointReference(0)
        end_point_ref = edge.GetEndPointReference(1)


        curve_of_edge = edge.AsCurve()

        start_point_curve = curve_of_edge.GetEndPoint(0)
        end_point_curve = curve_of_edge.GetEndPoint(1)

        list_ref_point.append(start_point_ref)
        list_ref_point.append(end_point_ref)

        list_point.append(start_point_curve)
        list_point.append(end_point_curve)

    for toa_do_sub_point, ref_point in zip(list_point,list_ref_point):

        up_direction = Currentview.UpDirection

        view_direction = Currentview.ViewDirection
        

        bend = module.move_point_along_vector(toa_do_sub_point, up_direction, bend_D * Currentview.Scale /304.8)

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

    t_2 = Transaction (doc, "Xóa Spot Elevation dư")
    t_2.Start()

    # list_unique = []

    # seen = set()
    # unique_list = []
    # for tung_spot in list_new_spot:
    #     spot_ori = tung_spot.Origin
    #     new_X = round(spot_ori.X,3)
    #     new_Y = round(spot_ori.Y,3)
    #     new_Z = round(spot_ori.Z,3)

    #     new_XYZ = str(new_X) + str(new_Y) + str(new_Z)

    #     if new_XYZ not in seen:
    #         unique_list.append(tung_spot)
    #         seen.add(new_XYZ)

    # last_return = []
    # for uni_item in unique_list:
    #     cnew_XY = get_new_XY(uni_item)
    #     cnew_Z = get_new_Z(uni_item)
    #     for uni_item_2 in unique_list:
    #         cnew_XY_2 = get_new_XY(uni_item_2)
    #         cnew_Z_2 = get_new_Z(uni_item_2)
    #         if uni_item.Id != uni_item_2.Id:
    #             if cnew_XY == cnew_XY_2:
    #                 if cnew_Z > cnew_Z_2:
    #                     last_return.append(uni_item)
    #                 else:
    #                     last_return.append(uni_item_2)


    # set_list_point = list(set(list_point))

    # loc_lan_cuoi = []
    # for tung_last in last_return:
    #     cnew_XYZ = get_new_XYZ(tung_last)
    #     for tung_point in set_list_point:
    #         qnew_X = round(tung_point.X,3)
    #         qnew_Y = round(tung_point.Y,3)
    #         qnew_Z = round(tung_point.Z,3)
    #         qnew_XYZ = str(qnew_X) + str(qnew_Y) + str(qnew_Z)
    #         if cnew_XYZ == qnew_XYZ:
    #             loc_lan_cuoi.append(tung_last)
    list_new_XYZ = []
    for tung_spot in list_new_spot:
        new_XYZ = get_new_XYZ(tung_spot)
        # list_new_XYZ.append(new_XYZ)

    list_new_XYZ_point = []
    list_loc_lan_cuoi = []
    for tung_point in list_point:
        new_XYZ_point = get_new_XYZ_point(tung_point)
        for tung_spot in list_new_spot:
            new_XYZ_spot = get_new_XYZ(tung_spot)
            if str(new_XYZ_spot) == str(new_XYZ_point):
                list_loc_lan_cuoi
        # list_new_XYZ_point.append(new_XYZ_point)

    for moi_XYZ_point in list_new_XYZ_point:






    # set_loc_lan_cuoi = list(set(loc_lan_cuoi))


    list_delete = []
    for item in list_new_spot:
        if item not in set_loc_lan_cuoi:
            list_delete.append(item)
            doc.Delete(item.Id)
    t_2.Commit()

    transaction_group.Assimilate()
except:
    import traceback
    print(traceback.format_exc())
    pass