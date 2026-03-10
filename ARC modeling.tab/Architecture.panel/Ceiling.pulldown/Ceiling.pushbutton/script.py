# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
import Autodesk.Revit.UI.Selection
import sys
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.UI import UIDocument
from rpw.ui.forms import Alert
import nances
try:
    if nances.AutodeskData():
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        pick = uidoc.Selection.PickObjects(ObjectType.Element)
        covert_reference_to_element = []
        for i in pick:
            element_id = i.ElementId
            covert_reference_to_element.append(doc.GetElement(element_id))
            
        Rooms = covert_reference_to_element
        active_view = doc.ActiveView # Lấy View hiện tại để vẽ Detail Line
        try: 
            active_level = active_view.GenLevel
            active_level_Id = active_level.Id
        except:
            Alert('Please run this tool on plan view and just select rooms',title="ARC tools",header= "")
            sys.exit()
            
        t = Transaction (doc, "Create ceiling from room")
        t.Start()
        
        failed_rooms = []

        # HÀM MỚI: Vẽ Detail Line bao quanh phòng
        def draw_detail_lines(room, view):
            options = SpatialElementBoundaryOptions()
            options.SpatialElementBoundaryLocation = SpatialElementBoundaryLocation.Finish
            boundaries = room.GetBoundarySegments(options)
            if boundaries:
                for boundary_list in boundaries:
                    for segment in boundary_list:
                        curve = segment.GetCurve()
                        try:
                            doc.Create.NewDetailCurve(view, curve)
                        except:
                            pass # Bỏ qua nếu có đoạn line siêu nhỏ không thể vẽ

        def create_ceilings(rooms, ceil_type, offset, level_Id, draw_lines_if_failed):
            ceilings = []
            for room in rooms:
                if not room.get_Parameter(BuiltInParameter.ROOM_AREA).AsDouble():
                    continue

                curveLoopList = None

                # Lấy mặt đáy từ khối Solid 3D
                geom_elem = room.ClosedShell
                if geom_elem:
                    for geom_obj in geom_elem:
                        if isinstance(geom_obj, Solid) and geom_obj.Faces.Size > 0:
                            for face in geom_obj.Faces:
                                if isinstance(face, PlanarFace):
                                    if face.FaceNormal.IsAlmostEqualTo(XYZ(0, 0, -1)):
                                        curveLoopList = face.GetEdgesAsCurveLoops()
                                        break
                            if curveLoopList:
                                break
                
                if not curveLoopList:
                    options = SpatialElementBoundaryOptions()
                    options.SpatialElementBoundaryLocation = SpatialElementBoundaryLocation.Finish
                    room_boundaries = room.GetBoundarySegments(options)
                    
                    if room_boundaries:
                        curveLoopList = List[CurveLoop]()
                        for roomBoundary in room_boundaries:
                            curve_list = List[Curve]()
                            for boundarySegment in roomBoundary:
                                curve_list.Add(boundarySegment.GetCurve())
                            try:
                                room_curve_loop = CurveLoop.Create(curve_list)
                                curveLoopList.Add(room_curve_loop)
                            except:
                                pass

                success = False
                if curveLoopList and curveLoopList.Count > 0:
                    try:
                        ceiling = Autodesk.Revit.DB.Ceiling.Create(doc, curveLoopList, ceil_type, level_Id)
                        ceilings.append(ceiling)
                        # SET OFFSET
                        param = ceiling.get_Parameter(BuiltInParameter.CEILING_HEIGHTABOVELEVEL_PARAM)
                        param.Set(offset)
                        success = True
                    except Exception as e:
                        pass
                
                if not success:
                    failed_rooms.append(room.Id.IntegerValue)
                    # Thực thi vẽ Detail Line nếu người dùng chọn tùy chọn này
                    if draw_lines_if_failed:
                        draw_detail_lines(room, active_view)

            return ceilings

        def all_type_of_ceiling():
            all_ceiling_type = FilteredElementCollector(doc).OfClass(CeilingType).OfCategory(BuiltInCategory.OST_Ceilings)
            return all_ceiling_type
            
        list_ceiling = all_type_of_ceiling()

        from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, CheckBox, Separator, Button)
        
        components = [Label('Select type of ceiling:'),
                        ComboBox('combobox1', [Autodesk.Revit.DB.Element.Name.GetValue(x) for x in list_ceiling]),
                        Label('Ceiling height:'),
                        TextBox('textbox1', Text="2700"),
                        CheckBox('draw_lines_cb', 'Draw Detail Lines for failed rooms', default=True),
                        Separator(),
                        Button('Create ceiling')]
                        
        form = FlexForm('ARC tools', components)
        form.show()
        
        if form.values:
            selected_ceiling = form.values["combobox1"]
            ceiling_height = float(form.values["textbox1"])
            draw_lines_if_failed = form.values["draw_lines_cb"] # Lấy giá trị True/False từ ô tick
            list_new_ceiling = []
            
            for i in list_ceiling:
                try:
                    type_name = Autodesk.Revit.DB.Element.Name.GetValue(i)
                    if type_name == selected_ceiling:
                        type_Id = i.Id
                        # Truyền thêm biến draw_lines_if_failed vào hàm
                        list_new_ceiling = create_ceilings(Rooms, type_Id, ceiling_height/304.8, active_level_Id, draw_lines_if_failed)
                        break
                except:
                    pass
            
            t.Commit()
            
            if list_new_ceiling:
                select = uidoc.Selection
                list_id = []
                for i in list_new_ceiling:
                    ceiling_id = i.Id
                    list_id.append(ceiling_id)
                Icollection = List[ElementId](list_id)
                select.SetElementIds(Icollection)
                
            if failed_rooms:
                failed_str = ", ".join(str(id) for id in failed_rooms)
                msg = 'Có một số room bị lỗi hình học, không thể tạo trần.\nDanh sách Room ID: ' + failed_str
                if draw_lines_if_failed:
                    msg += '\n\nAdd-in đã tự động vẽ Detail Lines bao quanh các phòng này để bạn dễ dàng rà soát và sửa lỗi.'
                Alert(msg, title="ARC tools", header="Cảnh báo")
        else:
            t.RollBack()
except Exception as e:
    pass