# -*- coding: utf-8 -*-
__doc__ = 'nguyenthanhson1712@gmail.com'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import Autodesk
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FailuresAccessor
from Autodesk.Revit.DB import Line
from Autodesk.Revit.Creation import ItemFactoryBase
from System.Collections.Generic import *
from Autodesk.Revit.DB import Reference
import math
import sys
import string
import importlib
import traceback
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
#Get Document 
from Autodesk.Revit.UI.Selection import ObjectType, Selection
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document

    def tao_sheet (idoc, id_khung_ban_ve):
        new_sheet = Autodesk.Revit.DB.ViewSheet.Create(idoc,id_khung_ban_ve)
        return new_sheet
    
    def dat_view_vao_sheet (idoc, sheet_id, view_id, point):
        kiem_tra = Autodesk.Revit.DB.Viewport.CanAddViewToSheet(idoc,sheet_id, view_id)
        if kiem_tra:
            new_viewport = Autodesk.Revit.DB.Viewport.Create(idoc, sheet_id, view_id, point)
        return new_viewport
    def lay_khung_ban_ve (viewsheet):
        filter = ElementClassFilter(FamilyInstance)
        get_dependent_element = viewsheet.GetDependentElements(filter)
        return get_dependent_element

    def lay_het_title_block (idoc):
        title_block_collector = FilteredElementCollector(idoc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsElementType().ToElements()

        # Danh sách chứa tên các loại title block
        title_block_types = []
        title_block_family_name = []

        # Lặp qua từng title block family và lấy tên các loại
        for title_block in title_block_collector:
            if isinstance(title_block, FamilySymbol):
                title_block_types.append(title_block)
                title_block_family_name.append(title_block.FamilyName)
        return title_block_types, title_block_family_name


    Ele_chua_sort = module.get_selected_elements(uidoc,doc)
    # for tung_element in Ele:
        # name_view = Autodesk.Revit.DB.Element.Name.GetValue(tung_element)
        # Ele.sort(key=lambda name_view: str(name_view))
    # Ele.sort(key=lambda x: x.Name)
    try:
        Ele = sorted(Ele_chua_sort, key=lambda x: x.GenLevel.Elevation)
    except:
        Ele = Ele_chua_sort
    # Ele = sorted(Ele_sort_name, key=lambda x: x.GenLevel)
 
    # for test in Ele:
    #     print (Autodesk.Revit.DB.Element.Name.GetValue(test))
    t = Transaction (doc, "Tạo sheet và đặt view vào sheet")
    t.Start()
    # id_khung_ban_ve = ElementId(3025922)
    all_khung_all_family_name = lay_het_title_block(doc)
    all_khung = all_khung_all_family_name[0]
    all_all_family_name = all_khung_all_family_name[1]
    list_new_format =[]
    for khung, family_name in zip(all_khung,all_all_family_name):
        new_format = str(family_name) + ": " + str(Autodesk.Revit.DB.Element.Name.GetValue(khung))
        list_new_format.append(new_format)
    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                Separator, Button, CheckBox)
    components = [Label('Chọn family khung tên:'),
                    ComboBox('combobox1', [x for x in list_new_format]),
                    Label('Giá trị Sheet Number đầu tiên (VD: S01-01)'),
                    TextBox('textbox1', Text="S01-01"),
                #   CheckBox('checkbox1', 'Check this'), (khong can check box)
                    Separator(),
                    Button('Tạo sheet')]
    form = FlexForm('ARC tools', components)
    form.show()
    # User selects `Opt 1`, types 'Wood' in TextBox, and select Checkbox
    form.values
    selected_title_block= form.values["combobox1"]
    sheet_number  = form.values["textbox1"]
    ky_tu_cuoi = sheet_number[-2:]
    cac_ky_tu_dau = sheet_number[:-2]
    chuyen_thanh_so = int(ky_tu_cuoi)
    for type_khung_bv, family_name_bv in zip(all_khung,all_all_family_name):
        if (str(family_name_bv) + ": " + str(Autodesk.Revit.DB.Element.Name.GetValue(type_khung_bv))) == str(selected_title_block):    
            id_khung_ban_ve = type_khung_bv.Id  
    for i in Ele:
        name = Autodesk.Revit.DB.Element.Name.GetValue(i)
        sheet_moi = tao_sheet(doc,id_khung_ban_ve)
        kiem_tra_co_bo_tri_sheet_duoc_khong = Autodesk.Revit.DB.Viewport.CanAddViewToSheet(doc,sheet_moi.Id, i.Id)
        sheet_moi.Name = name
        if kiem_tra_co_bo_tri_sheet_duoc_khong:
            dat_view_vao_sheet(doc,sheet_moi.Id,i.Id, XYZ(420.5/304.8,297/304.8,0))
            # khung_ban_ve_Id = lay_khung_ban_ve (sheet_moi)
            # hung_ban_ve = doc.GetElement(khung_ban_ve_Id[0])
            # width = module.get_parameter_value_by_name (hung_ban_ve, "Sheet Width")
            # print width
            sheet_moi_number = sheet_moi.SheetNumber
            sheet_number = str(cac_ky_tu_dau) + str(chuyen_thanh_so).zfill(2)
            # sheet_moi_number = str(sheet_number)
            module.get_builtin_parameter_by_name(sheet_moi, BuiltInParameter.SHEET_NUMBER).Set(sheet_number)
            chuyen_thanh_so += 1
        else:
            module.message_box("View đã có trong sheet khác rồi: " + str(i.Name))
    t.Commit()
