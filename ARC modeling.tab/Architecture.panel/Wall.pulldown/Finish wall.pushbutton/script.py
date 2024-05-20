__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib

ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
import Autodesk.Revit.UI.Selection
import sys
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.UI import UIDocument
from rpw.ui.forms import Alert
try:
    if module.AutodeskData():
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        pick = uidoc.Selection.PickObjects(ObjectType.Element)
        covert_reference_to_element = []
        for i in pick:
            element_id = i.ElementId
            covert_reference_to_element.append(doc.GetElement(element_id))
        # Ele = module.get_selected_elements(uidoc,doc) #Code nay de chon truoc room
        Rooms = covert_reference_to_element
        try: 
            active_level = doc.ActiveView.GenLevel
            active_level_Id = active_level.Id
        except:
            Alert('Please run this tool on plan view and just select rooms',title="ARC tools",header= "")
            sys.exit()
        t = Transaction (doc, "Create finish wall from room")
        t.Start()
        def create_ceilings(rooms, ceil_type, offset, level_Id):
            ceilings = []
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

                #  CREATE CEILINGS
                if curveLoopList:
                    ceiling = Autodesk.Revit.DB.Floor.Create(doc, curveLoopList, ceil_type, level_Id)
                    ceilings.append(ceiling)
                    # SET OFFSET
                    param = ceiling.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)
                    param.Set(offset)

            return ceilings
        def create_wall(doc, rooms, wall_type, level, height_offset):
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
                        para_width = wall_type.get_Parameter(Autodesk.Revit.DB.BuiltInParameter.WALL_ATTR_WIDTH_PARAM).AsValueString()
                        offset_curve = curve.CreateOffset(float(para_width)/(-2*304.8), Autodesk.Revit.DB.XYZ.BasisZ)
                        wall = Wall.Create(doc, offset_curve, level.Id, False)
                        para_top_constraint = wall.get_Parameter(Autodesk.Revit.DB.BuiltInParameter.WALL_HEIGHT_TYPE)
                        para_top_constraint.Set(level.Id)                   
                        para_top_offset = wall.get_Parameter(Autodesk.Revit.DB.BuiltInParameter.WALL_TOP_OFFSET)
                        para_top_offset.Set(height_offset)
                        wall.WallType = wall_type                    
            return wall   
        def all_wall_type ()  :   
            wall_type = FilteredElementCollector(doc).OfClass(WallType).ToElements()
            return wall_type        

        list_wall_type = all_wall_type()
        from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                    Separator, Button, CheckBox)
        components = [Label('Select type of finish wall:'),
                        ComboBox('combobox1', [Autodesk.Revit.DB.Element.Name.GetValue(x) for x in list_wall_type]),
                        Label('Height offset:'),
                        TextBox('textbox1', Text="2700"),
                    #   CheckBox('checkbox1', 'Check this'), (khong can check box)
                        Separator(),
                        Button('Create finish wall')]
        form = FlexForm('ARC tools', components)
        form.show()
        # User selects `Opt 1`, types 'Wood' in TextBox, and select Checkbox
        form.values
        selected_ceiling = form.values["combobox1"]
        height_offset = float(form.values["textbox1"])
        list_new_ceiling = []
        list_new_wall = []
        for i in list_wall_type:
            type_name = Autodesk.Revit.DB.Element.Name.GetValue(i)
            if type_name == selected_ceiling:
                type_Id = i.Id
                new_wall = create_wall(doc, Rooms, i, active_level, height_offset/304.8)
                list_new_wall.append(new_wall)
        t.Commit()
        select = uidoc.Selection
        list_id = []
        for i in list_new_wall:
            wall_id = i.Id
            list_id.append(wall_id)
        Icollection = List[ElementId](list_id)
        select.SetElementIds(Icollection)
except:
    pass