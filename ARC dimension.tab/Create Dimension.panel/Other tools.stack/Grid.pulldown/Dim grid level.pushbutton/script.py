# -*- coding: utf-8 -*-
from Autodesk.Revit.UI.Selection import ObjectType,ISelectionFilter,ObjectSnapTypes
from Autodesk.Revit.DB import *
from pyrevit import forms,revit
import Autodesk,sys,traceback

class GridLevelSelectionFilter(ISelectionFilter):
	def AllowElement(self,e): return isinstance(e,(Grid,Level))
	def AllowReference(self,r,p): return False

uidoc=revit.uidoc
doc=uidoc.Document

def get_element_position(e):
	if isinstance(e,Grid): return e.Curve.Evaluate(0.5,True)
	if isinstance(e,Level): return XYZ(0,0,e.Elevation)

def get_all_grids_or_levels_in_view(v,e1,e2):
	cat=BuiltInCategory.OST_Grids if isinstance(e1,Grid) else BuiltInCategory.OST_Levels
	els=list(FilteredElementCollector(doc,v.Id).OfCategory(cat).WhereElementIsNotElementType())
	p1,p2=get_element_position(e1),get_element_position(e2)
	if not p1 or not p2: return []
	if isinstance(e1,Grid):
		dir=e1.Curve.Direction.Normalize()
	else:
		dir=XYZ(1,0,0) if abs(p2.X-p1.X)>abs(p2.Y-p1.Y) else XYZ(0,1,0)
	res=[]
	for e in els:
		p=get_element_position(e)
		if not p: continue
		if isinstance(e,Grid):
			d=e.Curve.Direction.Normalize()
			if d.IsAlmostEqualTo(dir) or d.IsAlmostEqualTo(-dir):
				perp=XYZ(-dir.Y,dir.X,0)
				res.append((e,p.DotProduct(perp)))
		else:
			if abs(p.X-p1.X)<0.01 or abs(p.Y-p1.Y)<0.01:
				res.append((e,p.Y if dir.Y>dir.X else p.X))
	return [i[0] for i in sorted(res,key=lambda x:x[1])]

def set_work_plane_for_view(v):
	try:
		v.SketchPlane=SketchPlane.Create(doc,Plane.CreateByNormalAndOrigin(v.ViewDirection,v.Origin))
		return True
	except: return False

def create_dimensions(v,els,pt):
	if not els or len(els)<2:
		forms.alert("Không đủ đối tượng để tạo dim");return
	if isinstance(els[0],Grid):
		d=els[0].Curve.Direction.Normalize()
		dim_dir=XYZ(-d.Y,d.X,0)
	else:
		if v.ViewType==Autodesk.Revit.DB.ViewType.Section: dim_dir=XYZ(0,0,1)
		elif abs(v.ViewDirection.Z)>0.9: dim_dir=XYZ(1,0,0)
		else: dim_dir=XYZ(0,0,1)
	refs=ReferenceArray()
	for e in els: refs.Append(Reference(e))
	try:
		line=Line.CreateBound(pt,pt+dim_dir*10)
		doc.Create.NewDimension(v,line,refs)
	except: pass

def run():
	v=uidoc.ActiveView
	tg=TransactionGroup(doc,"Auto Dim Grids/Levels")
	tg.Start()
	try:
		with forms.WarningBar(title="Chọn Grid/Level thứ nhất (ESC để thoát)"):
			r1=uidoc.Selection.PickObject(ObjectType.Element,GridLevelSelectionFilter())
			e1=doc.GetElement(r1.ElementId)
		with forms.WarningBar(title="Chọn Grid/Level thứ hai (ESC để thoát)"):
			r2=uidoc.Selection.PickObject(ObjectType.Element,GridLevelSelectionFilter())
			e2=doc.GetElement(r2.ElementId)
		if type(e1)!=type(e2):
			forms.alert("Hai đối tượng phải cùng loại!")
			tg.RollBack();return
		els=get_all_grids_or_levels_in_view(v,e1,e2)
		with forms.WarningBar(title="Click để chọn điểm đặt dimension (ESC để thoát)"):
			pt=uidoc.Selection.PickPoint(ObjectSnapTypes.None)
		t1=Transaction(doc,"Set Work Plane");t1.Start()
		set_work_plane_for_view(v);t1.Commit()
		t2=Transaction(doc,"Create Dimension");t2.Start()
		create_dimensions(v,els,pt);t2.Commit()
		tg.Assimilate()
	except Autodesk.Revit.Exceptions.OperationCanceledException:
		tg.RollBack()
	except:
		print(traceback.format_exc());tg.RollBack()

if __name__=="__main__": run()