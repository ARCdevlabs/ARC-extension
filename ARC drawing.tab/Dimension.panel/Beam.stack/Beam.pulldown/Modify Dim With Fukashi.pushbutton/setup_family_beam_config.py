# -*- coding: utf-8 -*-
import sys
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
from pyrevit import script
xamlfile = script.get_bundle_file('WPF_setup_family_beam.xaml')
import wpf
clr.AddReference("System.Windows.Forms")
clr.AddReference("System")
from System import Windows
import nances

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

from pyrevit import script

logger = script.get_logger()
my_config = script.get_config("setup_family_beam")

default = ["中心立面図","Test lưu lại","3","4","8","下側","左側","左側","上端ふかし","下端ふかし","左ふかし","右ふかし"]

def load_configs():
    setup_beam = my_config.get_option("setup_family_beam", [])
    get_setup_beam = [(x) for x in (setup_beam or default)]
    return filter(None, get_setup_beam)

def save_configs(content):
    my_config.setup_family_beam = content
    script.save_config()


xamlfile = script.get_bundle_file('WPF_setup_family_beam.xaml')
class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)
        load_setting = load_configs()
        
        self.setup_top_ref_name = load_setting[0]
        self.setup_bot_ref_name = load_setting[1]
        self.setup_left_ref_name = load_setting[2]
        self.setup_right_ref_name = load_setting[3]
        self.setup_top_fukashi_ref_name = load_setting[4]
        self.setup_bot_fukashi_ref_name = load_setting[5]
        self.setup_left_fukashi_ref_name = load_setting[6]
        self.setup_right_fukashi_ref_name = load_setting[7]

        self.setup_top_fukashi_parameter_name = load_setting[8]
        self.setup_bot_fukashi_parameter_name = load_setting[9]
        self.setup_left_fukashi_parameter_name = load_setting[10]
        self.setup_right_fukashi_parameter_name = load_setting[11]

          
    load_setting = load_configs()
    @property
    def setup_top_ref_name(self):
        return self.top_reference_name.Text
        
    @setup_top_ref_name.setter
    def setup_top_ref_name(self,value):
        self.top_reference_name.Text = value
    


    @property
    def setup_bot_ref_name(self):
        return self.bottom_reference_name.Text
    
    @setup_bot_ref_name.setter
    def setup_bot_ref_name(self,value):
        self.bottom_reference_name.Text = value



    @property
    def setup_left_ref_name(self):
        return self.left_reference_name.Text
    
    @setup_left_ref_name.setter
    def setup_left_ref_name(self,value):
        self.left_reference_name.Text = value



    @property
    def setup_right_ref_name(self):
        return self.right_reference_name.Text
    
    @setup_right_ref_name.setter
    def setup_right_ref_name(self,value):
        self.right_reference_name.Text = value


    
    @property
    def setup_top_fukashi_ref_name(self):
        return self.top_fukashi_reference_name.Text
    
    @setup_top_fukashi_ref_name.setter
    def setup_top_fukashi_ref_name(self,value):
        self.top_fukashi_reference_name.Text = value

  
    @property
    def setup_bot_fukashi_ref_name(self):
        return self.bottom_fukashi_reference_name.Text
    
    @setup_bot_fukashi_ref_name.setter
    def setup_bot_fukashi_ref_name(self,value):
        self.bottom_fukashi_reference_name.Text = value


    @property
    def setup_left_fukashi_ref_name(self):
        return self.left_fukashi_reference_name.Text

    @setup_left_fukashi_ref_name.setter
    def setup_left_fukashi_ref_name(self,value):
        self.left_fukashi_reference_name.Text = value

   

    @property
    def setup_right_fukashi_ref_name(self):
        return self.right_fukashi_reference_name.Text
    
    @setup_right_fukashi_ref_name.setter
    def setup_right_fukashi_ref_name(self,value):
        self.right_fukashi_reference_name.Text = value
    
# Setup parameter name

    @property
    def setup_top_fukashi_parameter_name(self):
        return self.top_fukashi_parameter_name.Text
    
    @setup_top_fukashi_parameter_name.setter
    def setup_top_fukashi_parameter_name(self,value):
        self.top_fukashi_parameter_name.Text = value
    

    @property
    def setup_bot_fukashi_parameter_name(self):
        return self.bottom_fukashi_parameter_name.Text
    
    @setup_bot_fukashi_parameter_name.setter
    def setup_bot_fukashi_parameter_name(self,value):
        self.bottom_fukashi_parameter_name.Text = value
    

    @property
    def setup_left_fukashi_parameter_name(self):
        return self.left_fukashi_parameter_name.Text
    
    @setup_left_fukashi_parameter_name.setter
    def setup_left_fukashi_parameter_name(self,value):
        self.left_fukashi_parameter_name.Text = value
    
    
    @property
    def setup_right_fukashi_parameter_name(self):
        return self.right_fukashi_parameter_name.Text    

    @setup_right_fukashi_parameter_name.setter
    def setup_right_fukashi_parameter_name(self,value):
        self.right_fukashi_parameter_name.Text = value

    
    def save_setting_click(self, sender, args):

        top_reference_name = self.setup_top_ref_name
        bottom_reference_name = self.setup_bot_ref_name
        left_reference_name = self.setup_left_ref_name
        right_reference_name = self.setup_right_ref_name

        top_fukashi_reference_name = self.setup_top_fukashi_ref_name
        bottom_fukashi_reference_name = self.setup_bot_fukashi_ref_name
        left_fukashi_reference_name = self.setup_left_fukashi_ref_name
        right_fukashi_reference_name = self.setup_right_fukashi_ref_name

        top_fukashi_parameter_name = self.setup_top_fukashi_parameter_name
        bottom_fukashi_parameter_name = self.setup_bot_fukashi_parameter_name
        left_fukashi_parameter_name = self.setup_left_fukashi_parameter_name
        right_fukashi_parameter_name = self.setup_right_fukashi_parameter_name

        total_setting = [top_reference_name,bottom_reference_name,left_reference_name,right_reference_name,
                        top_fukashi_reference_name,bottom_fukashi_reference_name,left_fukashi_reference_name,right_fukashi_reference_name,
                        top_fukashi_parameter_name,bottom_fukashi_parameter_name,left_fukashi_parameter_name,right_fukashi_parameter_name
                        ]

        save_configs(total_setting)

        self.Close()

MyWindow().ShowDialog()
