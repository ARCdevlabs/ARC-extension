# -*- coding: utf-8 -*-
__doc__ = 'Rút ngắn chiều dài Grids và Levels'
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import *
from rpw.ui.forms import *
from pyrevit import forms
import Autodesk
import sys
import traceback
from System.Collections.Generic import *
from Autodesk.Revit.UI import TaskDialog
from nances import forms
import string
import importlib

ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
if module.AutodeskData():
	from pyrevit.coreutils import applocales
	current_applocale = applocales.get_current_applocale()

	if str(current_applocale) == "日本語 / Japanese (ja)":
		tin_nhan_0 = "通り及びレベルを切断します。"
		tin_nhan_2 = "通芯又はレベルを選択します。"
		huong_dan_1 = "通芯又はレベルを選択するためにマウスをドラッグします。"
		huong_dan_3 = "通り長さ調整の一点をクリックして選択します。"
	else:
		tin_nhan_0 = "Cắt trục và level"
		tin_nhan_2 = "Vui lòng chọn Grids hoặc Levels."
		huong_dan_1 = "Quét chuột để chọn các Grids và Levels."
		huong_dan_3 = "Click chọn điểm để thay đổi chiều dài trục."    

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

class GridSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
	def AllowElement(self, element):
		return element.Category.Id.IntegerValue in [int(BuiltInCategory.OST_Grids), int(BuiltInCategory.OST_Levels)]
	
	def AllowReference(self, reference, point):
		return False

def pick_grid_by_rectangle():
	while True:
		try:
			with forms.WarningBar(title=huong_dan_1):
				selection = uidoc.Selection
				selected_elements = selection.PickElementsByRectangle(GridSelectionFilter(), tin_nhan_2)
			if selected_elements:
				return selected_elements
		except Autodesk.Revit.Exceptions.OperationCanceledException:
			sys.exit()  # Thoát lệnh nếu nhấn ESC

selected_ids = uidoc.Selection.GetElementIds()

if not selected_ids:
	selected_elements = pick_grid_by_rectangle()
else:
	selected_elements = [doc.GetElement(id) for id in selected_ids]

grids = []
levels = []

for element in selected_elements:
	if isinstance(element, Grid):
		grids.append(element)
	elif isinstance(element, Level):
		levels.append(element)

while not grids and not levels:
	selected_elements = pick_grid_by_rectangle()
	grids = [el for el in selected_elements if isinstance(el, Grid)]
	levels = [el for el in selected_elements if isinstance(el, Level)]

def set_work_plane_for_view(view):
	try:
		plane = Autodesk.Revit.DB.Plane.CreateByNormalAndOrigin(view.ViewDirection, view.Origin)
		sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(doc, plane)
		view.SketchPlane = sketch_plane
		return True
	except:
		return False

def pick_point_with_nearest_snap(iuidoc):
	snap_settings = Autodesk.Revit.UI.Selection.ObjectSnapTypes.None
	prompt = huong_dan_3
	try:
		click_point = iuidoc.Selection.PickPoint(snap_settings, prompt)
		return click_point
	except Autodesk.Revit.Exceptions.OperationCanceledException:
		sys.exit()  # Thoát lệnh nếu nhấn ESC
	except Exception:
		return None

def nearest_point_on_line(start, end, point):
	line_direction = (end - start).Normalize()
	vector = point - start
	distance = vector.DotProduct(line_direction)
	closest_point = start + line_direction * distance
	return closest_point

def RUTNGAN_TRUC(grid, view, click_point):
	datum_extent_type = Autodesk.Revit.DB.DatumExtentType.ViewSpecific
	list_curve = grid.GetCurvesInView(datum_extent_type, view)
	if list_curve:
		curve = list_curve[0]
		if isinstance(curve, Line):
			start_point = curve.GetEndPoint(0)
			end_point = curve.GetEndPoint(1)

			closest_point = nearest_point_on_line(start_point, end_point, click_point)
			distance_to_start = closest_point.DistanceTo(start_point)
			distance_to_end = closest_point.DistanceTo(end_point)

			new_start_point = closest_point if distance_to_start < distance_to_end else start_point
			new_end_point = end_point if distance_to_start < distance_to_end else closest_point

			new_curve = Line.CreateBound(new_start_point, new_end_point)
			if new_curve.IsBound:
				grid.SetCurveInView(datum_extent_type, view, new_curve)

def RUTNGAN_LEVEL(level, click_point):
	datum_extent_type = Autodesk.Revit.DB.DatumExtentType.ViewSpecific
	list_curve = level.GetCurvesInView(datum_extent_type, doc.ActiveView)
	if list_curve:
		curve = list_curve[0]
		if isinstance(curve, Line):
			start_point = curve.GetEndPoint(0)
			end_point = curve.GetEndPoint(1)

			closest_point = nearest_point_on_line(start_point, end_point, click_point)
			distance_to_start = closest_point.DistanceTo(start_point)
			distance_to_end = closest_point.DistanceTo(end_point)

			new_start_point = closest_point if distance_to_start < distance_to_end else start_point
			new_end_point = end_point if distance_to_start < distance_to_end else closest_point

			new_curve = Line.CreateBound(new_start_point, new_end_point)
			if new_curve.IsBound:
				level.SetCurveInView(datum_extent_type, doc.ActiveView, new_curve)

trans_group = TransactionGroup(doc, tin_nhan_0)
trans_group.Start()

try:
	t1 = Transaction(doc, "Set Work Plane")
	t1.Start()
	if not set_work_plane_for_view(uidoc.ActiveView):
		module.message_box("Không thể thiết lập Work Plane. Vui lòng thử lại.")
		t1.RollBack()
		trans_group.RollBack()
		sys.exit()
	t1.Commit()

	with forms.WarningBar(title=huong_dan_3):
		click_point = pick_point_with_nearest_snap(uidoc)

	if not click_point:
		module.message_box("Không có điểm nào được chọn.")
		trans_group.RollBack()
		sys.exit()

	t2 = Transaction(doc, tin_nhan_0)
	t2.Start()
	for grid in grids:
		RUTNGAN_TRUC(grid, doc.ActiveView, click_point)
	for level in levels:
		RUTNGAN_LEVEL(level, click_point)
	t2.Commit()

	trans_group.Assimilate()
except:
	trans_group.RollBack()
	sys.exit()
