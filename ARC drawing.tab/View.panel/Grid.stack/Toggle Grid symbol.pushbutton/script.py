# -*- coding: utf-8 -*-
import string
import importlib
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import *
import traceback
import sys
from nances import forms
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))

if module.AutodeskData():
	from pyrevit.coreutils import applocales
	current_applocale = applocales.get_current_applocale()

	# Thông báo JP/VN
	if str(current_applocale) == "日本語 / Japanese (ja)":
		tin_nhan_1 = "選択された要素がありません。"
		huong_dan_1 = "通芯またはレベルを選択するためにマウスをドラッグします。"
		huong_dan_2 = "通芯またはレベルの端に近い点を1つ選択します。"
		huong_dan_3 = "通芯及びレベルを再度選択して、通り先端をON/OFFにする側を選択します。"
		huong_dan_4 = "通芯又はレベルを選択します。"
	else:
		tin_nhan_1 = "Không có đối tượng nào được chọn"
		huong_dan_1 = "Quét chuột để chọn các Grids hoặc Levels"
		huong_dan_2 = "Pick 1 điểm gần đầu trục hoặc level"
		huong_dan_3 = "Vui lòng chọn lại Grids và Levels. Sau đó chọn phía để bật/tắt đầu trục"	
		huong_dan_4 = "Vui lòng chọn Grids hoặc Levels."
	uidoc = __revit__.ActiveUIDocument
	doc = uidoc.Document

	# Filter để chọn grid và level
	class GridSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
		def AllowElement(self, element):
			return element.Category.Id.IntegerValue in [int(BuiltInCategory.OST_Grids), int(BuiltInCategory.OST_Levels)]

		def AllowReference(self, reference, point):
			return False

	# Hàm để chọn grid và level bằng cách quét
	def pick_grid_by_rectangle():
		try:
			with forms.WarningBar(title=huong_dan_1):
				selection = uidoc.Selection
				selected_elements = selection.PickElementsByRectangle(GridSelectionFilter(), huong_dan_4)
			return selected_elements
		except:
			sys.exit()

	# Lấy grid và level đã chọn

	# Set work plane
	def set_work_plane_for_view(view):
		current_work_plane = view.SketchPlane
		if current_work_plane is None:
			try:
				plane = Autodesk.Revit.DB.Plane.CreateByNormalAndOrigin(view.ViewDirection, view.Origin)
				sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(doc, plane)
				view.SketchPlane = sketch_plane
			except:
				return False
		return True

	# Hàm click point
	def pick_point_with_nearest_snap(iuidoc):
		snap_settings = Autodesk.Revit.UI.Selection.ObjectSnapTypes.None
		prompt = "Click"
		try:
			return iuidoc.Selection.PickPoint(snap_settings, prompt)
		except:
			return None

	# Bật/tắt hiển thị đầu trục dựa trên điểm click
	def bubble_visibility_grid(grid, click_point, view):
		datum_extent_type = Autodesk.Revit.DB.DatumExtentType.ViewSpecific
		curves = grid.GetCurvesInView(datum_extent_type, view)
		if curves:
			curve = curves[0]
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
				else:
					if grid.IsBubbleVisibleInView(DatumEnds.End1, view):
						grid.HideBubbleInView(DatumEnds.End1, view)
					else:
						grid.ShowBubbleInView(DatumEnds.End1, view)

	# Bật/tắt hiển thị đầu level dựa trên điểm click
	def bubble_visibility_level(level, click_point, view):
		datum_extent_type = Autodesk.Revit.DB.DatumExtentType.ViewSpecific
		curves = level.GetCurvesInView(datum_extent_type, view)
		if curves:
			curve = curves[0]
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
				else:
					if level.IsBubbleVisibleInView(DatumEnds.End1, view):
						level.HideBubbleInView(DatumEnds.End1, view)
					else:
						level.ShowBubbleInView(DatumEnds.End1, view)
while True:
	try:
		try:
			selected_ids = uidoc.Selection.GetElementIds()

			if not selected_ids:
				selected_elements = pick_grid_by_rectangle()
				if not selected_elements:
					module.message_box(tin_nhan_1)
					sys.exit()
			else:
				selected_elements = [doc.GetElement(id) for id in selected_ids]

			# Lọc Grid và Level
			grids = [e for e in selected_elements if isinstance(e, Grid)]
			levels = [e for e in selected_elements if isinstance(e, Level)]

			if not grids and not levels:
				module.message_box(huong_dan_4)
				sys.exit()
		except:
			break
		t = Transaction(doc, "Toggle Grids/Levels Symbol")
		t.Start()

		if not set_work_plane_for_view(doc.ActiveView):
			module.message_box("Cannot set Work Plane")
			t.RollBack()
			# sys.exit()

		# Chọn điểm click
		with forms.WarningBar(title=huong_dan_2):
			click_point = pick_point_with_nearest_snap(uidoc)

		if not click_point:
			module.message_box(huong_dan_3)
			t.RollBack()
			# sys.exit()

		# Bật/tắt hiển thị cho từng grid và level được chọn
		try:
			for elem in selected_elements:
				if isinstance(elem, Grid):
					bubble_visibility_grid(elem, click_point, doc.ActiveView)
				elif isinstance(elem, Level):
					bubble_visibility_level(elem, click_point, doc.ActiveView)
		except:
			t.RollBack()
		else:
			t.Commit()
	except Exception as ex:
		if "Operation canceled by user." in str(ex):
			break
		else:
			break