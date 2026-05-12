# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.Exceptions import OperationCanceledException

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

import nances
import sys
from nances import selection
"""Activates selection tool that picks only Model elements."""

from pyrevit.framework import List
from pyrevit import revit, DB, UI

from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox,
                            Separator, Button, CheckBox)
components = [
            Label('Nhập số bắt đầu'),
            TextBox('textbox1', Text="1"),      
            Label('Nhập parameter'),
            TextBox('textbox2', Text="Comments"),
            Separator(),
            Button('Ok')
        ]
form = FlexForm('ARC', components)
form.show()
form.values    
try:
    start_number = form.values["textbox1"]
    parameter = form.values["textbox2"]
    # save_configs(parameter)
    # get_parameter = load_configs()
except:
    sys.exit()

counter = int(start_number)

while True:
    try:

        ele = selection.pick_model_by_rectangle(uidoc)

        t = Transaction(doc, "Set Comments {}".format(counter))

        t.Start()

        for el in ele:
            p = el.LookupParameter(parameter)
            if p and not p.IsReadOnly:
                p.Set(str(counter))

        t.Commit()

        counter += 1

    except OperationCanceledException:
        # Nhấn ESC
        print("Đã dừng tool.")
        break

    except Exception as e:
        print("Lỗi:", e)
        break
    



