# -*- coding: utf-8 -*-
from System.Collections.Generic import *
import traceback
from pyrevit import script

logger = script.get_logger()
my_config = script.get_config("width_of_text_of_dim")

def load_configs():
    width_input = my_config.get_option("width_input", [])
    gia_tri_mac_dinh = ["1.8"]
    width = width_input or gia_tri_mac_dinh #Cần phải có dòng này, nếu không thì nếu lần đầu chạy tool sẽ bị lỗi ngay
    return width

def save_configs(content):
    my_config.width_input = content
    script.save_config()

if __name__ == "__main__":
    from rpw.ui.forms import TextInput
    prev_width_of_text_of_dim = load_configs()
    cover_to_string = prev_width_of_text_of_dim[0]
    input = TextInput('Input width of 1 symbol, normaly 1.7~1.9', cover_to_string)
    input_value = [input]
    save_configs(input_value)