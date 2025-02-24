# -*- coding: utf-8 -*-
import sys
from Autodesk.Revit.DB import *
from nances.forms import select_sheets
from System.Windows.Forms import MessageBox

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView

transform = Transform.Identity
opts = CopyPasteOptions()

element_to_copy_ids = uidoc.Selection.GetElementIds()
if not element_to_copy_ids:
	MessageBox.Show("Vui lòng chọn các phần tử cần sao chép!", "Thông báo")
	sys.exit()

list_category = set()
element_info = {}

for element_id in element_to_copy_ids:
	element = doc.GetElement(element_id)
	if element.Category:
		category_name = element.Category.Name
		list_category.add(category_name)

		if category_name == "Viewports":
			view_name = doc.GetElement(element.ViewId).Name if element.ViewId else "Unknown"
			element_info[element_id] = "Viewport: " + view_name
		elif category_name == "Generic Annotations":
			type_name = "Unknown"
			if hasattr(element, 'Symbol') and element.Symbol:
				element_type = doc.GetElement(element.GetTypeId())
				if element_type:
					type_name_param = element_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM)
					if type_name_param:
						type_name = type_name_param.AsString()
				type_name = element.Symbol.FamilyName + " - " + type_name if hasattr(element, 'Symbol') else "Unknown"
			element_info[element_id] = "Generic Annotation: " + type_name
		elif category_name == "Lines":
			line_style = element.LineStyle.Name if hasattr(element, 'LineStyle') else "Unknown"
			element_info[element_id] = "Detail Line: " + line_style
		elif category_name == "Text Notes":
			text_type_name = "Unknown"
			if hasattr(element, 'TextNoteType'):
				element_type = doc.GetElement(element.GetTypeId())
				if element_type:
					type_name_param = element_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM)
					if type_name_param:
						text_type_name = type_name_param.AsString()
			element_info[element_id] = "Text Note: " + text_type_name

if len(list_category) > 1:
	MessageBox.Show("Vui lòng chỉ chọn một loại category sao chép trong một lần chạy tool!", "Thông báo")
	sys.exit()

selected_category = list_category.pop()

if selected_category not in ["Viewports", "Generic Annotations", "Title Blocks", "Text Notes", "Lines", "Revision Clouds", "Text Notes"]:
	MessageBox.Show(selected_category.upper() + " không được hỗ trợ trong Tool này!", "Thông báo")
	sys.exit()

current_sheet = view if isinstance(view, ViewSheet) else None
selected_sheets = select_sheets("Copy 2D on Sheet", multiple=True, button_name="Select Sheets")

if not selected_sheets:
	MessageBox.Show("Không có sheet nào được chọn!", "Thông báo")
	sys.exit()

if current_sheet:
	selected_sheets = [sht for sht in selected_sheets if sht.Id != current_sheet.Id]

if not selected_sheets:
	MessageBox.Show("Không có sheet hợp lệ để sao chép!", "Thông báo")
	sys.exit()

print("Sao chép " + selected_category)
for element_id, info in element_info.items():
	print(info)

t = Transaction(doc, "Copy Annotations On Sheet")
t.Start()

try:
	if selected_category == "Generic Annotations":
		print("⚠ " + "-" * 50 + "⚠ ")
		for sht in selected_sheets:
			existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericAnnotation).OwnedByView(sht.Id).ToElements()
			sheet_number = sht.LookupParameter("Sheet Number").AsString()
			sheet_name = sht.LookupParameter("Sheet Name").AsString()
			list_type_element = [k.GetTypeId().IntegerValue for k in existing_vps]

			copy_status = "⚪Copy ---> Sheet " + sheet_number + " - " + sheet_name
			for element_id in element_to_copy_ids:
				element = doc.GetElement(element_id)
				if element.Category and element.Category.Name == "Generic Annotations":
					type_element_copy = element.GetTypeId().IntegerValue
					if type_element_copy in list_type_element:
						copy_status = "❌Skip   ---> Sheet " + sheet_number + " - " + sheet_name
						break

			if "Copy" in copy_status:
				ElementTransformUtils.CopyElements(view, element_to_copy_ids, sht, transform, opts)
			print(copy_status)

	else:
		for sheet in selected_sheets:
			sheet_number = sheet.LookupParameter("Sheet Number").AsString()
			sheet_name = sheet.LookupParameter("Sheet Name").AsString()
			print("⚪Copy ---> Sheet " + sheet_number + " - " + sheet_name)
			ElementTransformUtils.CopyElements(view, element_to_copy_ids, sheet, transform, opts)

except Exception as e:
	MessageBox.Show("Lỗi khi sao chép: " + str(e), "Thông báo")
finally:
	t.Commit()

print("✅Copy Done!!!")