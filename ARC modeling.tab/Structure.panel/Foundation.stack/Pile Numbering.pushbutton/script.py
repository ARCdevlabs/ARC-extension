# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
import Autodesk.Revit.UI.Selection
import sys
import os
import nances
if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Ele  = nances.get_elements(uidoc,doc, 'Select Piles', noti = False)

    from pyrevit import script
    logger = script.get_logger()
    my_config = script.get_config("parameter_pile_number")

    def load_configs():
        parameter_input = my_config.get_option("parameter_input", [])
        return parameter_input

    def save_configs(content):
        my_config.parameter_input = content
        script.save_config()

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

    # Lấy danh sách các cọc từ bộ lọc của Revit
    doc = __revit__.ActiveUIDocument.Document

    # Chỉ lấy các cọc có LocationPoint
    piles = [pile for pile in Ele if pile.Location and isinstance(pile.Location, LocationPoint)]


    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox,
                                Separator, Button, CheckBox)
    get_parameter = ''
    try:
        get_configs = load_configs()
        get_parameter = get_configs
    except:
        pass
    if get_parameter != None:
        config_parameter = get_parameter
    else:
        config_parameter = ''

    components = [
                    Label('Nhập số bắt đầu'),
                    TextBox('textbox1', Text="1"),
                    Label('Chọn cách lọc'),
                    ComboBox('combobox1', ['1. Phương X: Từ nhỏ đến lớn',
                                           '2. Phương X: Từ lớn đến nhỏ',
                                           '3. Phương Y: Từ nhỏ đến lớn',
                                           '4. Phương Y: Từ lớn đến nhỏ'
                                           ]),
                    Label('Parameter'),
                    TextBox('textbox2', Text = config_parameter),
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
        save_configs(parameter)
        get_parameter = load_configs()
    except:
        sys.exit()

    # Gọi hàm sắp xếp
    if method == '1. Phương X: Từ nhỏ đến lớn':
        sorted_piles = sort_piles_by(piles,"X", False)
    if method == '2. Phương X: Từ lớn đến nhỏ':
        sorted_piles = sort_piles_by(piles,"X", True)
    if method == '3. Phương Y: Từ nhỏ đến lớn':
        sorted_piles = sort_piles_by(piles,"Y", False)
    if method == '4. Phương Y: Từ lớn đến nhỏ':
        sorted_piles = sort_piles_by(piles,"Y", True)

    so_luong_coc = len(sorted_piles)
    try:
        convert_to_number = int(start_number)
    except:
        nances.message_box("Số bắt đầu không hợp lệ")
    # for number in range(convert_to_number, convert_to_number + so_luong_coc):
    #     print(number)
    t = Transaction (doc, "Pile Numbering")
    try:
        t.Start()
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
                # if method == '1. Phương X: Từ nhỏ đến lớn':
                #     convert_to_number += 1
                # if method == '2. Phương X: Từ lớn đến nhỏ':
                #     convert_to_number += 1
                # if method == '3. Phương Y: Từ nhỏ đến lớn':
                #     convert_to_number += 1
                # if method == '4. Phương Y: Từ lớn đến nhỏ':
                #     convert_to_number += 1                
            except:
                pass
        t.Commit()
    except:
        pass