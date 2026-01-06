# -*- coding: utf-8 -*-
__title__="Select by\nCategory"
__author__="Tô Thanh Tùng"

from Autodesk.Revit.DB import *
from pyrevit import forms,script,revit
from rpw.ui.forms import FlexForm,Label,CheckBox,Button,Separator
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Control
from System.Collections.Generic import List

uidoc=__revit__.ActiveUIDocument
doc=uidoc.Document
config=script.get_config()

ids=uidoc.Selection.GetElementIds()
if not ids:
	forms.alert("Vui lòng chọn ít nhất một đối tượng mẫu!",title=__title__)
	script.exit()

cat_ids=[]
for i in ids:
	e=doc.GetElement(i)
	if e.Category and e.Category.Id not in cat_ids: cat_ids.append(e.Category.Id)

shift=Control.ModifierKeys==Control.ModifierKeys.Shift
sel_view=True
sel_model=False

if shift:
	sel_view=config.get_option('sel_view',True)
	sel_model=config.get_option('sel_model',False)
	form=FlexForm(__title__,[
		Label("Phạm vi chọn đối tượng:"),
		CheckBox('sel_view',"Trong View hiện tại",default=sel_view),
		CheckBox('sel_model',"Trên Toàn Model",default=sel_model),
		Separator(),
		Button("Chọn Các Đối Tượng")
	])
	if not form.show(): script.exit()
	sel_view=form.values['sel_view']
	sel_model=form.values['sel_model']
	config.sel_view=sel_view
	config.sel_model=sel_model
	script.save_config()

final_ids=[]
cat_filter=ElementMulticategoryFilter(List[ElementId](cat_ids))

if sel_view:
	final_ids.extend(
		FilteredElementCollector(doc,doc.ActiveView.Id)
		.WherePasses(cat_filter).WhereElementIsNotElementType().ToElementIds()
	)

if sel_model:
	model_ids=FilteredElementCollector(doc)\
		.WherePasses(cat_filter).WhereElementIsNotElementType().ToElementIds()
	final_ids=list(set(final_ids)|set(model_ids))

if final_ids:
	uidoc.Selection.SetElementIds(List[ElementId](final_ids))
else:
	forms.alert("Không tìm thấy đối tượng nào phù hợp.")