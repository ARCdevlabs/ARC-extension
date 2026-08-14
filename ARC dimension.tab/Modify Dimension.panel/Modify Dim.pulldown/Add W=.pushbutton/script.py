# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.UI.Selection import ObjectType, ObjectSnapTypes
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import ItemFactoryBase
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
import math
import sys
from pyrevit import forms, revit, DB, UI
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Control

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

try:
	Currentview = doc.ActiveView
	if Currentview.ViewType in [ViewType.FloorPlan, ViewType.EngineeringPlan, ViewType.CeilingPlan, ViewType.Section]:
		def main():
			shift_pressed = Control.ModifierKeys == Control.ModifierKeys.Shift
			if shift_pressed:
				prefix = forms.ask_for_string(
					default="W=",
					prompt="Nhập prefix (VD: W=)\nĐể TRỐNG là xóa prefix hiện có.",
					title="Thêm Prefix cho Dimension"
				)
				if prefix is None:
					return
			else:
				prefix = "W="
			while True:
				try:
					def set_work_plane_for_view(view):
						current_work_plane = view.SketchPlane
						if current_work_plane is None:
							try:
								if view.ViewType in [ViewType.FloorPlan, ViewType.EngineeringPlan, ViewType.CeilingPlan]:
									plane = Plane.CreateByNormalAndOrigin(XYZ.BasisZ, XYZ.Zero)
								elif view.ViewType == ViewType.Section:
									plane = Plane.CreateByNormalAndOrigin(view.ViewDirection, view.Origin)
								sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(view.Document, plane)
								view.SketchPlane = sketch_plane
							except:
								return False
						return True

					def pick_point_with_nearest_snap():       
						snap_settings = UI.Selection.ObjectSnapTypes.None
						prompt = "Click gần text của dimension để thêm prefix..."
						try:
							click_point = uidoc.Selection.PickPoint(snap_settings, prompt)
							return click_point
						except:
							return None

					def projected_distance(p1, p2, view):
						vec = p2 - p1
						view_dir = view.ViewDirection.Normalize()
						proj_along_dir = vec.DotProduct(view_dir)
						perp_vec = vec - (proj_along_dir * view_dir)
						return perp_vec.GetLength()

					def get_nearest_point(points, reference_point, view):
						min_distance = float('inf')
						nearest_point = None
						for point in points:
							distance = projected_distance(point, reference_point, view)
							if distance < min_distance:
								min_distance = distance
								nearest_point = point
						return nearest_point, min_distance

					def add_prefix_to_dimension(dimension, prefix_value):
						try:
							if prefix_value == "":
								dimension.Prefix = ""
							else:
								dimension.Prefix = prefix_value
						except:
							pass

					t0 = Transaction(doc, "Set workplane")
					t0.Start()        
					current_view = uidoc.ActiveView
					if not set_work_plane_for_view(current_view):
						t0.RollBack()
						forms.alert("Không thể set Work Plane cho view hiện tại!", title="Error", warn_icon=True)
						return
					t0.Commit()   

					return_point = pick_point_with_nearest_snap()
					if not return_point:
						break
					
					collector = FilteredElementCollector(uidoc.Document, current_view.Id).OfCategory(BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType()

					list_dimension_and_seg = []
					list_dim_seg_point = []
					t = Transaction(doc, "Add/Remove Prefix")
					t.Start()  
					for dimension in collector:
						if not dimension.IsHidden(current_view):
							number_segment = dimension.NumberOfSegments
							if number_segment > 1:
								segments = dimension.Segments
								for seg in segments:
									list_dimension_and_seg.append(seg)
									list_dim_seg_point.append(seg.TextPosition)
							else:
								list_dimension_and_seg.append(dimension)
								list_dim_seg_point.append(dimension.TextPosition)
					
					if not list_dim_seg_point:
						t.RollBack()
						forms.alert("Không tìm thấy dimension nào trong view.", title="Info")
						break
					
					nearest_point_to_seg, min_dist = get_nearest_point(list_dim_seg_point, return_point, current_view)
					
					scale_factor = 1.0 / current_view.Scale
					threshold = max(5 * scale_factor, 2)
					
					if min_dist < threshold:
						zipped_seg = zip(list_dimension_and_seg, list_dim_seg_point)
						for dim_seg, dim_seg_point in zipped_seg:
							if dim_seg_point.IsAlmostEqualTo(nearest_point_to_seg):
								add_prefix_to_dimension(dim_seg, prefix)
								break
					else:
						forms.alert("Không chọn được dimension — click gần text hơn.", title="Info")
					
					t.Commit()

				except Exception as ex:
					if "Operation canceled by user." in str(ex):
						break
					else:
						import traceback
						forms.alert("Lỗi: " + str(ex), title="Error", warn_icon=True)
						break
		main()
	else:
		forms.alert("Vui lòng sử dụng tool ở mặt bằng hoặc mặt cắt", title="View Error", warn_icon=True)
except:
	import traceback
	forms.alert("Lỗi không xác định: " + traceback.format_exc(), title="Critical Error", warn_icon=True)