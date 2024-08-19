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

	# Thông báo JP/VN
	if str(current_applocale) == "日本語 / Japanese (ja)":
		tin_nhan_0 = "通り及びレベルを切断します。"
		tin_nhan_1 = "選択した部材なし！"
		tin_nhan_2 = "通芯又はレベルを選択します。"
		huong_dan_1 = "通芯又はレベルを選択するためにマウスをドラッグします。"
		huong_dan_2 = "通芯及びレベルを選択します。"
		huong_dan_3 = "通り長さ調整の一点をクリックして選択します。"
		huong_dan_4 = "通芯及びレベルを再度選択して、短縮点を選択します。"
	else:
		tin_nhan_0 = "Cắt trục và level"
		tin_nhan_1 = "Không có đối tượng nào được chọn!"
		tin_nhan_2 = "Vui lòng chọn Grids hoặc Levels."
		huong_dan_1 = "Quét chuột để chọn các Grids và Levels."
		huong_dan_2 = "Chọn Grids và Levels."
		huong_dan_3 = "Click chọn điểm để thay đổi chiều dài trục."    
		huong_dan_4 = "Vui lòng chọn lại Grids và Levels. Sau đó chọn điểm rút ngắn."

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
		with forms.WarningBar(title=huong_dan_1):
			selection = uidoc.Selection
			selected_elements = selection.PickElementsByRectangle(GridSelectionFilter(), huong_dan_2)
		return selected_elements
	except:
		pass
# Lấy danh sách các đối tượng bằng cách chọn trước chạy tool sau
selected_ids = uidoc.Selection.GetElementIds()

if not selected_ids:
	selected_elements = pick_grid_by_rectangle()
	if not selected_elements:
		module.message_box(tin_nhan_1)
		sys.exit()
else:
	selected_elements = [doc.GetElement(id) for id in selected_ids]

# Lọc ra các đối tượng Grid và Level
grids = []
levels = []

for element in selected_elements:
	if isinstance(element, Grid):
		grids.append(element)
	elif isinstance(element, Level):
		levels.append(element)

# Nếu không có Grid hoặc Level nào được chọn, hiển thị thông báo và thoát
if not grids and not levels:
	module.message_box(tin_nhan_2)
	sys.exit()

# Hàm thiết lập work plane
def set_work_plane_for_view(view):
	try:
		# Create a Plane using the view's direction and origin
		plane = Autodesk.Revit.DB.Plane.CreateByNormalAndOrigin(view.ViewDirection, view.Origin)
		sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(doc, plane)
		view.SketchPlane = sketch_plane
		return True
	except:
		# print("Lỗi khi set Work Plane: ", e)
		# print(traceback.format_exc())
		return False

# Hàm click chuột
def pick_point_with_nearest_snap(iuidoc):
	snap_settings = Autodesk.Revit.UI.Selection.ObjectSnapTypes.None
	prompt = huong_dan_3
	click_point = None
	try:
		click_point = iuidoc.Selection.PickPoint(snap_settings, prompt)
	except Exception:
		pass  # Ignore the exception and continue
	return click_point

# Hàm xác định vị trí chuột so với đầu trục
def nearest_point_on_line(start, end, point):
	line_direction = (end - start).Normalize()
	vector = point - start
	distance = vector.DotProduct(line_direction)
	closest_point = start + line_direction * distance
	return closest_point

# Rút ngắn trục ở mb
def RUTNGAN_TRUC_MAT_BANG(grid, view, click_point):
	datum_extent_type = Autodesk.Revit.DB.DatumExtentType.ViewSpecific
	list_curve = grid.GetCurvesInView(datum_extent_type, view)
	if list_curve:
		curve = list_curve[0]
		if isinstance(curve, Line):
			start_point = curve.GetEndPoint(0)
			end_point = curve.GetEndPoint(1)

			# Tính điểm gần nhất với click_point
			closest_point = nearest_point_on_line(start_point, end_point, click_point)
			distance_to_start = closest_point.DistanceTo(start_point)
			distance_to_end = closest_point.DistanceTo(end_point)

			# Tính điểm new start and end points
			if distance_to_start < distance_to_end:
				new_start_point = closest_point
				new_end_point = end_point
			else:
				new_start_point = start_point
				new_end_point = closest_point

			# Tạo curve mới với tọa độ mới
			new_curve = Line.CreateBound(new_start_point, new_end_point)
			if new_curve.IsBound:
				grid.SetCurveInView(datum_extent_type, view, new_curve)

# Rút ngắn trục mặt đứng
def RUTNGAN_TRUC_MAT_DUNG(grid, view, click_point):
	datum_extent_type = Autodesk.Revit.DB.DatumExtentType.ViewSpecific
	list_curve = grid.GetCurvesInView(datum_extent_type, view)
	if list_curve:
		curve = list_curve[0]
		if isinstance(curve, Line):
			start_point = curve.GetEndPoint(0)
			end_point = curve.GetEndPoint(1)

			# Tính điểm gần nhất với click_point
			closest_point = nearest_point_on_line(start_point, end_point, click_point)
			distance_to_start = closest_point.DistanceTo(start_point)
			distance_to_end = closest_point.DistanceTo(end_point)

			# So sánh vị trí new start and end points
			if distance_to_start < distance_to_end:
				new_start_point = closest_point
				new_end_point = end_point
			else:
				new_start_point = start_point
				new_end_point = closest_point

			# Tạo curve mới với tọa độ mới
			new_curve = Line.CreateBound(new_start_point, new_end_point)
			if new_curve.IsBound:
				grid.SetCurveInView(datum_extent_type, view, new_curve)

# Rút ngắn level
def RUTNGAN_LEVEL(level, click_point):
	datum_extent_type = Autodesk.Revit.DB.DatumExtentType.ViewSpecific
	list_curve = level.GetCurvesInView(datum_extent_type, doc.ActiveView)
	if list_curve:
		curve = list_curve[0]
		if isinstance(curve, Line):
			start_point = curve.GetEndPoint(0)
			end_point = curve.GetEndPoint(1)

			# Tính toán điểm gần nhất
			closest_point = nearest_point_on_line(start_point, end_point, click_point)
			distance_to_start = closest_point.DistanceTo(start_point)
			distance_to_end = closest_point.DistanceTo(end_point)

			if distance_to_start < distance_to_end:
				new_start_point = closest_point
				new_end_point = end_point
			else:
				new_start_point = start_point
				new_end_point = closest_point

			# Vẽ lại curve mới
			new_curve = Line.CreateBound(new_start_point, new_end_point)
			if new_curve.IsBound:
				level.SetCurveInView(datum_extent_type, doc.ActiveView, new_curve)

trans_group = TransactionGroup(doc, tin_nhan_0)
trans_group.Start()

try:
	# Chạy set work plane
	t1 = Transaction(doc, "Set Work Plane")
	t1.Start()
	if not set_work_plane_for_view(uidoc.ActiveView):
		module.message_box("Không thể thiết lập Work Plane. Vui lòng thử lại.")
		t1.RollBack()
		trans_group.RollBack()
		sys.exit()
	t1.Commit()

	# Chọn vị trí thay đổi chiều dài
	with forms.WarningBar(title=huong_dan_3):
		click_point = pick_point_with_nearest_snap(uidoc)

	if not click_point:
		module.message_box(huong_dan_4)
		trans_group.RollBack()
		sys.exit()

	# Thay đổi chiều dài trục và level
	t2 = Transaction(doc, tin_nhan_0)
	t2.Start()
	for grid in grids:
		if doc.ActiveView.ViewType == ViewType.FloorPlan or doc.ActiveView.ViewType == ViewType.CeilingPlan:
			RUTNGAN_TRUC_MAT_BANG(grid, doc.ActiveView, click_point)
		else:
			RUTNGAN_TRUC_MAT_DUNG(grid, doc.ActiveView, click_point)
	for level in levels:
		RUTNGAN_LEVEL(level, click_point)
	t2.Commit()

	trans_group.Assimilate()
except:
	# print(traceback.format_exc())
# 	trans_group.RollBack()
# finally:
# 	trans_group.Dispose()
	sys.exit()