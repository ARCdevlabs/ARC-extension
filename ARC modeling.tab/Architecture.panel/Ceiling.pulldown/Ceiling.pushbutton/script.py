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
        t = Transaction (doc, "Create ceiling from room")
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
                    ceiling = Autodesk.Revit.DB.Ceiling.Create(doc, curveLoopList, ceil_type, level_Id)
                    ceilings.append(ceiling)
                    # SET OFFSET
                    param = ceiling.get_Parameter(BuiltInParameter.CEILING_HEIGHTABOVELEVEL_PARAM)
                    param.Set(offset)

            return ceilings


        def all_type_of_ceiling():
            all_ceiling_type = FilteredElementCollector(doc).OfClass(CeilingType).OfCategory(BuiltInCategory.OST_Ceilings)
            return all_ceiling_type
        list_ceiling = all_type_of_ceiling()
    
        
        # from pyrevit import forms   (khong thich dung form cua pyrevit nua)
        # selected_ceiling = \
        #     forms.CommandSwitchWindow.show(
        #         sorted([Autodesk.Revit.DB.Element.Name.GetValue(x) for x in list_ceiling]),
        #         message='Pick type of ceiling:'
        #     )


        from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                    Separator, Button, CheckBox)
        components = [Label('Select type of ceiling:'),
                        ComboBox('combobox1', [Autodesk.Revit.DB.Element.Name.GetValue(x) for x in list_ceiling]),
                        Label('Ceiling height:'),
                        TextBox('textbox1', Text="2700"),
                    #   CheckBox('checkbox1', 'Check this'), (khong can check box)
                        Separator(),
                        Button('Create ceiling')]
        form = FlexForm('ARC tools', components)
        form.show()
        # User selects `Opt 1`, types 'Wood' in TextBox, and select Checkbox
        form.values
        selected_ceiling = form.values["combobox1"]
        ceiling_height = float(form.values["textbox1"])
        list_new_ceiling = []
        for i in list_ceiling:
            try:
                type_name = Autodesk.Revit.DB.Element.Name.GetValue(i)
                if type_name == selected_ceiling:
                    type_Id = i.Id
                    list_new_ceiling = create_ceilings(Rooms, type_Id, ceiling_height/304.8, active_level_Id)
            except:
                pass
        t.Commit()
        select = uidoc.Selection
        list_id = []
        for i in list_new_ceiling:
            ceiling_id = i.Id
            list_id.append(ceiling_id)
        Icollection = List[ElementId](list_id)
        select.SetElementIds(Icollection)
except:
    pass