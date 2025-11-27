# -*- coding: utf-8 -*-
import sys
from Autodesk.Revit.DB import *
from pyrevit.forms import select_sheets, alert
from pyrevit import script
from System.Collections.Generic import List
from System.Windows.Forms import MessageBox

__doc__ = 'Select similar 2D elements on multiple sheets'

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
output = script.get_output()
output.set_width(1100)
output.set_title("Select 2D Elements on Sheets")

selected_ids = uidoc.Selection.GetElementIds()
if not selected_ids or selected_ids.Count == 0:
	MessageBox.Show("Vui lòng chọn ít nhất 1 đối tượng 2D mẫu trước khi chạy tool!", "Warning")
	sys.exit()

selected_sheets = select_sheets(
	title="Chọn các Sheet cần tìm đối tượng tương tự",
	multiple=True,
	button_name="Chọn Sheets & Play"
)
if not selected_sheets:
	sys.exit()

target_sheet_ids = {s.Id for s in selected_sheets}

elements_to_select = []
owner_sheet_ids = set()

all_viewports    = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewports).WhereElementIsNotElementType()
all_titleblocks  = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsNotElementType()
all_annotations  = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericAnnotation).WhereElementIsNotElementType()
line_cat_filter  = ElementCategoryFilter(BuiltInCategory.OST_Lines)
all_detail_lines = FilteredElementCollector(doc).OfClass(CurveElement).WherePasses(line_cat_filter).WhereElementIsNotElementType()

sample_info = []

for elem_id in selected_ids:
	elem = doc.GetElement(elem_id)
	if not elem or not elem.Category:
		continue

	cat_name = elem.Category.Name

	if cat_name == "Viewports":
		view = doc.GetElement(elem.ViewId)
		view_name = view.Name if view else "Unknown View"
		sample_info.append("Viewport → {}".format(view_name))

	elif cat_name == "Title Blocks":
		type_elem = doc.GetElement(elem.GetTypeId())
		type_name = type_elem.FamilyName if type_elem else "Unknown Type"
		sample_info.append("Title Block → {}".format(type_name))

	elif cat_name == "Generic Annotations":
		type_elem = doc.GetElement(elem.GetTypeId())
		family_name = type_elem.FamilyName if type_elem else "Unknown"
		sample_info.append("Annotation → {}".format(family_name))

	elif cat_name in ["Lines", "Detail Lines"] and elem.LineStyle:
		style_name = elem.LineStyle.Name
		sample_info.append("Detail Line → {}".format(style_name))

sample_info = list(dict.fromkeys(sample_info))

# Tìm kiếm
for elem_id in selected_ids:
	elem = doc.GetElement(elem_id)
	if not elem or not elem.Category:
		continue

	cat_name = elem.Category.Name

	# 1. Viewports
	if cat_name == "Viewports":
		target_view_id = elem.ViewId
		for vp in all_viewports:
			if vp.ViewId == target_view_id and vp.SheetId in target_sheet_ids:
				elements_to_select.append(vp.Id)
				owner_sheet_ids.add(vp.SheetId)

	# 2. Title Blocks
	elif cat_name == "Title Blocks":
		target_type_id = elem.GetTypeId()
		for tb in all_titleblocks:
			if tb.GetTypeId() == target_type_id and tb.OwnerViewId in target_sheet_ids:
				elements_to_select.append(tb.Id)
				owner_sheet_ids.add(tb.OwnerViewId)

	# 3. Generic Annotations (ĐÃ SỬA LỖI target_scheme_ids → target_sheet_ids)
	elif cat_name == "Generic Annotations":
		target_type_id = elem.GetTypeId()
		for ann in all_annotations:
			if ann.GetTypeId() == target_type_id and ann.OwnerViewId in target_sheet_ids:
				elements_to_select.append(ann.Id)
				owner_sheet_ids.add(ann.OwnerViewId)

	# 4. Detail Lines
	elif cat_name in ["Lines", "Detail Lines"] and elem.LineStyle:
		target_style_id = elem.LineStyle.Id
		for curve in all_detail_lines:
			if curve.LineStyle and curve.LineStyle.Id == target_style_id and curve.OwnerViewId in target_sheet_ids:
				elements_to_select.append(curve.Id)
				owner_sheet_ids.add(curve.OwnerViewId)

# In kết quả
if elements_to_select:
	uidoc.Selection.SetElementIds(List[ElementId](elements_to_select))

	output.print_md("# TÌM & CHỌN THÀNH CÔNG")
	
	if sample_info:
		output.print_md("**Đang tìm theo:**")
		for info in sample_info:
			print("• {}".format(info))
		print("")

	output.print_md("**{} đối tượng** được tìm thấy trên các Sheet sau:\n".format(len(elements_to_select)))

	sorted_ids = sorted(owner_sheet_ids,
						key=lambda sid: (doc.GetElement(sid).SheetNumber or "ZZZ",
										doc.GetElement(sid).Name.lower()))

	for sid in sorted_ids:
		sheet = doc.GetElement(sid)
		num = sheet.SheetNumber or "(No Number)"
		name = sheet.Name
		eid = sid.IntegerValue
		full = "{} - {} (Id: {})".format(num, name, eid)
		link = output.linkify(sid, title=full)
		print("• {} → **{}**".format(link, full))

	print("\n" + "—" * 100)
	output.print_md("**Tổng cộng: {} Sheet** có đối tượng tương tự".format(len(sorted_ids)))
	print("Click vào link để đi đến Sheet.")
else:
	alert("Không tìm thấy đối tượng nào tương tự trên các Sheet đã chọn.")