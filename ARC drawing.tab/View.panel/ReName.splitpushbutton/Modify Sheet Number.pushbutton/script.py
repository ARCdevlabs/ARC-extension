# -*- coding: utf-8 -*-
import clr
import re
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import MessageBox
from pyrevit.forms import WPFWindow
from System.Windows import Window, SizeToContent, WindowStartupLocation, Thickness
from System.Windows.Controls import StackPanel, TextBlock, Button, ScrollViewer
__title__ = 'Sheet Renumber'

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
class CustomMessageBox(Window):
	def __init__(self, message):
		self.Title = "Thông Báo"
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
class ModalForm(WPFWindow):
	def __init__(self, xaml_file_name):
		WPFWindow.__init__(self, xaml_file_name)

		self.text1 = self.FindName("tien_to")
		self.text2 = self.FindName("so_bat_dau")
		self.text3 = self.FindName("hau_to")
		self.Combobox = self.FindName("kieu_so")
		self.text4 = self.FindName("Prefix")
		self.text5 = self.FindName("Suffix")

		self.OK = self.FindName("OK")
		self.ApplyToView = self.FindName("ApplyToView") 

		self.OK.Click += self.on_ok_click
		self.ApplyToView.Click += self.on_apply_to_view_click

		self.selected_elements1 = []
		self.list_sheet = []

	def select_elements(self):
		selection = uidoc.Selection.GetElementIds()
		self.selected_elements1 = selection
		self.list_sheet = []
		for i in selection:
			ele = doc.GetElement(i)
			if isinstance(ele, ViewSheet):
				sheet_number = ele.LookupParameter("Sheet Number").AsString()
				self.list_sheet.append(sheet_number)

	
	def value_input(self):
		ky_tu_ban_ve = str(self.text1.Text)
		so_bat_dau = int(self.text2.Text)
		Hau_to = str(self.text3.Text)
		kieu_seri = str(self.Combobox.SelectedItem.Content)
		prefix = str(self.text4.Text)
		suffix = str(self.text5.Text)
		return ky_tu_ban_ve, so_bat_dau, Hau_to, kieu_seri, prefix, suffix
	
	def check_sheet_number(self, list_sheet, prefix, suffix):
		if prefix and not suffix:
			order_numbers = []
			for sheet_number in list_sheet:
				len_prefix = len(prefix)
				len_suffix = len(suffix)
				len_sheet_number = len(sheet_number)
				if sheet_number.startswith(prefix):
					order_number = sheet_number[len_prefix:]
					order_number_cleaned = re.sub(r'[_/-]', '.', order_number)
					try:
						order_number_value = float(order_number_cleaned) if order_number_cleaned else None
						order_numbers.append((sheet_number, order_number_value))
					except ValueError:
						MessageBox.Show("Sheet Number " + sheet_number + " chứa ký tự chữ nên không thể sắp xếp")
						continue  
			sorted_list_sheet = sorted(order_numbers, key=lambda x: x[1])
		elif suffix and not prefix:
			order_numbers = []
			for sheet_number in list_sheet:
				len_prefix = len(prefix)
				len_suffix = len(suffix)
				len_sheet_number = len(sheet_number)
				if sheet_number.endswith(suffix):
					order_number = sheet_number[:-len_suffix]
					order_number_cleaned = re.sub(r'[_/-]', '.', order_number)
					try:
						order_number_value = float(order_number_cleaned) if order_number_cleaned else None
						order_numbers.append((sheet_number, order_number_value))
					except ValueError:
						MessageBox.Show("Sheet Number " + sheet_number + " chứa ký tự chữ nên không thể sắp xếp")
						continue  

			sorted_list_sheet = sorted(order_numbers, key=lambda x: x[1])

		elif prefix and suffix:
			order_numbers = []
			for sheet_number in list_sheet:
				len_prefix = len(prefix)
				len_suffix = len(suffix)
				len_sheet_number = len(sheet_number)
				if sheet_number.startswith(prefix) and sheet_number.endswith(suffix):
					order_number = sheet_number[len_prefix:len_sheet_number - len_suffix]
					order_number_cleaned = re.sub(r'[_/-]', '.', order_number)
					try:
						order_number_value = float(order_number_cleaned) if order_number_cleaned else None
						order_numbers.append((sheet_number, order_number_value))
					except ValueError:
						MessageBox.Show("Sheet Number " + sheet_number + " chứa ký tự chữ nên không thể sắp xếp")
						continue  

			sorted_list_sheet = sorted(order_numbers, key=lambda x: x[1])

		else:
			sorted_list_sheet = sorted(list_sheet)  
		return sorted_list_sheet

	def on_ok_click(self, sender, e):
		
		ky_tu_ban_ve, so_bat_dau, Hau_to, kieu_seri, prefix, suffix = self.value_input()
		if not self.list_sheet:
			self.select_elements()
		sorted_list_sheet = self.check_sheet_number(self.list_sheet, prefix, suffix)
		if not sorted_list_sheet:
			MessageBox.Show("Ký tự Prefix & Suffix của Sheet number hiện tại không hợp lý, Vui lòng kiểm tra lại!")
			return
		zfill_length = len(kieu_seri)
		count = so_bat_dau
		message_lines = ["KẾT QUẢ VAR", "Kiểm tra thứ tự sắp xếp của Sheet number hiện tại", "Nếu thứ tự của Sheet number hiện tại đúng thì số thứ tự sẽ đổi đúng !","-" * 75 ]
		for item in sorted_list_sheet:
			if isinstance(item, tuple):
				sheet_number = item[0]
			else:
				sheet_number = item
			sheet_number_new = str(ky_tu_ban_ve + str(count).zfill(zfill_length) + Hau_to)
			message_lines.append("Sheet number hiện tại: {} -------> Sheet number mới: {}".format(sheet_number, sheet_number_new))
			count += 1
		message = "\n".join(message_lines)
		custom_message_box = CustomMessageBox(message)
		custom_message_box.ShowDialog()

	def on_apply_to_view_click(self, sender, e):
		t = Transaction(doc, 'Sheet Renumber')
		t.Start()
		ky_tu_ban_ve, so_bat_dau, Hau_to, kieu_seri, prefix, suffix = self.value_input()
		self.select_elements()
		sorted_list_sheet = self.check_sheet_number(self.list_sheet, prefix, suffix)
		if not sorted_list_sheet:
			MessageBox.Show("Ký tự Prefix & Suffix của Sheet number hiện tại không hợp lý, Vui lòng kiểm tra lại!")
			t.RollBack()  
			return
		zfill_length = len(kieu_seri)
		count = so_bat_dau
		sheet_set =[]
		message_lines = ["ĐÃ ÁP DỤNG SHEET NUMBER MỚI VÀO REVIT !","-" * 52 ]
		for item in sorted_list_sheet:
			if isinstance(item, tuple):
				sheet_number = item[0]
			else:
				sheet_number = item
			sheet_number_new = str(ky_tu_ban_ve + str(count).zfill(zfill_length) + Hau_to)
			sheet_number_new_with_z = str(ky_tu_ban_ve + str(count).zfill(zfill_length) + Hau_to +"z")
			message_lines.append("Sheet number hiện tại: {} -------> Sheet number mới: {}".format(sheet_number, sheet_number_new))
			count += 1
			for i in self.selected_elements1:
				ele = doc.GetElement(i)
				if isinstance(ele, ViewSheet) and ele.LookupParameter("Sheet Number").AsString() == sheet_number:
					ele.LookupParameter("Sheet Number").Set(sheet_number_new_with_z)
					sheet_set.append(ele)
		for ele in sheet_set:
			current_sheet_number_with_z = ele.LookupParameter("Sheet Number").AsString()
			if current_sheet_number_with_z.endswith("z"):
				new_sheet_number = current_sheet_number_with_z[:-1]
				ele.LookupParameter("Sheet Number").Set(new_sheet_number)
			else:
				print("Lỗi sheets không có z")
				break
		t.Commit()
		self.Close()
		message = "\n".join(message_lines)
		custom_message_box = CustomMessageBox(message)
		custom_message_box.ShowDialog()
if __name__ == "__main__":
	form = ModalForm('SheetReNumber.xaml')
	form.ShowDialog()

