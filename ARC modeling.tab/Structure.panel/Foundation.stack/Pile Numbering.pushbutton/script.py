# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
import Autodesk.Revit.UI.Selection
import sys
import os
import nances
from nances import selection
from pyrevit import script
logger = script.get_logger()


if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document

    logger = script.get_logger()
    my_config = script.get_config("setting_danh_so_coc")
    def load_configs_so_bat_dau():
        so_mac_dinh = "1"
        get_so_bat_dau = my_config.get_option("so_bat_dau", [])
        tra_ve_so_bat_dau = get_so_bat_dau or so_mac_dinh
        return tra_ve_so_bat_dau

    def save_configs_so_bat_dau(content):
        my_config.so_bat_dau = content
        script.save_config()

    def load_configs_thu_tu_tang():
        thu_tu_mac_dinh = "1. Phương X: Từ nhỏ đến lớn"
        get_thu_tu_tang = my_config.get_option("thu_tu_tang", [])
        tra_ve_thu_tu_tang = get_thu_tu_tang or thu_tu_mac_dinh
        return tra_ve_thu_tu_tang

    def save_configs_thu_tu_tang(content):
        my_config.thu_tu_tang = content
        script.save_config()

    def load_configs_parameter_danh_so():
        parameter_mac_dinh = "番号"
        get_parameter_danh_so = my_config.get_option("parameter_danh_so", [])
        tra_ve_parameter_danh_so = get_parameter_danh_so or parameter_mac_dinh
        return tra_ve_parameter_danh_so

    def save_configs_parameter_danh_so(content):
        my_config.parameter_danh_so = content
        script.save_config()

    def xoay_list(lst, gia_tri):
        if gia_tri not in lst:
            return lst

        index = lst.index(gia_tri)

        return lst[index:] + lst[:index]
    
    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox,
                                Separator, Button, CheckBox)
    
    source_so_bat_dau = load_configs_so_bat_dau()
    source_thu_tu_tang = load_configs_thu_tu_tang()
    source_parameter = load_configs_parameter_danh_so()
    list_dau_vao_combobox = ['1. Phương X: Từ nhỏ đến lớn',
                                        '2. Phương X: Từ lớn đến nhỏ',
                                        '3. Phương Y: Từ nhỏ đến lớn',
                                        '4. Phương Y: Từ lớn đến nhỏ'
                                        ]
    xoay_list_theo_dau_vao = xoay_list(list_dau_vao_combobox, source_thu_tu_tang)

    components = [
                Label('Nhập số bắt đầu'),
                TextBox('textbox1', source_so_bat_dau),
                Label('Chọn cách lọc'),
                ComboBox('combobox1', xoay_list_theo_dau_vao,sort=False),
                Label('Parameter'),
                TextBox('textbox2',source_parameter),
                Separator(),
                Button('Ok')
            ]
    form = FlexForm('ARC', components)
    form.show()
    form.values    
    try:
        start_number = form.values["textbox1"]
        method = form.values["combobox1"]
        parameter = form.values["textbox2"]
        save_configs_so_bat_dau(start_number)
        save_configs_thu_tu_tang(method)
        save_configs_parameter_danh_so(parameter)

    except:
        sys.exit()

    try:
        convert_to_number = int(start_number)
    except:
        nances.message_box("Số bắt đầu không hợp lệ")
    def main(convert_to_number):
        # Bat dau vong lap lua chon
        run = True
        while run == True:
            try:    # Chỉ lấy các cọc có LocationPoint
                def sort_piles_by(piles, direction, reverse = False):
                    try:
                        # Lấy tọa độ X của từng cọc, nếu có LocationPoint
                        if direction == "X" and reverse == False:
                            sorted_piles = sorted(piles, key=lambda pile: pile.Location.Point.X)
                        if direction == "X" and reverse == True:
                            sorted_piles = sorted(piles, key=lambda pile: pile.Location.Point.X, reverse = True)
                        if direction == "Y" and reverse == False:
                            sorted_piles = sorted(piles, key=lambda pile: pile.Location.Point.Y)
                        if direction == "Y" and reverse == True:
                            sorted_piles = sorted(piles, key=lambda pile: pile.Location.Point.Y, reverse = True)
                        return sorted_piles
                    except:
                        pass
                # Ele  = nances.get_elements(uidoc,doc, 'Select Piles', noti = False)
                try:
                    # pick_elements = nances.pick = uidoc.Selection.PickObjects(Autodesk.Revit.UI.Selection.ObjectType.Element)
                    Ele = []
                    Ele = selection.pick_model_by_rectangle(uidoc)
                    if Ele:
                        run = True
                        # for tung_ele in pick_elements:
                        #     Ele.append(doc.GetElement(tung_ele.ElementId))
                    else:
                        run = False
                except:
                    run = False
                    Ele = []
                    pass
                piles = [pile for pile in Ele if pile.Location and isinstance(pile.Location, LocationPoint)]
                # Gọi hàm sắp xếp
                if method == '1. Phương X: Từ nhỏ đến lớn':
                    sorted_piles = sort_piles_by(piles,"X", False)
                if method == '2. Phương X: Từ lớn đến nhỏ':
                    sorted_piles = sort_piles_by(piles,"X", True)
                if method == '3. Phương Y: Từ nhỏ đến lớn':
                    sorted_piles = sort_piles_by(piles,"Y", False)
                if method == '4. Phương Y: Từ lớn đến nhỏ':
                    sorted_piles = sort_piles_by(piles,"Y", True)
                t = Transaction (doc, "Pile Numbering")
                t.Start()
                try:                   
                    for pile in sorted_piles:
                        try:
                            get_para = nances.get_parameter_by_name(pile, str(parameter))
                            storage_type = get_para.StorageType
                            if str(storage_type) == "String":
                                get_para.Set(str(convert_to_number))
                                convert_to_number += 1
                            if str(storage_type) == "Double" or str(storage_type) == "Integer":
                                get_para.Set(convert_to_number)
                                convert_to_number += 1  
                        except:
                            pass
                    t.Commit()
                except:
                    t.RollBack()
                    pass
            except Exception as ex:
                run = False
                if "Operation canceled by user." in str(ex):
                    run = False
                    break
                else:
                    run = False
                    break
    main(convert_to_number)