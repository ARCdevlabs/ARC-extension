# -*- coding: utf-8 -*-
__doc__='Rút ngắn chiều dài Grids và Levels'
from Autodesk.Revit.UI.Selection import ObjectType,ObjectSnapTypes,ISelectionFilter
from Autodesk.Revit.DB import *
import Autodesk.Revit.Exceptions
from pyrevit import forms,revit
import string,importlib,sys

ARC=string.ascii_lowercase
begin=''.join(ARC[i] for i in [13,0,13,2,4,18])
module=importlib.import_module(str(begin))

if module.AutodeskData():
	from pyrevit.coreutils import applocales
	loc=str(applocales.get_current_applocale())
	if loc=="日本語 / Japanese (ja)":
		title_main="通り及びレベルを切断します。"
		msg_select="Grids/Levelsを選択してください（ESCで範囲選択）"
		msg_continue="追加選択、またはESCで切断位置選択へ"
		msg_selected="選択済み {} 個 - ESCで切断位置選択へ"
		msg_rectangle="通芯又はレベルを選択するためにマウスをドラッグします。"
		msg_pick="通り長さ調整の一点をクリックして選択します。"
		msg_none="対象が選択されていません。"
		msg_wp="ワークプレーンの設定に失敗しました。"
	else:
		title_main="Rút ngắn Grids và Levels"
		msg_select="Click chọn Grids/Levels (ESC để quét)"
		msg_continue="Chọn thêm hoặc ESC để chọn vị trí cắt"
		msg_selected="Đã chọn {} đối tượng - ESC để chọn vị trí cắt"
		msg_rectangle="Quét chuột để chọn các Grids và Levels."
		msg_pick="Click chọn vị trí để rút ngắn Grids và Levels"
		msg_none="Không có đối tượng nào được chọn!"
		msg_wp="Không thể thiết lập Work Plane."

uidoc=revit.uidoc
doc=uidoc.Document
view=doc.ActiveView

class GridLevelSelectionFilter(ISelectionFilter):
	def AllowElement(self,e): return isinstance(e,(Grid,Level))
	def AllowReference(self,r,p): return False

def set_wp(v):
	try:
		v.SketchPlane=SketchPlane.Create(doc,Plane.CreateByNormalAndOrigin(v.ViewDirection,v.Origin))
		return True
	except: return False

def nearest(p0,p1,p):
	v=(p1-p0).Normalize()
	return p0+v*((p-p0).DotProduct(v))

def modify(d,v,p):
	cs=d.GetCurvesInView(DatumExtentType.ViewSpecific,v)
	if not cs or not isinstance(cs[0],Line): return
	p0,p1=cs[0].GetEndPoint(0),cs[0].GetEndPoint(1)
	c=nearest(p0,p1,p)
	nc=Line.CreateBound(c,p1) if c.DistanceTo(p0)<c.DistanceTo(p1) else Line.CreateBound(p0,c)
	if nc.IsBound: d.SetCurveInView(DatumExtentType.ViewSpecific,v,nc)

def pick_elements():
	sel=uidoc.Selection
	res=[]
	for i in sel.GetElementIds():
		e=doc.GetElement(i)
		if isinstance(e,(Grid,Level)) and e not in res: res.append(e)
	if res: return res
	wb=forms.WarningBar(height=32)
	wb._setup(title=msg_select)
	wb.show()
	try:
		while True:
			prompt=msg_select if not res else msg_continue
			r=sel.PickObject(ObjectType.Element,GridLevelSelectionFilter(),prompt)
			e=doc.GetElement(r.ElementId)
			if e not in res: res.append(e)
			wb.message_tb.Text=msg_selected.format(len(res))
	except Autodesk.Revit.Exceptions.OperationCanceledException:
		pass
	finally:
		try: wb.Close();wb.Dispose()
		except: pass
	if not res:
		try:
			with forms.WarningBar(title=msg_rectangle):
				rs=sel.PickElementsByRectangle(GridLevelSelectionFilter(),msg_rectangle)
				for r in rs:
					e=doc.GetElement(r.Id) if hasattr(r,'Id') else r
					if e not in res: res.append(e)
		except Autodesk.Revit.Exceptions.OperationCanceledException:
			pass
	return res

els=pick_elements()
grids=[e for e in els if isinstance(e,Grid)]
levels=[e for e in els if isinstance(e,Level)]
if not grids and not levels: forms.alert(msg_none,exitscript=True)

tg=TransactionGroup(doc,title_main)
tg.Start()
try:
	t1=Transaction(doc,"Set Work Plane")
	t1.Start()
	if not set_wp(view):
		t1.RollBack();tg.RollBack();module.message_box(msg_wp);sys.exit()
	t1.Commit()
	with forms.WarningBar(title=msg_pick):
		pt=uidoc.Selection.PickPoint(ObjectSnapTypes.None,msg_pick)
	t2=Transaction(doc,title_main)
	t2.Start()
	for d in grids+levels: modify(d,view,pt)
	t2.Commit()
	tg.Assimilate()
except Exception as e:
	if tg.GetStatus()==TransactionStatus.Started: tg.RollBack()
	forms.alert("Lỗi: {}".format(str(e)))