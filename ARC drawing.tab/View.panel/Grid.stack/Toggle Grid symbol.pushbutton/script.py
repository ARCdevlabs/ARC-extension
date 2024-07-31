# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
import traceback
import sys
from nances import forms
if module.AutodeskData():
	
	from pyrevit.coreutils import applocales
	current_applocale = applocales.get_current_applocale()
	if str(current_applocale) == "日本語 / Japanese (ja)":
		tin_nhan_1 = "選択された要素がありません。"
		huong_dan_1 = "通芯またはレベルを選択するためにマウス`をドラッグします。"
		huong_dan_2 = "通芯またはレベルの端に近い点を1つ選択します。"
	else:
		tin_nhan_1 = "Không có đối tượng nào được chọn"
		huong_dan_1 = "Quét chuột để chọn các grid hoặc level"
		huong_dan_2 = "Pick 1 điểm gần đầu trục hoặc level"

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
		try:
			with forms.WarningBar(title = huong_dan_1):
				selection = uidoc.Selection
				selected_elements = selection.PickElementsByRectangle(GridSelectionFilter(), "Chọn grid và level")
			return selected_elements
		except:
			sys.exit()

	# Lấy danh sách các đối tượng đã được chọn từ người dùng
	selection = uidoc.Selection.GetElementIds()

	if not selection:
		selection = pick_grid_by_rectangle()
		if not selection:
			module.message_box(tin_nhan_1)
			sys.exit()

	# Thiết lập work plane
	def set_work_plane_for_view(view):
		current_work_plane = view.SketchPlane
		if current_work_plane is None:
			try:
				plane = Autodesk.Revit.DB.Plane.CreateByNormalAndOrigin(view.ViewDirection, view.Origin)
				sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(doc, plane)
				view.SketchPlane = sketch_plane
			except:
				pass
				return False
		return True

	# Hàm chọn điểm
	def pick_point_with_nearest_snap(iuidoc):
		snap_settings = Autodesk.Revit.UI.Selection.ObjectSnapTypes.None
		prompt = "Click"
		click_point = None
		try:
			click_point = iuidoc.Selection.PickPoint(snap_settings, prompt)
		except:
			pass
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
						# grid.HideBubbleInView(DatumEnds.End1, view)
				else:
					if grid.IsBubbleVisibleInView(DatumEnds.End1, view):
						grid.HideBubbleInView(DatumEnds.End1, view)
					else:
						grid.ShowBubbleInView(DatumEnds.End1, view)
						# grid.HideBubbleInView(DatumEnds.End0, view)

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
						# level.HideBubbleInView(DatumEnds.End1, view)
				else:
					if level.IsBubbleVisibleInView(DatumEnds.End1, view):
						level.HideBubbleInView(DatumEnds.End1, view)
					else:
						level.ShowBubbleInView(DatumEnds.End1, view)
						# level.HideBubbleInView(DatumEnds.End0, view)

	# Bắt đầu transaction
	t = Transaction(doc, "Toggle Grid Symbol")
	t.Start()

	if not set_work_plane_for_view(doc.ActiveView):
		module.message_box("Can not setting Work Plane")
		t.RollBack()
		sys.exit()

	# Chọn điểm click chuột

	with forms.WarningBar(title = huong_dan_2):
		click_point = pick_point_with_nearest_snap(uidoc)

	try:
		for elem in selection:
			if isinstance(elem, ElementId):
				elem = doc.GetElement(elem)
			if elem.Category.Id.IntegerValue == int(BuiltInCategory.OST_Grids):
				bubble_visibility_grid(elem, click_point, doc.ActiveView)
			elif elem.Category.Id.IntegerValue == int(BuiltInCategory.OST_Levels):
				bubble_visibility_level(elem, click_point, doc.ActiveView)
	except:
		t.RollBack()
	else:
		t.Commit()