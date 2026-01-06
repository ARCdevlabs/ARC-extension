# -*- coding: utf-8 -*-
import string,importlib,sys,traceback,Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List
from nances import forms

ARC=string.ascii_lowercase
begin=''.join(ARC[i] for i in [13,0,13,2,4,18])
module=importlib.import_module(str(begin))

if module.AutodeskData():
	from pyrevit.coreutils import applocales
	loc=str(applocales.get_current_applocale())
	if loc=="日本語 / Japanese (ja)":
		tin_nhan_1="選択された要素がありません。"
		huong_dan_1="通芯またはレベルを選択するためにマウスをドラッグします。"
		huong_dan_2="通芯またはレベルの端に近い点を1つ選択します。"
		huong_dan_3="通芯及びレベルを再度選択して、通り先端をON/OFFにする側を選択します。"
		huong_dan_4="通芯又はレベルを選択します。"
		msg_workplane="作業平面を設定できません。"
	else:
		tin_nhan_1="Không có đối tượng nào được chọn"
		huong_dan_1="Quét chuột để chọn các Grids hoặc Levels"
		huong_dan_2="Pick 1 điểm gần đầu trục hoặc level"
		huong_dan_3="Vui lòng chọn lại Grids và Levels. Sau đó chọn phía để bật/tắt đầu trục"
		huong_dan_4="Vui lòng chọn Grids hoặc Levels."
		msg_workplane="Không thể thiết lập Work Plane."

	uidoc=__revit__.ActiveUIDocument
	doc=uidoc.Document

	class GridLevelSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
		def AllowElement(self,e): return isinstance(e,(Grid,Level))
		def AllowReference(self,r,p): return False

	def set_work_plane_for_view(v):
		if v.SketchPlane: return True
		try:
			v.SketchPlane=SketchPlane.Create(doc,Plane.CreateByNormalAndOrigin(v.ViewDirection,v.Origin))
			return True
		except: return False

	def pick_grid_by_rectangle():
		try:
			with forms.WarningBar(title=huong_dan_1):
				return uidoc.Selection.PickElementsByRectangle(GridLevelSelectionFilter(),huong_dan_4)
		except: return None

	def toggle_bubble_visibility(e,pt,v):
		curves=e.GetCurvesInView(DatumExtentType.ViewSpecific,v)
		if not curves: return
		c=curves[0]
		if not isinstance(c,Line): return
		p0,p1=c.GetEndPoint(0),c.GetEndPoint(1)
		end=DatumEnds.End0 if pt.DistanceTo(p0)<pt.DistanceTo(p1) else DatumEnds.End1
		if e.IsBubbleVisibleInView(end,v): e.HideBubbleInView(end,v)
		else: e.ShowBubbleInView(end,v)

	while True:
		try:
			ids=uidoc.Selection.GetElementIds()
			if not ids:
				els=pick_grid_by_rectangle()
				if not els: break
			else:
				els=[doc.GetElement(i) for i in ids if isinstance(doc.GetElement(i),(Grid,Level))]
			if not els:
				module.message_box(tin_nhan_1);break
			t=Transaction(doc,"Toggle Grids/Levels Symbol")
			t.Start()
			if not set_work_plane_for_view(doc.ActiveView):
				module.message_box(msg_workplane);t.RollBack();break
			try:
				with forms.WarningBar(title=huong_dan_2):
					pt=uidoc.Selection.PickPoint(Autodesk.Revit.UI.Selection.ObjectSnapTypes.None,huong_dan_2)
			except:
				t.RollBack();break
			try:
				for e in els: toggle_bubble_visibility(e,pt,doc.ActiveView)
				t.Commit()
				uidoc.Selection.SetElementIds(List[ElementId]())
			except:
				t.RollBack();break
		except Exception as ex:
			break