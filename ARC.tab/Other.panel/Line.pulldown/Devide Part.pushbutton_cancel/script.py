# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog
from System.Collections.Generic import List
import Autodesk
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
from System.Collections.Generic import List
from Autodesk.Revit.DB import Curve
import Autodesk
import nances
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType


curve_array = List[Curve]()



# Chọn một Part từ model
# selection = uidoc.Selection
# ref = selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element, "Chọn một Part")
# part = doc.GetElement(ref.ElementId)
element = nances.get_elements(uidoc,doc, 'select part', noti = False)

# ref_plane = nances.get_element(uidoc,doc, 'select reference plane', noti = False)
pick = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element)
# list_ele.append(doc.GetElement(pick.ElementId))
ref_plane = doc.GetElement(pick.ElementId)

active_view= nances.Active_view(doc)
sketch_plane = active_view.SketchPlane
# print sketch_plane
trans_group = TransactionGroup(doc, ' Group')
trans_group.Start()
for tung_element in element:
    if isinstance(tung_element, Part): 
        # t = Transaction(doc, "Divide Part")
        # t.Start()
        from nances import revit
        with revit.Transaction('Divide Part', swallow_errors=True):
            part_ids = List[ElementId]()
            plane_ids = List[ElementId]()

            part_ids.Add(tung_element.Id)
            plane_ids.Add(ref_plane.Id)

            "Thay thế nhé"
            # skect_id = ElementId(16877)

            try:
                PartUtils.DivideParts(doc, part_ids, plane_ids,curve_array,sketch_plane.Id)
                # t.Commit()
            except:
                # t.RollBack()
                pass       
trans_group.Assimilate()
TaskDialog.Show("Thông báo", "Tool viết vội, thông cảm nếu có lỗi :v. Tool chỉ hoạt động trên view mặt bằng nhé.")