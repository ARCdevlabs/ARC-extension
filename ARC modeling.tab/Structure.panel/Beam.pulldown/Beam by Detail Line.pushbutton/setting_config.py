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

    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                                Separator, Button, CheckBox)
    all_type_framing = all_type_of_framing()
    components = [Label('Select type of Beam:'),
                    ComboBox('combobox1', [DB.Element.Name.GetValue(x) for x in all_type_framing]),
                    Separator(),
                    Button('Finish Setting')]

    form = FlexForm('ARC', components)
    form.show()
    form.values
    try:
        selected_framing_type = form.values["combobox1"]
    except:
        import sys
        sys.exit()

    def load_configs():
        beam_type = my_config.get_option("beam_type", [])
        return beam_type

    def save_configs(content_list):
        my_config.beam_type = content_list[0]
        script.save_config()

    if __name__ == "__main__":
        input_value = [selected_framing_type]
        save_configs(input_value)







