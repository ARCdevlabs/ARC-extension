# -*- coding: utf-8 -*-
import sys
import clr
from pyrevit import script
import wpf
clr.AddReference("System.Windows.Forms")
clr.AddReference("System")
from System import Windows
import nances

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

from pyrevit import script

logger = script.get_logger()
my_config = script.get_config("configs_setup_position_dim_foundation_column")

default_settup_setup_position_of_dim = [bool(False),bool(False),bool(False),bool(True)]

default_setup_dim = str(4)

def load_configs_setup_position_of_dim():
    setup_position = my_config.get_option("setup_position_of_dim", [])
    get_setup_position_of_dim = [(x) for x in (setup_position or default_settup_setup_position_of_dim)]
    return get_setup_position_of_dim

def save_configs_get_setup_position_of_dim(content):
    my_config.setup_position_of_dim = content
    script.save_config()

def load_configs_setup_offset_dim():
    setup_offset = my_config.get_option("setup_offset_dim", [])
    get_setup_offset_dim = setup_offset or default_setup_dim
    return filter(None, get_setup_offset_dim)

def save_configs_setup_offset_dim(content):
    my_config.setup_offset_dim = content
    script.save_config()


import re

xamlfile = script.get_bundle_file('WPF_setup_position_of_dim_foundation_column.xaml')

class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

        self._updating = False

        load_configs_offset_dim = load_configs_setup_offset_dim()

        load_setting_position_of_dim= load_configs_setup_position_of_dim()

        self.setup_offset_dim = load_configs_offset_dim[0]

        self.apply_load_setting_position_of_dim(load_setting_position_of_dim)   

    def number_only(self, sender, args):
        # Cho số + dấu chấm
        if not re.match(r'^[0-9.]$', args.Text):
            args.Handled = True

    def apply_load_setting_position_of_dim(self, load_setting_position_of_dim):
        self.setup_top_left = load_setting_position_of_dim[0]
        self.setup_top_right = load_setting_position_of_dim[1]
        self.setup_bot_left = load_setting_position_of_dim[2]
        self.setup_bot_right = load_setting_position_of_dim[3]

    @property
    def setup_offset_dim(self):
        return self.textbox_offset_dim.Text
    
    @setup_offset_dim.setter
    def setup_offset_dim(self,value):
        self.textbox_offset_dim.Text = value

    # Radio button
    @property
    def setup_top_left(self):
        return self.radio_button_top_left.IsChecked
    
    @setup_top_left.setter
    def setup_top_left(self,value):
        self.radio_button_top_left.IsChecked =  bool(value)

    @property
    def setup_top_right(self):
        return self.radio_button_top_right.IsChecked
    
    @setup_top_right.setter
    def setup_top_right(self,value):
        self.radio_button_top_right.IsChecked =  bool(value)

    @property
    def setup_bot_left(self):
        return self.radio_button_bot_left.IsChecked
    
    @setup_bot_left.setter
    def setup_bot_left(self,value):
        self.radio_button_bot_left.IsChecked =  bool(value)

    @property
    def setup_bot_right(self):
        return self.radio_button_bot_right.IsChecked
    
    @setup_bot_right.setter
    def setup_bot_right(self,value):
        self.radio_button_bot_right.IsChecked =  bool(value)


    def save_setting_click(self, sender, args): #save_setting_click là tên của biến button và hành động click trong file xaml

        is_check_top_left = self.setup_top_left
        is_check_top_right = self.setup_top_right
        is_check_bot_left = self.setup_bot_left
        is_check_bot_right = self.setup_bot_right

        total_setting_position_of_dim = [is_check_top_left,is_check_top_right,is_check_bot_left,is_check_bot_right]

        offset_of_dim = self.setup_offset_dim
        total_offset_dim = [offset_of_dim]
        save_configs_setup_offset_dim(total_offset_dim)

        save_configs_get_setup_position_of_dim(total_setting_position_of_dim)
        
        self.Close()

if __name__ == "__main__": #Cần phải có hàm này bởi vì nếu không có thì khi lần đầu mở revit và mở tool lên, form xaml sẽ hiện lên dù không nhấn shift
    MyWindow().ShowDialog()
