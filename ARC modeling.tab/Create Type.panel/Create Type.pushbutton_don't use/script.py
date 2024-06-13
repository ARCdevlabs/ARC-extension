# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
import System.Windows.Forms as WinForms
import xlrd
# import lxml
import sys
from pyrevit import revit, DB
__doc__ = 'nguyenthanhson1712@gmail.com'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import*
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Element
from System.Collections.Generic import *
import math
from rpw import ui
from rpw.ui.forms import Alert
#Get UIDocument
uidoc = __revit__.ActiveUIDocument
#Get Document 
doc = uidoc.Document
# Ham de tim kiem loai co cung ten trong family

from Autodesk.Revit.DB import FilteredElementCollector

# Lấy tất cả các loại đối tượng từ mô hình
type_collector = FilteredElementCollector(doc).OfClass(ElementType)

# # Duyệt qua danh sách các loại đối tượng và in ra tên của chúng
# for type_element in type_collector:
#     print(type_element.Name)

# import pandas as pd

# data = pd.read_excel(dialog.FileName)


# type_ban_dau = doc.GetElement(ElementId(5240815))

dialog = WinForms.OpenFileDialog()
dialog.Filter = "Excel Files (*.xlsx)|*.xlsx"
dialog.Title = "Select an Excel file"
clr.AddReference("Microsoft.Office.Interop.Excel")
from Microsoft.Office.Interop.Excel import ApplicationClass
excel_app = ApplicationClass()
if dialog.ShowDialog() == WinForms.DialogResult.OK:
    # workbook = xlrd.open_workbook(dialog.FileName)
    file_path = dialog.FileName
    workbook = excel_app.Workbooks.Open(file_path)
    # print dir(workbook)
    list_sheet_names = []
    list_sheets = []
    for number in range(1,100):
        try:
            list_sheet_names.append(workbook.Sheets[number].Name)
            list_sheets.append(workbook.Sheets[number])
        except:
            pass

    module.message_box("Tiếp theo, hãy chọn một đối tượng mẫu ban đầu để bắt đầu duplicate")


    pick = uidoc.Selection.PickObject(ObjectType.Element)
    covert_reference_to_element = []
    doi_tuong_dau_tien = doc.GetElement(pick.ElementId)
    category = doi_tuong_dau_tien.Category
    # print category.Name
    symbol = doi_tuong_dau_tien.Symbol
    family = symbol.Family
    types_collector = FilteredElementCollector(doc).OfClass(symbol.GetType())
    list_type = []
    list_type_name = []
    for type in types_collector:
        # print type.Category.Name
        if type.Category.Name == category.Name:
            if type.Family.Name == family.Name:
                list_type.append(type)
                list_type_name.append(Autodesk.Revit.DB.Element.Name.GetValue(type))
                # print Autodesk.Revit.DB.Element.Name.GetValue(type)
        # print Autodesk.Revit.DB.Element.Name.GetValue(type)


    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                Separator, Button, CheckBox)
    components = [Label('Chọn tên sheet excel đã nhập data'),
                    ComboBox('combobox1', [x for x in list_sheet_names]),
                    Label('Chọn type cần duplicate'),
                    ComboBox('combobox2', [x for x in list_type_name]),
                    Separator(),
                    Button('Tạo type')]
    form = FlexForm('ARC tools', components)
    form.show()
    form.values

    sheet_da_chon = form.values["combobox1"]

    type_da_chon = form.values["combobox2"]

    for tung_sheet, tung_sheet_name in zip(list_sheets,list_sheet_names):
        if tung_sheet_name == sheet_da_chon:
            sheet = tung_sheet
    # sheet = workbook.sheet_by_index(0)
            

    for y,z in zip(list_type,list_type_name):
        if z == type_da_chon:
            type_ban_dau = y

        
    # data=[]
    # for row_idx in range(sheet.nrows):
    #     row_data = []
    #     for col_idx in range(sheet.ncols):
    #         row_data.append(sheet.cell_value(row_idx, col_idx))
    #     data.append(row_data)

    # import unicode
    data = []
    for row in range(1, sheet.UsedRange.Rows.Count + 1 ):
        row_data = []
        for column in range(1, sheet.UsedRange.Columns.Count + 1):
            cell_value = sheet.Cells[row, column].Value2
            # print dir(cell_value), cell_value
            # if isinstance(cell_value_1, unicode):
            #     cell_value = cell_value_1
            # else:
            #     cell_value = unicode_string()
            row_data.append(cell_value)
        data.append(row_data)
        
    workbook.Close()
    excel_app.Quit()


    # print data
    transposed_data = [[row[i] for row in data] for i in range(len(data[0]))]
    data_para_va_type = data[0]
    data_para  = data_para_va_type[1:]
    data_type = transposed_data[0]
    data_gia_tri_va_type = data[1:]
    # print data_gia_tri_va_type
    list_gia_tri = []
    for tung_data in data_gia_tri_va_type:
        list_gia_tri.append(tung_data[1:])
    # print list_gia_tri
    # print data_para
    list_sau_khi_dup = []

    tx = Transaction(doc, "Duplicate Type từ file excel")
    tx.Start()
    list_bi_trung =[]
    for tung_cell in data_type[1:]:
        # print tung_cell
        try:
            duplicate_type = type_ban_dau.Duplicate(str(tung_cell))
            list_sau_khi_dup.append(duplicate_type)
        except:
            list_bi_trung.append(str(tung_cell))
            pass
    if len(list_bi_trung) > 0:
        tin_nhan = "Những Type đã bị trùng, hãy kiểm tra lại" + str(list_bi_trung)
        module.message_box(tin_nhan)
        sys.exit()
    # for i, j in zip(data_para[0], data_gia_tri):
    #     print i, j
    
    for index, tung_para in enumerate(data_para):
        # print tung_para
        # print tung_para
        # print list_gia_tri
        # print transposed_list_gia_tri
        # for tung_type in list_sau_khi_dup:
        so_luong = 0
        for index_2, tung_type in enumerate(list_sau_khi_dup):
            list_gia_tri_index = list_gia_tri[index_2]
            gia_tri_trong_list_gia_tri_index = list_gia_tri_index[index]
            # print gia_tri_trong_list_gia_tri_index
            get_para = module.get_parameter_by_name(tung_type, tung_para)
            storage = get_para.StorageType
            try:
                if str(storage) == "String":
                    set_para = module.set_parameter_value_by_name(tung_type, tung_para, str(gia_tri_trong_list_gia_tri_index))
                else:
                    set_para = module.set_parameter_value_by_name(tung_type, tung_para, float(gia_tri_trong_list_gia_tri_index)/304.8)
            except:
                module.message_box("Kiểm tra lại parameter đã nhập đúng chưa, kiểm tra có nhập nhầm dạng dữ liệu text và number không")
                import sys
                sys.exit()
            so_luong += 1
    type_va_para_da_tao = "Đã tạo " + str(so_luong) + " type"
    module.message_box(type_va_para_da_tao)
    tx.Commit()