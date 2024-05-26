# -*- coding: utf-8 -*-
__doc__ = 'nguyenthanhson1712@gmail.com'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
import traceback
if module.AutodeskData():
	uidoc = __revit__.ActiveUIDocument
	doc = uidoc.Document

from Autodesk.Revit.UI.Selection import ObjectType, Selection
from pyrevit import revit, UI, script

logger = script.get_logger()
my_config = script.get_config("width_of_text_of_dim")

def load_configs():
    """Load list of frequently selected categories from configs or defaults"""
    width_input = my_config.get_option("width_input", [])
    width = [width_input]
    return width


def save_configs(content):
    """Save given list of categories as frequently selected"""
    my_config.width_input = content
    script.save_config()

if __name__ == "__main__":
    from rpw.ui.forms import TextInput
    input = TextInput('Input width of 1 symbol, nomaly 1.7~1.9', default="1.8")
    prev_width_of_text_of_dim = load_configs()
    input_value = [input]
    save_configs(input_value)






