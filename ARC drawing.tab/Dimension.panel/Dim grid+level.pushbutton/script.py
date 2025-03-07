# -*- coding: utf-8 -*-
from Autodesk.Revit.UI.Selection import ObjectType, ObjectSnapTypes
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import Selection
from pyrevit import forms, revit
import sys
import traceback
import Autodesk #cái này quan trọng, sử dụng cho pick point và set work plane = not associated

class GridSelectionFilter(Selection.ISelectionFilter):
	def AllowElement(self, element):
		return element.Category and element.Category.Id.IntegerValue in [int(BuiltInCategory.OST_Grids), int(BuiltInCategory.OST_Levels)]
	
	def AllowReference(self, reference, position):
		return False

uidoc = revit.uidoc
doc = uidoc.Document

def pick_grid_or_level(prompt="Chọn Grid hoặc Level"):
	with forms.WarningBar(title=prompt + " (bấm ESC để thoát)"):
		try:
			reference = uidoc.Selection.PickObject(ObjectType.Element, GridSelectionFilter(), prompt)
			if reference is None:
				return None
			return doc.GetElement(reference.ElementId)
		except Autodesk.Revit.Exceptions.OperationCanceledException:
			return None
		except Exception as e:
			forms.alert("Lỗi khi chọn Grid hoặc Level: " + str(e))
			return None
			
def pick_point_with_nearest_snap(iuidoc):
	snap_settings = ObjectSnapTypes.None
	prompt = "Click để chọn một điểm đặt dim"
	try:
		click_point = iuidoc.Selection.PickPoint(snap_settings, prompt)
		return click_point
	except Autodesk.Revit.Exceptions.OperationCanceledException:
		return None
	except Exception as e:
		print("Lỗi khi chọn điểm: ", e)
		return None

def get_element_position(element):
	if isinstance(element, Grid):
		return element.Curve.Evaluate(0.5, True)
	elif isinstance(element, Level):
		return XYZ(0, 0, element.Elevation)
	return None

def get_all_grids_or_levels_in_view(view, element1, element2):
	category = BuiltInCategory.OST_Grids if isinstance(element1, Grid) else BuiltInCategory.OST_Levels
	collector = FilteredElementCollector(doc, view.Id).OfCategory(category).WhereElementIsNotElementType()
	elements = list(collector)
	
	pos1 = get_element_position(element1)
	pos2 = get_element_position(element2)
	if not pos1 or not pos2:
		return []
	
	# Xác định hướng của grid (bao gồm trục xiên)
	if isinstance(element1, Grid):
		direction = element1.Curve.Direction
		# Chuẩn hóa vector hướng
		direction = direction.Normalize()
	else:
		is_horizontal = abs(pos2.X - pos1.X) > abs(pos2.Y - pos1.Y)
		direction = XYZ(1, 0, 0) if is_horizontal else XYZ(0, 1, 0)
	
	filtered_elements = []
	for el in elements:
		pos = get_element_position(el)
		if pos and isinstance(el, Grid):
			# Kiểm tra các grid song song với grid đầu tiên
			el_dir = el.Curve.Direction.Normalize()
			if el_dir.IsAlmostEqualTo(direction) or el_dir.IsAlmostEqualTo(-direction):
				perp_dir = XYZ(-direction.Y, direction.X, 0)
				filtered_elements.append((el, pos.DotProduct(perp_dir)))
		elif pos and isinstance(el, Level):
			if abs(pos.X - pos1.X) < 0.01 or abs(pos.Y - pos1.Y) < 0.01:
				filtered_elements.append((el, pos.Y if direction.Y > direction.X else pos.X))
	
	return [el[0] for el in sorted(filtered_elements, key=lambda x: x[1])]

def set_work_plane_for_view(view): #Set work plane = not associated
	try:
		plane = Plane.CreateByNormalAndOrigin(view.ViewDirection, view.Origin)
		sketch_plane = SketchPlane.Create(doc, plane)
		view.SketchPlane = sketch_plane
		return True
	except Exception as e:
		print("Lỗi khi set Work Plane: ", e)
		return False

def create_dimensions(view, elements, click_point):
	if not elements or len(elements) < 2:
		forms.alert("Không đủ elements để tạo dim")
		return
	
	is_grid = isinstance(elements[0], Grid)
	
	if is_grid:
		direction = elements[0].Curve.Direction.Normalize()
		dim_direction = XYZ(-direction.Y, direction.X, 0)
	else:
		if view.ViewDirection.IsAlmostEqualTo(XYZ(0, 0, 1)) or abs(view.ViewDirection.Z) > 0.9:
			dim_direction = XYZ(1, 0, 0)
		elif view.ViewDirection.IsAlmostEqualTo(XYZ(1, 0, 0)) or view.ViewDirection.IsAlmostEqualTo(XYZ(-1, 0, 0)):
			dim_direction = XYZ(0, 0, 1)
		elif view.ViewDirection.IsAlmostEqualTo(XYZ(0, 1, 0)) or view.ViewDirection.IsAlmostEqualTo(XYZ(0, -1, 0)):
			dim_direction = XYZ(0, 0, 1)
		else:
			forms.alert("Hướng view không được hỗ trợ")
			return
	
	dim_refs = ReferenceArray()
	for e in elements:
		dim_refs.Append(Reference(e))
	
	try:
		line = Line.CreateBound(click_point, click_point + dim_direction * 10) # 10 là độ dài mặc định
		doc.Create.NewDimension(view, line, dim_refs)
	except Exception as e:
		print("Lỗi khi tạo dimension: ", e)

with TransactionGroup(doc, "Auto dim Grids and Levels") as trans_group:
	trans_group.Start()
	try:
		t1 = Transaction(doc, "Set Work Plane")
		t1.Start()
		if not set_work_plane_for_view(uidoc.ActiveView):
			t1.RollBack()
			trans_group.RollBack()
			sys.exit(0)
		t1.Commit()

		while True:
			element1 = pick_grid_or_level("Chọn Grid hoặc Level thứ nhất")
			if not element1:
				break
				
			element2 = pick_grid_or_level("Chọn Grid hoặc Level thứ hai")
			if not element2:
				break
				
			elements = get_all_grids_or_levels_in_view(uidoc.ActiveView, element1, element2)
			if not elements:
				forms.alert("Không tìm thấy elements phù hợp")
				continue
				
			with forms.WarningBar(title="Chọn điểm để đặt dim"):
				click_point = pick_point_with_nearest_snap(uidoc)
				
			if not click_point:
				break

			t2 = Transaction(doc, "Create Dimensions")
			t2.Start()
			create_dimensions(uidoc.ActiveView, elements, click_point)
			t2.Commit()

		trans_group.Assimilate()
	except Exception as e:
		print("Lỗi: ", e)
		print(traceback.format_exc())
		trans_group.RollBack()
		sys.exit(0)