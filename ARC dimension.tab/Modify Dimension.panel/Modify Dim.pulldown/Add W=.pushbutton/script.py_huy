# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.UI import TaskDialog
from pyrevit import script
from rpw.ui.forms import FlexForm, Label, TextBox, CheckBox, Button, Separator
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Control

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
config = script.get_config()
current_view = doc.ActiveView

# KIỂM TRA VIEW
is_legend = current_view.ViewType == ViewType.Legend
is_plan_view = current_view.ViewType in [ViewType.FloorPlan, ViewType.CeilingPlan, ViewType.EngineeringPlan]
is_section_elevation = current_view.ViewType in [ViewType.Section, ViewType.Elevation]

if not (is_legend or is_plan_view or is_section_elevation):
	TaskDialog.Show("Lỗi", "Chỉ dùng trong: FloorPlan, RCP, EngineeringPlan, Section, Elevation hoặc Legend")
	script.exit()

# SET WORK PLANE
def set_temporary_workplane(view):
	if view.SketchPlane is not None:
		return True
	
	try:
		if view.ViewType in [ViewType.FloorPlan, ViewType.CeilingPlan, ViewType.EngineeringPlan]:
			plane = Plane.CreateByNormalAndOrigin(XYZ.BasisZ, XYZ.Zero)
		else:  # Section hoặc Elevation
			plane = Plane.CreateByNormalAndOrigin(view.ViewDirection, view.Origin)
		
		sp = SketchPlane.Create(doc, plane)
		view.SketchPlane = sp
		return True
	except:
		return False

# KIỂM TRA VIEW LEGEND
if not is_legend:
	t_wp = Transaction(doc, "Temporary Workplane for Dimension Tool")
	t_wp.Start()
	if not set_temporary_workplane(current_view):
		t_wp.RollBack()
		TaskDialog.Show("Lỗi", "Không thể tạo Workplane tạm thời cho view này!\nTool sẽ thoát.")
		script.exit()
	t_wp.Commit()

shift_pressed = Control.ModifierKeys == Control.ModifierKeys.Shift
if not shift_pressed:
	add_prefix_mode = True
	replace_mode = False
	prefix_text = "W="
	replace_text = ""
else:
	last_add = config.get_option('add_prefix', True)
	last_rep = config.get_option('replace', False)
	last_txt = config.get_option('text', 'W=')
	components = [
		Label("Chọn chế độ:"),
		CheckBox('prefix', "Thêm Prefix", default=last_add),
		CheckBox('replace', "Thay Text hoàn toàn", default=last_rep),
		Separator(),
		Label("Nhập Prefix hoặc Text thay thế:"),
		Label("(Để trống = xóa prefix / bỏ override)"),
		TextBox('text', Text=last_txt, Height=60),
		Button("OK")
	]
	form = FlexForm("Dimension Tool - Thiết lập", components)
	if not form.show():
		script.exit()
	add_prefix_mode = form.values['prefix']
	replace_mode = form.values['replace']
	text_value = form.values['text'].strip()

	if not add_prefix_mode and not replace_mode:
		add_prefix_mode = True
		text_value = "W="
	
	prefix_text = text_value if add_prefix_mode else ""
	replace_text = text_value if replace_mode else ""

	config.add_prefix = add_prefix_mode
	config.replace = replace_mode
	config.text = text_value
	script.save_config()

mode_text = ""
if add_prefix_mode and replace_mode: mode_text = " - Prefix + Replace"
elif add_prefix_mode: mode_text = " - Add Prefix"
elif replace_mode: mode_text = " - Replace Text"
trans_name = "Dimension Tool" + mode_text

dim_elements_in_view = None
if not is_legend:
	dim_elements_in_view = FilteredElementCollector(doc, current_view.Id)\
		.OfCategory(BuiltInCategory.OST_Dimensions)\
		.WhereElementIsNotElementType()\
		.ToElements()

if is_legend:
	class LegendDimFilter(ISelectionFilter):
		def AllowElement(self, elem):
			return isinstance(elem, Dimension)
		def AllowReference(self, ref, pt):
			return False

	while True:
		try:
			ref = uidoc.Selection.PickObject(ObjectType.Element, LegendDimFilter())
			dim = doc.GetElement(ref.ElementId)
			if not isinstance(dim, Dimension): 
				continue
			click_pt = ref.GlobalPoint

			best_seg = None
			best_dist = float('inf')
			if dim.NumberOfSegments == 0:
				best_seg = dim
			else:
				for seg in dim.Segments:
					if not hasattr(seg, "TextPosition") or not seg.TextPosition: 
						continue
					d = seg.TextPosition.DistanceTo(click_pt)
					if d < best_dist:
						best_dist = d
						best_seg = seg
			if not best_seg:
				continue

			t = Transaction(doc, trans_name)
			t.Start()
			try:
				if add_prefix_mode and hasattr(best_seg, "Prefix"):
					best_seg.Prefix = prefix_text
				if replace_mode:
					best_seg.ValueOverride = replace_text if replace_text else None
				
				from System.Collections.Generic import List
				uidoc.Selection.SetElementIds(List[ElementId]([dim.Id]))
				t.Commit()
			except Exception as e:
				t.RollBack()
				TaskDialog.Show("Lỗi", "Không thể sửa dimension:\n" + str(e))
		except:
			break

else:
	view_dir = current_view.ViewDirection

	while True:
		try:
			pt = uidoc.Selection.PickPoint(ObjectSnapTypes.None)
		except: 
			break

		candidates = []
		for dim in dim_elements_in_view:
			if dim.IsHidden(current_view):
				continue
			if dim.NumberOfSegments > 0:
				for seg in dim.Segments:
					pos = getattr(seg, "TextPosition", None)
					if pos: 
						candidates.append((seg, pos, dim.Id))
			else:
				pos = getattr(dim, "TextPosition", None)
				if pos:
					candidates.append((dim, pos, dim.Id))

		if not candidates:
			continue

		best_seg = best_id = None
		min_dist = float('inf')
		for seg, pos, pid in candidates:
			vec = pt - pos
			perp = vec - vec.DotProduct(view_dir) * view_dir
			dist = perp.GetLength()
			if dist < min_dist:
				min_dist = dist
				best_seg = seg
				best_id = pid

		threshold = max(3.0 / current_view.Scale, 0.5)
		if min_dist > threshold:
			continue

		t = Transaction(doc, trans_name)
		t.Start()
		try:
			if add_prefix_mode and hasattr(best_seg, "Prefix"):
				best_seg.Prefix = prefix_text
			if replace_mode:
				best_seg.ValueOverride = replace_text if replace_text else None
			
			from System.Collections.Generic import List
			uidoc.Selection.SetElementIds(List[ElementId]([best_id]))
			t.Commit()
		except Exception as e:
			t.RollBack()
			TaskDialog.Show("Lỗi", "Không thể sửa dimension:\n" + str(e))