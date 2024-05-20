
# -*- coding: utf-8 -*-
__doc__ = 'nguyenthanhson1712@gmail.com'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
# import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
active_view = module.Active_view(doc)
beams = module.get_selected_elements(uidoc,doc)
beam = beams[0]
beam_level = module.get_parameter_value_by_name(beam, "Reference Level", is_UTF8 = False)
def create_new_area_plan (idoc, area_scheme_id, level_id):
	new_area_plan = Autodesk.Revit.DB.ViewPlan.CreateAreaPlan(idoc, area_scheme_id, level_id)
	return new_area_plan

def create_new_area_boundary( idoc, sketchPlane, geometryCurve, areaView):
    new_area_boundary = idoc.NewAreaBoundaryLine(sketchPlane,geometryCurve, areaView)
    return new_area_boundary
def create_area (idoc, area_view, uv_point):
    area = idoc.Create.NewArea(area_view, uv_point)
    return area
# all_area_schemes = FilteredElementCollector(doc).OfClass(AreaScheme).ToElements()
# # trans_group = TransactionGroup(doc, "Create slab")
# # trans_group.Start()
# t1 = Transaction (doc, "Create slab (step 1)")
# t1.Start()
# levels = module.get_all_elements_of_OST(doc, BuiltInCategory.OST_Levels)
# for level in levels:
# 	level_name = module.get_parameter_value_by_name(level, "Name", is_UTF8 = False)
# 	if level_name == beam_level:
# 		room_level = level
# 		break
# area_plan = create_new_area_plan(doc,all_area_schemes[0].Id,room_level.Id)     

# level_plane = room_level.GetPlaneReference()
# sketch_plane = SketchPlane.Create(doc, level_plane)
# curve_array = Autodesk.Revit.DB.CurveArray()
# list_wall = []
# for i in beams:
#     Cur = i.Location.Curve
#     Direction = Cur.Direction
#     Startpoint = Cur.GetEndPoint(0)
#     Endpoint = Cur.GetEndPoint(1)
#     Midpoint0 = Cur.Evaluate(0.7, True)
#     PlaMidpoint0 = XYZ(Midpoint0.X, Midpoint0.Y, 0)
#     Zpoint = Autodesk.Revit.DB.XYZ(Midpoint0.X, Midpoint0.Y, Midpoint0.Z + 10)
#     Zaxis = Autodesk.Revit.DB.Line.CreateBound(Midpoint0, Zpoint)
#     LCenter = Autodesk.Revit.DB.Line.CreateBound(XYZ(Startpoint.X,Startpoint.Y,Startpoint.Z),XYZ(Endpoint.X,Endpoint.Y,Startpoint.Z))
#     curve_array.Append(LCenter)
#     # wall = create_wall(doc, LCenter, level)
#     # list_wall.append(wall)
# # room_separation = doc.Create.NewRoomBoundaryLines(sketch_plane, curve_array, active_view)
# for cur in curve_array:
#     area_separation = doc.Create.NewAreaBoundaryLine(sketch_plane, cur, area_plan)
#     mid_point = cur.Evaluate(0.5, True)
#     uv =  UV(mid_point.X, mid_point.Y)            
#     new_area = create_area(doc,area_plan, uv)
# options = t1.GetFailureHandlingOptions()
# options.SetClearAfterRollback(True)
# options.SetForcedModalHandling(False)
# t1.SetFailureHandlingOptions(options)
# t1.Commit()

# print new_area


# limitoffset = 8
# beam_phase = module.get_parameter_value_by_name(beam, "Phase Created", is_UTF8 = False)
# phases = module.get_all_elements_of_OST(doc, BuiltInCategory.OST_Phases)
# for phase in phases:
#     phase_name = module.get_parameter_value_by_name(phase, "Name", is_UTF8 = False)
#     if phase_name == beam_phase:
#          room_phase = phase
#          break
# rooms = []
# list_rooms = []

# t2 = Transaction (doc, "Create slab (step 2)")
# t2.Start()
# planTopology = doc.get_PlanTopology(room_level)
# for i,plancircuit in enumerate(planTopology.Circuits):
#     if plancircuit.IsRoomLocated == True:
#         continue
#     room = doc.Create.NewRoom(room_phase)
#     room.Name = "Room for create slab" + str(i)
#     room.Number = str(i) + "." + str(i)
#     room.LimitOffset = limitoffset
#     try:
#         new_room = doc.Create.NewRoom(room,plancircuit)
#     except:
#         continue
#     rooms.append(new_room)
# list_rooms.append(rooms)
# list_rooms_flat = module.flatten_list(list_rooms)
# t2.Commit(options)

# def create_slabs(rooms, floor_type, offset, level_Id):
#     slabs = []
#     for room in rooms:
#         # IGNORE NON-BOUNDING ROOMS
#         if not room.get_Parameter(BuiltInParameter.ROOM_AREA).AsDouble():
#             return None

#         # ROOM BOUNDARIES -> List[CurveLoop]()
#         room_boundaries = room.GetBoundarySegments(SpatialElementBoundaryOptions())
#         curveLoopList   = List[CurveLoop]()

#         for roomBoundary in room_boundaries:
#             room_curve_loop = CurveLoop()
#             for boundarySegment in roomBoundary:
#                 curve = boundarySegment.GetCurve()
#                 room_curve_loop.Append(curve)
#             curveLoopList.Add(room_curve_loop)

#         if curveLoopList:
#             slab = Autodesk.Revit.DB.Floor.Create(doc, curveLoopList, floor_type, level_Id)
#             slabs.append(slab)
#             # SET OFFSET
#             param = slab.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)
#             param.Set(offset)
#     return slabs


# t3 = Transaction (doc, "Create slab (done)")
# t3.Start()
# list_type_floors = module.all_type_of_class_and_OST(doc, FloorType, BuiltInCategory.OST_Floors)
# for floor in list_type_floors:
#     type_floor = floor
# type_floor_id = type_floor.Id
# height_offset = 0
# level_id = room_level.Id
# list_new_slabs = create_slabs (list_rooms_flat, type_floor_id, height_offset, level_id)
# for delete_room_line in area_separation:
#     Autodesk.Revit.DB.Document.Delete(doc,delete_room_line.Id)
# # for delete_wall in list_wall:
# #     Autodesk.Revit.DB.Document.Delete(doc,delete_wall.Id)
# for delete_room in list_rooms_flat:
#     Autodesk.Revit.DB.Document.Delete(doc,delete_room.Id)
# t3.Commit(options)

# trans_group.Assimilate()

# Import các module cần thiết



t2 = Transaction (doc, "Test")
t2.Start()
print (t2.HasStarted())
doc.Delete(ElementId(5970902))
t2.Commit()
print (t2.HasEnded())
t2.RollBack()