# -*- coding: utf-8 -*-
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
from pyrevit import revit
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    active_view = module.Active_view(doc)
    view_direction = active_view.ViewDirection
    if view_direction.Z == 1 and str(active_view.ViewType) != "ThreeD":

        beams = module.get_elements(uidoc,doc, 'Select Beams', noti = False)
        try:
            beam = beams[0]
            # beam_level = module.get_parameter_value_by_name(beam, "Reference Level", is_UTF8 = False)
            beam_level = module.get_builtin_parameter_by_name(beam, DB.BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM).AsElementId()


            def create_wall(doc, curve, level):
                wall = Wall.Create(doc, curve, level.Id, False)                         
                return wall  
            list_type_walls = module.all_type_of_class_and_OST(doc, WallType, BuiltInCategory.OST_Walls)
            for wall in list_type_walls:
                type_wall = wall

            trans_group = TransactionGroup(doc, "Create slab")
            trans_group.Start()

            with revit.Transaction("Tạo room separator", swallow_errors=True):
                levels = module.get_all_elements_of_OST(doc, BuiltInCategory.OST_Levels)
                for level in levels:
                    # level_name = module.get_parameter_value_by_name(level, "Name", is_UTF8 = True)
                    # level_name = module.get_builtin_parameter_by_name(level.Id, DB.BuiltInParameter.DATUM_TEXT).AsString()
                    if level.Id == beam_level:
                        room_level = level
                        break
                level_plane = room_level.GetPlaneReference()
                sketch_plane = SketchPlane.Create(doc, level_plane)
                curve_array = Autodesk.Revit.DB.CurveArray()
                list_wall = []
                for i in beams:
                    Cur = i.Location.Curve
                    Startpoint = Cur.GetEndPoint(0)
                    Endpoint = Cur.GetEndPoint(1)
                    Midpoint0 = Cur.Evaluate(0.7, True)
                    PlaMidpoint0 = XYZ(Midpoint0.X, Midpoint0.Y, 0)
                    Zpoint = Autodesk.Revit.DB.XYZ(Midpoint0.X, Midpoint0.Y, Midpoint0.Z + 10)
                    Zaxis = Autodesk.Revit.DB.Line.CreateBound(Midpoint0, Zpoint)
                    LCenter = Autodesk.Revit.DB.Line.CreateBound(XYZ(Startpoint.X,Startpoint.Y,Startpoint.Z),XYZ(Endpoint.X,Endpoint.Y,Startpoint.Z))
                    curve_array.Append(LCenter)
                    # wall = create_wall(doc, LCenter, level)
                    # list_wall.append(wall)
                room_separation = doc.Create.NewRoomBoundaryLines(sketch_plane, curve_array, active_view)

                # options = t1.GetFailureHandlingOptions()
                # options.SetClearAfterRollback(True)
                # options.SetForcedModalHandling(False)
                # t1.SetFailureHandlingOptions(options)



            limitoffset = 8
            beam_phase = module.get_parameter_value_by_name(beam, "Phase Created", is_UTF8 = False)
            phases = module.get_all_elements_of_OST(doc, BuiltInCategory.OST_Phases)
            for phase in phases:
                phase_name = module.get_parameter_value_by_name(phase, "Name", is_UTF8 = False)
                if phase_name == beam_phase:
                    room_phase = phase
                    break
            rooms = []
            list_rooms = []

            with revit.Transaction("Đặt room hàng loạt", swallow_errors=True):
                planTopology = doc.get_PlanTopology(room_level)
                for i,plancircuit in enumerate(planTopology.Circuits):
                    if plancircuit.IsRoomLocated == True:
                        continue
                    room = doc.Create.NewRoom(room_phase)
                    room.Name = "Room for create slab" + str(i)
                    room.Number = str(i) + "." + str(i)
                    room.LimitOffset = limitoffset
                    try:
                        new_room = doc.Create.NewRoom(room,plancircuit)
                    except:
                        continue
                    rooms.append(new_room)
                list_rooms.append(rooms)
                list_rooms_flat = module.flatten_list(list_rooms)

            def create_slabs(rooms, floor_type, offset, level_Id):
                slabs = []
                for room in rooms:
                    # IGNORE NON-BOUNDING ROOMS
                    if not room.get_Parameter(BuiltInParameter.ROOM_AREA).AsDouble():
                        return None

                    # ROOM BOUNDARIES -> List[CurveLoop]()
                    room_boundaries = room.GetBoundarySegments(SpatialElementBoundaryOptions())
                    curveLoopList   = List[CurveLoop]()

                    for roomBoundary in room_boundaries:
                        room_curve_loop = CurveLoop()
                        for boundarySegment in roomBoundary:
                            curve = boundarySegment.GetCurve()
                            room_curve_loop.Append(curve)
                        curveLoopList.Add(room_curve_loop)

                    if curveLoopList:
                        slab = Autodesk.Revit.DB.Floor.Create(doc, curveLoopList, floor_type, level_Id)
                        slabs.append(slab)
                        # SET OFFSET
                        param = slab.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)
                        param.Set(offset)
                        # structure = slab.get_Parameter(BuiltInParameter.FLOOR_PARAM_IS_STRUCTURAL).AsInteger()
                        structure = module.get_builtin_parameter_by_name(slab, DB.BuiltInParameter.FLOOR_PARAM_IS_STRUCTURAL)
                        structure.Set(1)
                return slabs


            # t3 = Transaction (doc, "Create slab (done)")
            # t3.Start()
            list_type_floors = module.all_type_of_class_and_OST(doc, FloorType, BuiltInCategory.OST_Floors)
            for floor in list_type_floors:
                type_floor = floor
            type_floor_id = type_floor.Id
            height_offset = 0
            level_id = room_level.Id
            with revit.Transaction("Tạo sàn và xóa room separator và xóa room", swallow_errors=True):
                try:
                    list_new_slabs = create_slabs (list_rooms_flat, type_floor_id, height_offset, level_id)
                    for delete_room_line in room_separation:
                        Autodesk.Revit.DB.Document.Delete(doc,delete_room_line.Id)
                    # for delete_wall in list_wall:
                    #     Autodesk.Revit.DB.Document.Delete(doc,delete_wall.Id)
                    for delete_room in list_rooms_flat:
                        Autodesk.Revit.DB.Document.Delete(doc,delete_room.Id)
                except:
                    pass
            trans_group.Assimilate()
        except:
            module.message_box("Please Select Only Beam")
            pass
    else:
        module.message_box("Please use the tool in plan view.") 