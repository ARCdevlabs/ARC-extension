# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
import traceback
from Autodesk.Revit.UI.Selection import ObjectType, Selection
from pyrevit import revit, UI, script
import nances
if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    def all_type_of_framing(doc):
        list_all_type_of_framing = []
        all_type_of_framing = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_StructuralFraming)
        for tung_dam in all_type_of_framing:
            family_name = nances.get_builtin_parameter_by_name(tung_dam,BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM).AsString()
            type_name = nances.get_builtin_parameter_by_name(tung_dam,BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
            family_name_type_name = family_name + ":" + type_name
            list_all_type_of_framing.append(family_name_type_name) 
            list_all_type_of_framing.sort()       
        return list_all_type_of_framing

    logger = script.get_logger()
    my_config = script.get_config("setting_type_beam_by_detail_line")

    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox,
                                Separator, Button)
    
    def load_configs_type_dam():
        type_mac_dinh = "MK_梁〈RC〉:1G1"
        beam_type_input = my_config.get_option("beam_type_input", [])
        beam_type = beam_type_input or type_mac_dinh
        return beam_type

    def save_configs_type_dam(content):
        my_config.beam_type_input = content
        script.save_config()

    def load_configs_phuong():
        phuong_mac_dinh = "Tự do"
        phuong_input = my_config.get_option("phuong_dam", [])        
        phuong_value = phuong_input or phuong_mac_dinh
        return phuong_value
    
    def save_configs_phuong(content):
        my_config.phuong_dam = content
        script.save_config()

    def load_configs_extend():
        extend_mac_dinh = "2500"
        extend_input = my_config.get_option("extend", [])        
        extend_value = extend_input or extend_mac_dinh
        return extend_value
    
    def save_configs_extend(content):
        my_config.extend = content
        script.save_config()


    '''Load configs để lấy giá trị đã lưu vào trong .ini'''
    gia_tri_load_configs_type_dam = load_configs_type_dam() #kết quả là 1G1 theo mặc định hoặc là các kết quả khác 
    list_type_dam = all_type_of_framing(doc)
    if len(list_type_dam) == 0:
        nances.message_box("Don't have type beam in the model")
        import sys
        sys.exit()
    try:
        index_load_configs_phuong = list_type_dam.index(gia_tri_load_configs_type_dam) #kết quả là 0 hoặc 1 hoặc 2
    except Exception as e:
        index_load_configs_phuong = 0
        pass
    index_mac_dinh_type_dam = list_type_dam[index_load_configs_phuong] #kết quả là Tự do hoặc phương dọc hoặc phương ngang.


    '''Load configs để lấy giá trị đã lưu vào trong .ini'''
    gia_tri_load_configs_phuong = load_configs_phuong() #kết quả là Tự do hoặc phương dọc hoặc phương ngang.
    phuong_mac_dinh = ["Tự do","Phương dọc", "Phương ngang"]
    index_load_configs_phuong = phuong_mac_dinh.index(gia_tri_load_configs_phuong) #kết quả là 0 hoặc 1 hoặc 2
    index_mac_dinh_phuong = phuong_mac_dinh[index_load_configs_phuong] #kết quả là Tự do hoặc phương dọc hoặc phương ngang.


    load_gia_tri_extend = load_configs_extend()

    #ComboBox('combobox2', phuong_mac_dinh,default=index_mac_dinh, sort=False) ở dòng này, 
    # sort để thành False nếu không combobox sẽ sắp xếp mặc định theo bảng chữ cái
    components = [Label('Chọn type của dầm:'),
                ComboBox('combobox1', list_type_dam, default=index_mac_dinh_type_dam,sort=False),
                Separator(),
                Label('Chọn phương muốn vẽ dầm:'),
                ComboBox('combobox2', phuong_mac_dinh, default = index_mac_dinh_phuong, sort=False), 
                Separator(),
                Label('Nhập giá trị mở rộng 2 đầu dầm:'),
                TextBox('textbox1',load_gia_tri_extend),
                Separator(),
                Button('Finish Setting')]
    
    if __name__ == "__main__":
        form = FlexForm('ARC', components)
        form.show()
        form.values
        try:
            selected_framing_type_name = form.values["combobox1"]
            phuong_dam = form.values["combobox2"]
            extend = form.values["textbox1"]
        except:
            import sys
            sys.exit()

        save_configs_type_dam(selected_framing_type_name)
        save_configs_phuong(phuong_dam)
        save_configs_extend(extend)





