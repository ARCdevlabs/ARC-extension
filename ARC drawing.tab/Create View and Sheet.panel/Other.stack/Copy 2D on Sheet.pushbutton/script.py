# -*- coding: utf-8 -*-
import sys
from Autodesk.Revit.DB import *
from pyrevit.forms import select_views,select_sheets
from pyrevit import forms
from System.Windows.Forms import MessageBox
from pyrevit import revit, DB, UI
from Autodesk.Revit.UI.Selection import ObjectType 
from System.Windows import Window, SizeToContent, WindowStartupLocation, Thickness
from System.Windows.Controls import StackPanel, TextBlock, Button, ScrollViewer
from System.Collections.Generic import List
from rpw.ui.forms import SelectFromList
__title__ = 'Copy 2D on Sheet'
Info = "ARC-Tools"

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

class CustomMessageBox(Window):
	def __init__(self, message):
		self.Title = Info
		self.SizeToContent = SizeToContent.WidthAndHeight  
		self.WindowStartupLocation = WindowStartupLocation.CenterScreen

		scroll_viewer = ScrollViewer()
		scroll_viewer.MaxHeight = 700  

		stack_panel = StackPanel()
		scroll_viewer.Content = stack_panel 
		self.Content = scroll_viewer  

		text_block = TextBlock()
		text_block.Text = message
		text_block.Margin = Thickness(10)
		stack_panel.Children.Add(text_block)

		button = Button()
		button.Content = "CLOSE"
		button.Margin = Thickness(10)
		button.Click += self.close_window
		stack_panel.Children.Add(button)

	def close_window(self, sender, e):
		self.Close()
transform = Transform.Identity
opts = CopyPasteOptions()

try:
	selected_ids = uidoc.Selection.GetElementIds()


	selected_sheets = []  
	cursheet = revit.uidoc.ActiveGraphicalView  

	if selected_ids:
		for j in selected_ids:
			ele = doc.GetElement(j)  
			if isinstance(ele, ViewSheet) and cursheet.Id != j:
				selected_sheets.append(ele)  
	else:

		selected_sheets = select_sheets("Select Sheets",multiple=True,
									button_name='OK')
		if not selected_sheets:
			sys.exit()
		cursheet = revit.uidoc.ActiveGraphicalView
		for v in selected_sheets:
			if cursheet.Id == v.Id:
				selected_sheets.remove(v)
	with forms.WarningBar(title="Click to select the object."):
		selected_object = uidoc.Selection.PickObject(ObjectType.Element)
		list_type_element_copy = []
		list_element_copy = []
		list_category = []
		eleid = selected_object.ElementId
		elementToCopy = List[ElementId]() 
		elementToCopy.Add(selected_object.ElementId) 
		element_copy = doc.GetElement(selected_object) 
		list_element_copy.append(element_copy)
		category = (element_copy.Category).Name
		list_category.append(category)

		if category == "Viewports":
			type_element_copy = (element_copy.ViewId).IntegerValue
			list_type_element_copy.append(type_element_copy)
		else:
			type_element_copy = (element_copy.GetTypeId()).IntegerValue
			list_type_element_copy.append(type_element_copy)

except Exception:  
    sys.exit()
view = doc.ActiveView

for x in list_category:
	if x not in ["Viewports", "Generic Annotations", "Title Blocks", "Lines",  "Text Notes"]:
		MessageBox.Show(category.upper() + " is not supported in this Tool !", Info)
		sys.exit()

value = SelectFromList(Info, ['Copy and Skip Existing Element','Copy and Replace', 'Upadate Location'])


if value == "Copy and Skip Existing Element":
	t = Transaction(doc,__title__)
	t.Start()
	for x in list_category: 
		if x == "Viewports":
			message_lines = ["Notification !","-"*75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewports).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				list_type_element=[]
				for k in existing_vps:
					type_element = (k.ViewId).IntegerValue
					list_type_element.append(type_element)

				if type_element_copy not in list_type_element:
					ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
					message_lines.append("{}-{} ----> Create New".format(sheet_number, sheet_name))
				elif type_element_copy  in list_type_element:			
					message_lines.append("{}-{} ----> {} Skip!".format(sheet_number, sheet_name, "*" * 30))
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()
		elif x == "Title Blocks":
			message_lines = ["Notification !","-"*75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				list_type_element=[]
				for k in existing_vps:
					type_element = (k.GetTypeId()).IntegerValue
					list_type_element.append(type_element)
				if type_element_copy not in list_type_element:
					ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
					message_lines.append("{}-{} ----> Create New".format(sheet_number, sheet_name))
				elif type_element_copy  in list_type_element:			
					message_lines.append("{}-{} ----> {} Skip!".format(sheet_number, sheet_name, "*" * 30))
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()
		elif x == "Generic Annotations":
			message_lines = ["Notification !","-"*75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericAnnotation).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				list_type_element=[]
				for k in existing_vps:
					type_element = (k.GetTypeId()).IntegerValue
					list_type_element.append(type_element)
				if type_element_copy not in list_type_element:
					ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
					message_lines.append("{}-{} ----> Create New".format(sheet_number, sheet_name))
				elif type_element_copy  in list_type_element:			
					message_lines.append("{}-{} ----> {} Skip!".format(sheet_number, sheet_name, "*" * 30))
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()

		elif x == "Lines":
			message_lines = ["Notification !","-"*75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				list_type_element=[]
				for k in existing_vps:
					type_element = (k.GetTypeId()).IntegerValue
					list_type_element.append(type_element)
				if type_element_copy not in list_type_element:
					ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
					message_lines.append("{}-{} ----> Create New".format(sheet_number, sheet_name))
				elif type_element_copy  in list_type_element:			
					message_lines.append("{}-{} ----> {} Skip!".format(sheet_number, sheet_name, "*" * 30))
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()
		elif x == "Text Notes":
			message_lines = ["Notification !","-"*75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TextNotes).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				list_type_element=[]
				for k in existing_vps:
					type_element = (k.GetTypeId()).IntegerValue
					list_type_element.append(type_element)
				if type_element_copy not in list_type_element:
					ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)	
					message_lines.append("{}-{} ----> Create New".format(sheet_number, sheet_name))
				elif type_element_copy  in list_type_element:			
					message_lines.append("{}-{} ----> {} Skip!".format(sheet_number, sheet_name, "*" * 30))
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()
	t.Commit()
elif value == "Copy and Replace":
	t = Transaction(doc,__title__)
	t.Start()
	for x in list_category: 
		if x == "Viewports":
			message_lines = ["Notification !","-"*75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewports).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				list_type_element=[]
				for k in existing_vps:
					type_element = (k.ViewId).IntegerValue
					list_type_element.append(type_element)

				if type_element_copy not in list_type_element:
					ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
					message_lines.append("{}-{} ----> Create New".format(sheet_number, sheet_name))
				elif type_element_copy  in list_type_element:
					existing_element = next((e for e in existing_vps if ((e.ViewId).IntegerValue == type_element_copy)), None) 
					if existing_element:
						doc.Delete(existing_element.Id)
						ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
						message_lines.append("{}-{} ----> {} Replace!".format(sheet_number, sheet_name, "*" * 25))
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()
		elif x == "Title Blocks":
			message_lines = ["Notification !","-"*75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				list_type_element=[]
				for k in existing_vps:
					type_element = (k.GetTypeId()).IntegerValue
					list_type_element.append(type_element)
				if type_element_copy not in list_type_element:
					ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
					message_lines.append("{}-{} ----> Create New".format(sheet_number, sheet_name))
				elif type_element_copy in list_type_element:
					existing_element = next((e for e in existing_vps if (e.GetTypeId().IntegerValue == type_element_copy)), None) 
					if existing_element:
						doc.Delete(existing_element.Id)
						ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
						message_lines.append("{}-{} ----> {} Replace!".format(sheet_number, sheet_name, "*" * 25))
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()

		elif x == "Generic Annotations":
			message_lines = ["Notification !","-"*75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericAnnotation).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				list_type_element=[]
				for k in existing_vps:
					type_element = (k.GetTypeId()).IntegerValue
					list_type_element.append(type_element)
				if type_element_copy not in list_type_element:
					ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
					message_lines.append("{}-{} ----> Create New".format(sheet_number, sheet_name))
				elif type_element_copy in list_type_element:
					existing_element = next((e for e in existing_vps if (e.GetTypeId().IntegerValue == type_element_copy)), None) 
					if existing_element:
						doc.Delete(existing_element.Id)
						ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
						message_lines.append("{}-{} ----> {} Replace!".format(sheet_number, sheet_name, "*" * 25))
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()

		elif x == "Lines":
			message_lines = ["Notification !","-"*75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				list_type_element=[]
				for k in existing_vps:
					type_element = (k.GetTypeId()).IntegerValue
					list_type_element.append(type_element)
				if type_element_copy not in list_type_element:
					ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
					message_lines.append("{}-{} ----> Create New".format(sheet_number, sheet_name))
				elif type_element_copy  in list_type_element:
					existing_element = next((e for e in existing_vps if (e.GetTypeId().IntegerValue == type_element_copy)), None) 
					if existing_element:
						doc.Delete(existing_element.Id)
						ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
						message_lines.append("{}-{} ----> {} Replace!".format(sheet_number, sheet_name, "*" * 25))
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()
		elif x == "Text Notes":
			message_lines = ["Notification !","-"*75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TextNotes).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				list_type_element=[]
				for k in existing_vps:
					type_element = (k.GetTypeId()).IntegerValue
					list_type_element.append(type_element)
				if type_element_copy not in list_type_element:
					ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)	
					message_lines.append("{}-{} ----> Create New".format(sheet_number, sheet_name))
				elif type_element_copy  in list_type_element:
					existing_element = next((e for e in existing_vps if (e.GetTypeId().IntegerValue == type_element_copy)), None) 
					if existing_element:
						doc.Delete(existing_element.Id)
						ElementTransformUtils.CopyElements(view, elementToCopy, sht, transform, opts)
						message_lines.append("{}-{} ----> {} Replace!".format(sheet_number, sheet_name, "*" * 25))
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()
	t.Commit()
elif value == "Upadate Location":
	t = Transaction(doc,"Upadate Location 2D On Sheet")
	t.Start()
	for x in list_category: 
		if x == "Viewports":
			message_lines = ["Notification !","-"*75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewports).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				found_updateable_element = False
				for k in existing_vps:
					type_element = (k.ViewId).IntegerValue
					if type_element_copy == type_element:
						found_updateable_element = True
						k.SetBoxCenter(element_copy.GetBoxCenter())
						k.ChangeTypeId(element_copy.GetTypeId())
						message_lines.append("{}-{} ----> Update location".format(sheet_number, sheet_name))
				if not found_updateable_element:
					message_lines.append("{}-{} ----> {} Not Found Element To Update!".format(sheet_number, sheet_name, "*" * 20))				
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()
		elif x == "Title Blocks":
			message_lines = ["Notification !","-"*75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				found_updateable_element = False
				for k in existing_vps:
					type_element = (k.GetTypeId()).IntegerValue
					if type_element_copy == type_element:
						found_updateable_element = True
						location = k.Location  
						if isinstance(location, DB.LocationPoint):
							new_location = element_copy.Location.Point  
							location.Point = new_location  
							k.ChangeTypeId(element_copy.GetTypeId())
							message_lines.append("{}-{} ----> Update location".format(sheet_number, sheet_name))
						elif isinstance(location, DB.LocationCurve):
							pass
				if not found_updateable_element:
					message_lines.append("{}-{} ----> {} Not Found Element To Update!".format(sheet_number, sheet_name, "*" * 20))
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()

		elif x == "Generic Annotations":
			message_lines = ["Notification!", "-" * 75]
			for sht in selected_sheets:
				existing_vps = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericAnnotation).OwnedByView(sht.Id).ToElements()
				sheet_number = sht.LookupParameter("Sheet Number").AsString()
				sheet_name = sht.LookupParameter("Sheet Name").AsString()
				found_updateable_element = False
				for k in existing_vps:
					type_element = (k.GetTypeId()).IntegerValue
					if type_element_copy == type_element:
						found_updateable_element = True
						location = k.Location  
						if isinstance(location, DB.LocationPoint):
							new_location = element_copy.Location.Point  
							location.Point = new_location  
							k.ChangeTypeId(element_copy.GetTypeId())
							message_lines.append("{}-{} ----> Update location".format(sheet_number, sheet_name))
						elif isinstance(location, DB.LocationCurve):
							pass
			if not found_updateable_element:
				message_lines.append("{}-{} ----> {} Not Found Element To Update!".format(sheet_number, sheet_name, "*" * 20))
			message = "\n".join(message_lines)
			custom_message_box = CustomMessageBox(message)
			custom_message_box.ShowDialog()
	t.Commit()