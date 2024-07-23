# -*- coding: utf8 -*-
__doc__ = 'Ẩn/Hiện đầu trục cho grid và level'
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Line
from rpw.ui.forms import *
from pyrevit import forms
import Autodesk
import sys
import traceback
from System.Collections.Generic import *
from Autodesk.Revit.UI import TaskDialog

# Get UIDocument
uidoc = __revit__.ActiveUIDocument

# Get Document 
doc = uidoc.Document

class GridSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
	def AllowElement(self, element):
		return element.Category.Id.IntegerValue in [int(BuiltInCategory.OST_Grids), int(BuiltInCategory.OST_Levels)]

	def AllowReference(self, reference, point):
		return False

def pick_grid_by_rectangle():
	with forms.WarningBar(title='Quét chuột để chọn các grid và level'):
		selection = uidoc.Selection
		selected_elements = selection.PickElementsByRectangle(GridSelectionFilter(), "Chọn grid và level")
	return selected_elements

# Lấy danh sách các đối tượng đã được chọn từ người dùng
selection = uidoc.Selection.GetElementIds()

# Nếu không có đối tượng nào được chọn, sử dụng phương thức quét chuột
if not selection:
	selection = pick_grid_by_rectangle()
	if not selection:
		TaskDialog.Show("Thông báo", "Không có đối tượng nào được chọn")
		sys.exit()

# Thiết lập work plane
def set_work_plane_for_view(view):
	current_work_plane = view.SketchPlane
	if current_work_plane is None:
		try:
			plane = Autodesk.Revit.DB.Plane.CreateByNormalAndOrigin(view.ViewDirection, view.Origin)
			sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(doc, plane)
			view.SketchPlane = sketch_plane
		except Exception as e:
			print("Lỗi khi thiết lập Work Plane: ", e)
			print(traceback.format_exc())
			return False
	return True

# Hàm chọn điểm
def pick_point_with_nearest_snap(iuidoc):
	snap_settings = Autodesk.Revit.UI.Selection.ObjectSnapTypes.None
	prompt = "Click"
	click_point = None
	try:
		click_point = iuidoc.Selection.PickPoint(snap_settings, prompt)
	except Exception as e:
		print("Lỗi khi chọn điểm: ", e)
		print(traceback.format_exc())
	return click_point

# Hàm ẩn/hiện đầu trục dựa trên click point
def bubble_visibility_grid(grid, click_point, view):
	datum_extent_type = Autodesk.Revit.DB.DatumExtentType.ViewSpecific
	list_curve = grid.GetCurvesInView(datum_extent_type, view)
	if list_curve:
		curve = list_curve[0]
		if isinstance(curve, Line):
			start_point = curve.GetEndPoint(0)
			end_point = curve.GetEndPoint(1)

			dist_to_start = click_point.DistanceTo(start_point)
			dist_to_end = click_point.DistanceTo(end_point)

			if dist_to_start < dist_to_end:
				if grid.IsBubbleVisibleInView(DatumEnds.End0, view):
					grid.HideBubbleInView(DatumEnds.End0, view)
				else:
					grid.ShowBubbleInView(DatumEnds.End0, view)
					grid.HideBubbleInView(DatumEnds.End1, view)
			else:
				if grid.IsBubbleVisibleInView(DatumEnds.End1, view):
					grid.HideBubbleInView(DatumEnds.End1, view)
				else:
					grid.ShowBubbleInView(DatumEnds.End1, view)
					grid.HideBubbleInView(DatumEnds.End0, view)

# Hàm chuyển đổi hiển thị đầu level dựa trên điểm click
def bubble_visibility_level(level, click_point, view):
	datum_extent_type = Autodesk.Revit.DB.DatumExtentType.ViewSpecific
	list_curve = level.GetCurvesInView(datum_extent_type, view)
	if list_curve:
		curve = list_curve[0]
		if isinstance(curve, Line):
			start_point = curve.GetEndPoint(0)
			end_point = curve.GetEndPoint(1)

			dist_to_start = click_point.DistanceTo(start_point)
			dist_to_end = click_point.DistanceTo(end_point)

			if dist_to_start < dist_to_end:
				if level.IsBubbleVisibleInView(DatumEnds.End0, view):
					level.HideBubbleInView(DatumEnds.End0, view)
				else:
					level.ShowBubbleInView(DatumEnds.End0, view)
					level.HideBubbleInView(DatumEnds.End1, view)
			else:
				if level.IsBubbleVisibleInView(DatumEnds.End1, view):
					level.HideBubbleInView(DatumEnds.End1, view)
				else:
					level.ShowBubbleInView(DatumEnds.End1, view)
					level.HideBubbleInView(DatumEnds.End0, view)

# Bắt đầu transaction
t = Transaction(doc, "Ẩn/Hiện đầu trục và level")
t.Start()

if not set_work_plane_for_view(doc.ActiveView):
	TaskDialog.Show("Thông báo", "Không thể thiết lập Work Plane. Vui lòng thử lại.")
	t.RollBack()
	sys.exit()

# Chọn điểm click chuột
with forms.WarningBar(title='Chọn điểm để Ẩn/Hiện đầu trục'):
	click_point = pick_point_with_nearest_snap(uidoc)

try:
	for elem in selection:
		if isinstance(elem, ElementId):
			elem = doc.GetElement(elem)
		if elem.Category.Id.IntegerValue == int(BuiltInCategory.OST_Grids):
			bubble_visibility_grid(elem, click_point, doc.ActiveView)
		elif elem.Category.Id.IntegerValue == int(BuiltInCategory.OST_Levels):
			bubble_visibility_level(elem, click_point, doc.ActiveView)
except Exception as e:
	print("Lỗi: ", e)
	print(traceback.format_exc())
	t.RollBack()
else:
	t.Commit()