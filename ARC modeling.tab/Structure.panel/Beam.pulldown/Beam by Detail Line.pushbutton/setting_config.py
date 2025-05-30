# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
import traceback
from Autodesk.Revit.UI.Selection import ObjectType, Selection
from pyrevit import revit, UI, script
import nances as module
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    def all_type_of_framing():
        all_type_of_framing = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_StructuralFraming)
        return all_type_of_framing

    logger = script.get_logger()
    my_config = script.get_config("setting_type_beam_by_detail_line")

    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox,
                                Separator, Button, CheckBox)
    all_type_framing = all_type_of_framing()
    components = [Label('Chọn type của dầm:'),
                    ComboBox('combobox1', [DB.Element.Name.GetValue(x) for x in all_type_framing]),
                    Separator(),
                    Label('Chọn phương muốn vẽ dầm:'),
                    ComboBox('combobox2', ["Phương dọc", "Phương ngang","Tự do"]),
                    Separator(),
                    Label('Nhập giá trị mở rộng 2 đầu dầm:'),
                    TextBox('textbox1','2500'),
                    Separator(),
                    Button('Finish Setting')]

    def load_configs():
        beam_type_input = my_config.get_option("beam_type_input", [])
        beam_type = [beam_type_input]
        return beam_type

    def save_configs(content):
        """Save given list of categories as frequently selected"""
        my_config.beam_type_input = content
        script.save_config()
        
    if __name__ == "__main__":
        form = FlexForm('ARC', components)
        form.show()
        form.values
        input = []
        try:
            selected_framing_type = form.values["combobox1"]
            phuong_dam = form.values["combobox2"]
            extend = form.values["textbox1"]

        except:
            import sys
            sys.exit()
        input.append(selected_framing_type)
        input.append(phuong_dam)
        input.append(extend)

        prev_framing_type = load_configs()
        beam_type_input_2 = input
        save_configs(beam_type_input_2)





