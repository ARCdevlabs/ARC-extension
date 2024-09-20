
# -*- coding: utf-8 -*-
import clr
import re
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference("System.Windows.Forms")
from pyrevit.forms import WPFWindow
from System.Windows import Window, WindowStartupLocation
from System.Windows.Controls import TextBlock, Button, StackPanel
from System.Windows import Thickness, SizeToContent


uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
class CustomMessageBox(Window):
	def __init__(self, message):
		self.Title = "Thông Báo"
		self.SizeToContent = SizeToContent.WidthAndHeight  # Tự động điều chỉnh kích thước
		self.WindowStartupLocation = WindowStartupLocation.CenterScreen

		stack_panel = StackPanel()
		self.Content = stack_panel

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

		self.OK = self.FindName("OK")  # Tìm nút OK
		self.ApplyToView = self.FindName("ApplyToView")  # Tìm nút ApplyToView

		self.OK.Click += self.on_ok_click  # Liên kết sự kiện nhấp nút OK
		self.ApplyToView.Click += self.on_apply_to_view_click  # Liên kết sự kiện nhấp nút ApplyToView

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
				pos = sheet_number.find(prefix)
				if pos != -1:  # Nếu tìm thấy prefix
					order_number = sheet_number[pos + len(prefix):]
					order_number_cleaned = re.sub(r'[_/-]', '.', order_number)
					try:
						order_number_value = float(order_number_cleaned) if order_number_cleaned else None
						order_numbers.append((sheet_number, order_number_value))
					except ValueError:
						continue  # Bỏ qua nếu không thể chuyển đổi

			# Sắp xếp theo giá trị số
			sorted_list_sheet = sorted(order_numbers, key=lambda x: x[1])

		elif suffix and not prefix:
			order_numbers = []
			for sheet_number in list_sheet:
				pos = sheet_number.find(suffix)
				if pos != -1:  # Nếu tìm thấy suffix
					order_number = sheet_number[:pos]  # Lấy phần trước suffix
					order_number_cleaned = re.sub(r'[_/-]', '.', order_number)
					try:
						order_number_value = float(order_number_cleaned) if order_number_cleaned else None
						order_numbers.append((sheet_number, order_number_value))
					except ValueError:
						continue  # Bỏ qua nếu không thể chuyển đổi

			sorted_list_sheet = sorted(order_numbers, key=lambda x: x[1])

		elif prefix and suffix:  # Nếu có cả prefix và suffix
			order_numbers = []

			for sheet_number in list_sheet:
				pos_prefix = sheet_number.find(prefix)
				pos_suffix = sheet_number.find(suffix)
				if pos_prefix != -1 and pos_suffix != -1 and pos_prefix < pos_suffix:  # Kiểm tra vị trí
					order_number = sheet_number[pos_prefix + len(prefix):pos_suffix]  # Lấy phần giữa
					order_number_cleaned = re.sub(r'[_/-]', '.', order_number)
					try:
						order_number_value = float(order_number_cleaned) if order_number_cleaned else None
						order_numbers.append((sheet_number, order_number_value))
					except ValueError:
						continue  # Bỏ qua nếu không thể chuyển đổi

			sorted_list_sheet = sorted(order_numbers, key=lambda x: x[1])

		else:  # Khi cả prefix và suffix không có giá trị
			sorted_list_sheet = sorted(list_sheet)  
		return sorted_list_sheet

	def on_ok_click(self, sender, e):
		
		ky_tu_ban_ve, so_bat_dau, Hau_to, kieu_seri, prefix, suffix = self.value_input()
		if not self.list_sheet:
			self.select_elements()
		sorted_list_sheet = self.check_sheet_number(self.list_sheet, prefix, suffix)
		zfill_length = len(kieu_seri)
		count = so_bat_dau
		message_lines = ["KẾT QUẢ VAR", "Kiểm tra thứ tự sắp xếp của sheet number cũ, nếu thứ tự của sheet number cũ đúng thì số thứ tự sẽ duỗi đúng !","-" * 123 ]
		for item in sorted_list_sheet:
			if isinstance(item, tuple):
				sheet_number = item[0]  # Lấy sheet_number từ tuple
			else:
				sheet_number = item  # Nếu là chuỗi
			sheet_number_new = str(ky_tu_ban_ve + str(count).zfill(zfill_length) + Hau_to)
			message_lines.append("Sheet number mới: {} ________ Sheet number cũ: {}".format(sheet_number_new, sheet_number))
			count += 1
		message = "\n".join(message_lines)
		custom_message_box = CustomMessageBox(message)
		custom_message_box.ShowDialog()

	def on_apply_to_view_click(self, sender, e):
		t = Transaction(doc, 'Đánh sheet number')
		t.Start()
		ky_tu_ban_ve, so_bat_dau, Hau_to, kieu_seri, prefix, suffix = self.value_input()
		self.select_elements()
		sorted_list_sheet = self.check_sheet_number(self.list_sheet, prefix, suffix)
		zfill_length = len(kieu_seri)
		count = so_bat_dau
		sheet_set =[]
		message_lines = ["ĐÃ ÁP DỤNG SHEET NUMBER MỚI VÀO REVIT !","-" * 52 ]
		for item in sorted_list_sheet:
			if isinstance(item, tuple):
				sheet_number = item[0]  # Lấy sheet_number từ tuple
			else:
				sheet_number = item  # Nếu là chuỗi
			sheet_number_new = str(ky_tu_ban_ve + str(count).zfill(zfill_length) + Hau_to)
			sheet_number_new_with_z = str(ky_tu_ban_ve + str(count).zfill(zfill_length) + Hau_to+"z")
			message_lines.append("Sheet number mới: {} ________ Sheet number cũ: {}".format(sheet_number_new, sheet_number))
			count += 1
			for i in self.selected_elements1:
				ele = doc.GetElement(i)
				if isinstance(ele, ViewSheet) and ele.LookupParameter("Sheet Number").AsString() == sheet_number:
					ele.LookupParameter("Sheet Number").Set(sheet_number_new_with_z)
					sheet_set.append(ele)
		for ele in sheet_set:
			current_sheet_number_with_z = ele.LookupParameter("Sheet Number").AsString()
			if current_sheet_number_with_z.endswith("z"):
				new_sheet_number = current_sheet_number_with_z[:-1]  # Loại bỏ ký tự "z"
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
	form = ModalForm('DuoiSheetNumber.xaml')
	form.ShowDialog()

