# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
active_view = uidoc.ActiveView


# Lấy các phần tử được chọn
selection = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]

# Tạo tập hợp để lưu tên các family đã chọn
selected_families = set()

# Lấy tên của các family từ các phần tử được chọn
for ele in selection:
    family_param = ele.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM)
    if family_param:
        family_name = family_param.AsValueString()
        if family_name:
            selected_families.add(family_name)

# Nếu không có family nào được chọn, thoát
if not selected_families:
    print("Không tìm thấy family nào trong các phần tử đã chọn.")

else:
    # Tạo danh sách để lưu ID của các phần tử thuộc các family đã chọn
    elements_to_select = []

    # Lặp qua tất cả các phần tử trong view hiện tại
    collector = FilteredElementCollector(doc, active_view.Id)
    elements = collector.WhereElementIsNotElementType().ToElements()

    for ele in elements:
        family_param = ele.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM)
        if family_param:
            family_name = family_param.AsValueString()
            if family_name in selected_families:
                elements_to_select.append(ele.Id)

    # Chọn tất cả các phần tử thuộc các family đã chọn
    if elements_to_select:
        uidoc.Selection.SetElementIds(List[ElementId](elements_to_select))
    else:
        print("Không tìm thấy phần tử nào thuộc family đã chọn trong view hiện tại.")
