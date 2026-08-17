# -*- coding: utf-8 -*-
import sys
import clr
from pyrevit import script
import wpf
clr.AddReference("System.Windows.Forms")
clr.AddReference("System")
from System import Windows
import nances
from System import Uri, UriKind

from System.Windows.Media.Imaging import BitmapImage

def get_link_image (ten_image):
    import os

    base_appdata = os.environ["APPDATA"]

    image_link = os.path.join(
        base_appdata,
        "pyRevit",
        "Extensions",
        "ARC extension.extension",
        "lib",
        "nances",
        "allpictureloadtoxaml",
        "tooldimwallRC",
        "05082026picture",
        str(ten_image)
        )

    return image_link

image_path_guide_1 = get_link_image("guide_5.png")
bitmap_guide_1 = BitmapImage()
bitmap_guide_1.BeginInit()
bitmap_guide_1.UriSource = Uri(image_path_guide_1, UriKind.Absolute)
bitmap_guide_1.EndInit()


uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

from pyrevit import script

logger = script.get_logger()
my_config = script.get_config("configs_setup_dim_wall_RC_in_need")

default_settup_setup_dim_in_need = [bool(True),bool(True),bool(True),bool(False),bool(False)]

default_setup_dim = str(5)

def load_configs_setup_dim_wall_RC_in_need():
    dim_in_need = my_config.get_option("setup_dim_in_need_new", [])
    get_dim_in_need = [(x) for x in (dim_in_need or default_settup_setup_dim_in_need)]
    return get_dim_in_need

def save_configs_setup_dim_wall_RC_in_need(content):
    my_config.setup_dim_in_need_new = content
    script.save_config()

def load_configs_setup_offset_dim():
    setup_offset = my_config.get_option("setup_offset_dim", [])
    get_setup_offset_dim = setup_offset or default_setup_dim
    return filter(None, get_setup_offset_dim)

def save_configs_setup_offset_dim(content):
    my_config.setup_offset_dim = content
    script.save_config()


import re

xamlfile = script.get_bundle_file('WPF_setup_dim_wall_RC.xaml')

class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

        self.guide_image_1.Source = bitmap_guide_1

        self._updating = False

        load_configs_offset_dim_wall_RC = load_configs_setup_offset_dim()

        load_setting_dim_in_need= load_configs_setup_dim_wall_RC_in_need()

        self.setup_offset_dim = load_configs_offset_dim_wall_RC[0]

        self.apply_load_setting_dim_in_need(load_setting_dim_in_need)   

    def number_only(self, sender, args):
        # Cho số + dấu chấm
        if not re.match(r'^[0-9.]$', args.Text):
            args.Handled = True

    def apply_load_setting_dim_in_need(self, load_setting_dim_in_need):
        self.setup_dim_1 = load_setting_dim_in_need[0]
        self.setup_dim_2 = load_setting_dim_in_need[1]
        self.setup_dim_3 = load_setting_dim_in_need[2]
        self.setup_dim_3a = load_setting_dim_in_need[3]
        self.setup_reverse_dim = load_setting_dim_in_need[4]

    @property
    def setup_offset_dim(self):
        return self.textbox_offset_dim.Text
    
    @setup_offset_dim.setter
    def setup_offset_dim(self,value):
        self.textbox_offset_dim.Text = value

    # Radio button
    @property
    def setup_dim_1(self):
        return self.check_box_combo_1.IsChecked
    
    @setup_dim_1.setter
    def setup_dim_1(self,value):
        self.check_box_combo_1.IsChecked =  bool(value)

    @property
    def setup_dim_2(self):
        return self.check_box_combo_2.IsChecked
    
    @setup_dim_2.setter
    def setup_dim_2(self,value):
        self.check_box_combo_2.IsChecked =  bool(value)

    @property
    def setup_dim_3(self):
        return self.check_box_combo_3.IsChecked
    
    @setup_dim_3.setter
    def setup_dim_3(self,value):
        self.check_box_combo_3.IsChecked =  bool(value)

    @property
    def setup_dim_3a(self):
        return self.check_box_combo_3a.IsChecked
    
    @setup_dim_3a.setter
    def setup_dim_3a(self,value):
        self.check_box_combo_3a.IsChecked =  bool(value)
        
    def check_box_combo_3_changed(self, sender, args):
        if self.check_box_combo_3.IsChecked:
            self.check_box_combo_3a.IsChecked = False


    def check_box_combo_3a_changed(self, sender, args):
        if self.check_box_combo_3a.IsChecked:
            self.check_box_combo_3.IsChecked = False

    @property
    def setup_reverse_dim(self):
        return self.check_box_reverse_dim_position.IsChecked
    
    @setup_reverse_dim.setter
    def setup_reverse_dim(self,value):
        self.check_box_reverse_dim_position.IsChecked =  bool(value)

    def save_setting_click(self, sender, args): #save_setting_click là tên của biến button và hành động click trong file xaml

        is_check_dim_1 = self.setup_dim_1
        is_check_dim_2 = self.setup_dim_2
        is_check_dim_3 = self.setup_dim_3
        is_check_dim_3a = self.setup_dim_3a
        is_check_reverse_dim = self.setup_reverse_dim

        total_setting_dim_in_need = [is_check_dim_1,is_check_dim_2,is_check_dim_3,is_check_dim_3a,is_check_reverse_dim]

        offset_of_dim = self.setup_offset_dim
        total_offset_dim = [offset_of_dim]
        save_configs_setup_offset_dim(total_offset_dim)

        save_configs_setup_dim_wall_RC_in_need(total_setting_dim_in_need)
        
        self.Close()

if __name__ == "__main__": #Cần phải có hàm này bởi vì nếu không có thì khi lần đầu mở revit và mở tool lên, form xaml sẽ hiện lên dù không nhấn shift
    MyWindow().ShowDialog()
