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
from pyrevit import revit, UI
from pyrevit import script, forms
import sys
import nances
if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Currentview = doc.ActiveView

    def get_floor_sub_element_edge(floor):
        edge_list = []
        option = DB.Options()
        option.ComputeReferences = True
        for geometryObject in floor.get_Geometry(option):
            if isinstance(geometryObject, DB.Solid):
                for edge in geometryObject.Edges:
                            edge_list.append(edge)
        return edge_list

    def get_floor_sub_element_edges_by_face(floor):
        edge_list = []
        option = DB.Options()
        option.ComputeReferences = True
        for geometryObject in floor.get_Geometry(option):
            if isinstance(geometryObject, DB.Solid):
                for face in geometryObject.Faces:
                    for edgeArray in face.EdgeLoops:
                        for edge in edgeArray:
                            edge_list.append(edge)
        return edge_list

    def spot_elevation (idoc, view, ref, point, bend, end,ref_point, leader):
        spot = idoc.Create.NewSpotElevation(view, ref, point, bend, end,ref_point, leader)
        return spot


    def get_new_XYZ (spot):
        cspot_ori = spot.Origin
        cnew_X = cspot_ori.X
        cnew_Y = cspot_ori.Y
        cnew_Z = cspot_ori.Z
        cnew_XYZ = str(cnew_X) + str(cnew_Y) + str(cnew_Z)
        return cnew_XYZ

    def get_new_XYZ_point (input_point):
        dnew_X = input_point.X
        dnew_Y = input_point.Y
        dnew_Z = input_point.Z
        dnew_XYZ = str(dnew_X) + str(dnew_Y) + str(dnew_Z)
        return dnew_XYZ

    try:
        with module.forms.WarningBar(title="Select the floor have sub element."):
            pick = uidoc.Selection.PickObject(ObjectType.Element)
            floor = doc.GetElement(pick.ElementId)
    except:
        sys.exit()
    if floor:
        try:
            edges = get_floor_sub_element_edges_by_face(floor)
            slab_shape_editor = floor.SlabShapeEditor.SlabShapeVertices
        except:
            module.message_box("Please select the floor have sub element")
            sys.exit()
    class MyPath(forms.Reactive):
        def __init__(self, path):
            self._path = path

        @forms.reactive
        def path(self):
            return self._path

        @path.setter
        def path(self, value):
            self._path = value

    class UI(forms.WPFWindow, forms.Reactive):
        def __init__(self):
            self.my_path = MyPath(r'%APPDATA%\Roaming\pyRevit\Extensions\ARC extension.extension\ARC drawing.tab\Dimension.panel\Slab.stack\Spot Elevation.pulldown\Spot On SubElement.pushbutton\Tool Spot Elevation.jpg')
            return
        
        def setup(self):
            self.set_image_source(self.image_chu_thich, 'Tool Spot Elevation.jpg')

        def setting_a_value(self):
            return self.a_value.Text
        
        def setting_b_value(self):
            return self.b_value.Text
        
        def setting_c_value(self):
            return self.c_value.Text
        
        def click_button(self, sender, args):

            self.Close()
        
            nghieng_60_do = float(self.setting_a_value())

            bend_D = float(self.setting_c_value())

            shoulder_D = float(self.setting_b_value())

            try:
                transaction_group = DB.TransactionGroup(doc, "Spot elevation Floor")
                transaction_group.Start()

                t_1 = DB.Transaction (doc, "Tạo spot elevation")
                t_1.Start()
                list_new_spot = []

                # bend_D = 10

                nghieng = True

                # nghieng_60_do = 5 #Chiều ngang của spot line

                # shoulder_D = 10 #Chiều ngang của spot line

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

                t_2 = DB.Transaction (doc, "Xóa Spot Elevation dư")
                t_2.Start()

                seen = set()
                unique_spot = []
                for tung_spot in list_new_spot:
                    new_XYZ_spot = get_new_XYZ(tung_spot)
                    if new_XYZ_spot not in seen:
                        unique_spot.append(tung_spot)
                        seen.add(new_XYZ_spot)
                
                loc_spot_theo_sub_element = []
                for tung_spot in unique_spot:
                    new_XYZ_spot = get_new_XYZ(tung_spot)
                    for sub_point in slab_shape_editor:
                        sub_position = sub_point.Position
                        new_XYZ_point = get_new_XYZ_point(sub_position)
                        if str(new_XYZ_spot) == str(new_XYZ_point):
                            loc_spot_theo_sub_element.append(tung_spot)

                list_delete = []
                for item in list_new_spot:
                    if item not in loc_spot_theo_sub_element:
                        list_delete.append(item)
                        doc.Delete(item.Id)
                t_2.Commit()
                transaction_group.Assimilate()
            except:
                pass

    ui = script.load_ui(UI(), 'SpotElevationSetting.xaml')
    ui.show_dialog()
