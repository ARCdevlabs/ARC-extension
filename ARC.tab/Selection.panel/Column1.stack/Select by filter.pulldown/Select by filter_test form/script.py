# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import codecs
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import clr
clr.AddReference("System")
from System import Array
import System
import sys
import random
from System.Drawing import Size, Color, Font, FontStyle
from System import Drawing
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Form, SelectionMode , CheckedListBox,CheckedListBox, Keys, Button, TextBox, Label, Panel, MessageBox, SelectionMode, FormStartPosition
from System.Collections.Generic import List
import Autodesk
from Autodesk.Revit import DB
from Autodesk.Revit.DB import View, OverrideGraphicSettings, FilteredElementCollector,FillPatternTarget, ElementParameterFilter, FilterRule, ParameterFilterRuleFactory, FilterElement, FilteredElementCollector, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, ParameterFilterElement, Transaction, BuiltInParameter, BuiltInCategory, WallType, ElementId, FilterRule, ParameterFilterElement, ElementParameterFilter, ParameterFilterRuleFactory
import Autodesk.Revit.UI.Selection
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
view = doc.ActiveView
t = Transaction (doc, "Chọn đối tượng dựa vào filter")
t.Start()
def get_filter_elements():
    filter_elements = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()
    return filter_elements
all_view_filters = get_filter_elements()
name = []
for i in all_view_filters:
    name.append(Autodesk.Revit.DB.Element.Name.GetValue(i))
    name.sort()

def get_elements_by_view_filter(doc, view_filter):
    # Lấy tất cả các đối tượng trong view hiện tại
    collector = FilteredElementCollector(doc, doc.ActiveView.Id)
    all_elements = collector.ToElements()
    get_ele_filter = view_filter.GetElementFilter()
    # Tạo danh sách để lưu trữ các đối tượng thỏa mãn điều kiện của view filter
    selected_elements = []

    # Kiểm tra từng đối tượng xem nó có thỏa mãn view filter không
    for element in all_elements:
        if get_ele_filter.PassesFilter(element):
            selected_elements.append(element)
    return selected_elements


class MyForm(Form):
    def __init__(self):
        self.StartPosition = FormStartPosition.CenterScreen
        self.Text = "ARC: Chọn các đối tượng trong model dựa vào view filter"
        self.ShowIcon = False  #An icon nho
        self.Size = Size(520, 500)
        self.checkedListBox = CheckedListBox()
        items = Array[object](list(name))
        self.checkedListBox.Items.AddRange(items)
        self.checkedListBox.Size = Size(400, 300)
        self.checkedListBox.Location = Drawing.Point(10, 50)
        self.checkedListBox.CheckOnClick = False


        self.selectAllButton = Button()
        self.selectAllButton.Text = "Select All"
        self.selectAllButton.Location = Drawing.Point(420, 50)
        self.selectAllButton.Click += self.on_select_all_button_click

        self.nonebutton = Button()
        self.nonebutton.Text = "None"
        self.nonebutton.Location = Drawing.Point(420, 80)
        self.nonebutton.Click += self.on_none_click

        self.signatureLabel = Label()
        self.signatureLabel.Text = "nguyenthanhson1712@gmail.com"
        self.signatureLabel.Size = Size(485, 20)
        self.signatureLabel.Location = Drawing.Point(320, 440)


        # Ham nay de chon tat ca type tuong khi hien windowform
        default_checked = Array[object](list(name))
        for item in default_checked:
            index = self.checkedListBox.FindStringExact(item)
            if index != -1:
                self.checkedListBox.SetItemChecked(index, False)

        # self.checkedListBox.ItemCheck += self.on_item_check
        self.printButton = Button()
        self.printButton.Text = "Chọn"
        self.printButton.Location = Drawing.Point(420, 400)
        self.printButton.Click += self.on_print_button_click
        # Add the CheckedListBox to the Form
        self.Controls.Add(self.checkedListBox)
        self.Controls.Add(self.printButton)
        self.Controls.Add(self.selectAllButton)
        self.Controls.Add(self.nonebutton)
        self.Controls.Add(self.signatureLabel)

    def on_select_all_button_click(self, sender, e):
        for i in range(self.checkedListBox.Items.Count):
            self.checkedListBox.SetItemChecked(i, True)

    def on_none_click(self, sender, e):
        for i in range(self.checkedListBox.Items.Count):
            self.checkedListBox.SetItemChecked(i, False)

    def on_item_check(self, sender, e):
        checked_items = [self.checkedListBox.GetItemText(item) for item in self.checkedListBox.CheckedItems]
        print("Checked items:", checked_items)
    def on_checkedListBox_key_down(self, sender, e):
        if e.Control:
            e.Handled = True

    def on_print_button_click(self, sender, e):
        checked_items = [self.checkedListBox.GetItemText(item) for item in self.checkedListBox.CheckedItems]
        list_filter = []
        list_selected_element = []
        list_selected_element_thu_cap =[]
        for each_name in checked_items:  
            for filter in all_view_filters:
                if filter.Name == each_name:
                    list_filter.append(filter)
        # filter = doc.GetElement(filter_id)
        for filter in list_filter:
        # Sử dụng hàm get_elements_by_view_filter để lấy tất cả các đối tượng thỏa mãn view filter và lưu vào danh sách selected_elements
            selected_elements = get_elements_by_view_filter(doc, filter)
            list_selected_element.append(selected_elements)
            # Bây giờ selected_elements chứa tất cả các đối tượng mà view filter đang áp dụng
        for tung_doi_tuong in list_selected_element:
            for tung_doi_tuong_2 in tung_doi_tuong:
                list_selected_element_thu_cap.append(tung_doi_tuong_2)
        chon_doi_tuong = module.get_current_selection(uidoc,list_selected_element_thu_cap)
        self.Close()  
form = MyForm()

# Run the application
form.ShowDialog()
t.Commit()  


