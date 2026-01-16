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
my_config = script.get_config("configs_setup_family_beam")

from System import Uri, UriKind
from System.Windows.Media.Imaging import BitmapImage

image_path_guide_1 = script.get_bundle_file("guide_1.png")
bitmap_guide_1 = BitmapImage()
bitmap_guide_1.BeginInit()
bitmap_guide_1.UriSource = Uri(image_path_guide_1, UriKind.Absolute)
bitmap_guide_1.EndInit()


image_path_guide_2 = script.get_bundle_file("guide_2.png")
bitmap_guide_2 = BitmapImage()
bitmap_guide_2.BeginInit()
bitmap_guide_2.UriSource = Uri(image_path_guide_2, UriKind.Absolute)
bitmap_guide_2.EndInit()


default_settup_family = ["中心立面図","6","3","4","8","下側","左側","右側","上端ふかし","下端ふかし","左ふかし","右ふかし"]
default_settup_dim_in_need = [bool(True),bool(True),bool(True)]

def load_configs_setup_family():
    setup_beam = my_config.get_option("setup_family_beam", [])
    get_setup_beam = [(x) for x in (setup_beam or default_settup_family)]
    return filter(None, get_setup_beam)

def load_configs_setup_dim_in_need():
    setup_dim = my_config.get_option("setup_dim_in_need", [])
    get_setup_dim = [(x) for x in (setup_dim or default_settup_dim_in_need)]
    return get_setup_dim

def save_configs_setup_family(content):
    my_config.setup_family_beam = content
    script.save_config()

def save_configs_setup_dim_in_need(content):
    my_config.setup_dim_in_need = content
    script.save_config()



xamlfile = script.get_bundle_file('WPF_setup_family_beam_for_dim.xaml')
class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

        self.guide_image_1.Source = bitmap_guide_1
        self.guide_image_2.Source = bitmap_guide_2

        self.MK_梁_RC = ["中心立面図","6","3","4","8","下側","左側","右側","上端ふかし","下端ふかし","左ふかし","右ふかし"]
        self.MK_S_構フ_RC_梁 = ["中心立面図","中央_梁せい","中央_梁幅_1","中央_梁幅_2","上部_ふかし厚さ","下部_中央_ふかし_厚さ","左部_ふかし_厚さ_中央","右部_ふかし_厚さ_中央","Srb011_上部_ふかし厚さ","Srb012_下部_ふかし厚さ","Srb013_側1_ふかし厚さ","Srb014_側2_ふかし厚さ"]
        self.list_other = [""] * 12 #Tạo ra list có 12 đối tượng trống.

        values =[
                    "Last setting",
                    "MK_梁〈RC〉",
                    "MK_S_構フ_RC_梁",
                    "Other"
                ]
        self.combo_box_select_family.ItemsSource = values
        self.combo_box_select_family.SelectedIndex = 0

        load_setting_dim = load_configs_setup_dim_in_need()
        self.apply_load_setting_dim_in_need(load_setting_dim)

    def combo_box_select_family_changed(self, sender, args): 
        #Điều này có nghĩa là bất cứ khi nào combox bị đổi giá trị thì 
        #dòng cuối [self.apply_load_setting(load_setting)] sẽ load lại 1 lần, và từ đó gán lại giá trị cho các text box.
        selected = self.combo_box_select_family.SelectedItem

        if selected == "MK_S_構フ_RC_梁":
            load_setting = self.MK_S_構フ_RC_梁

        elif selected == "MK_梁〈RC〉":
            load_setting = self.MK_梁_RC

        elif selected == "Last setting":
            load_setting = load_configs_setup_family()

        elif selected == "Other":
            load_setting = self.list_other
       
        self.apply_load_setting(load_setting)

        

    def apply_load_setting(self, load_setting):
        self.setup_top_ref_name = load_setting[0] #Dòng này sẽ gán vào giá trị value ở hàm  @setup_top_ref_name.setter
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

    def apply_load_setting_dim_in_need(self, load_setting_dim):
        self.setup_dim_3 = load_setting_dim[0]
        self.setup_dim_2 = load_setting_dim[1]
        self.setup_dim_1 = load_setting_dim[2]


    @property
    def setup_top_ref_name(self): #"setup_top_ref_name" là tên của biến trong python
        return self.top_reference_name.Text #"top_reference_name" là tên của biến trong file xaml
        
    @setup_top_ref_name.setter #Mục đích hàm setter này là để lấy giá trị từ file .ini để gán vào form, nếu không có hàm này thì dù có lưu setting thì form lúc nào cũng gọi giá trị mặc định hoặc giá trị ban đầu.
    def setup_top_ref_name(self,value):
        self.top_reference_name.Text = value #value này sẽ lấy giá trị từ dòng :self.setup_top_ref_name = load_setting[0]:
    

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


    # Setup dim in need
    @property
    def setup_dim_3(self):
        return self.check_box_combo_3.IsChecked
    
    @setup_dim_3.setter
    def setup_dim_3(self,value):
        self.check_box_combo_3.IsChecked =  bool(value)

    @property
    def setup_dim_2(self):
        return self.check_box_combo_2.IsChecked
    @setup_dim_2.setter
    def setup_dim_2(self,value):
        self.check_box_combo_2.IsChecked =  bool(value)
    
    @property
    def setup_dim_1(self):
        return self.check_box_combo_1.IsChecked
    @setup_dim_1.setter
    def setup_dim_1(self,value):
        self.check_box_combo_1.IsChecked =  bool(value)
    
    def save_setting_click(self, sender, args): #save_setting_click là tên của biến button và hành động click trong file xaml
        top_reference_name = self.setup_top_ref_name #"top_reference_name" là tên biến của textbox trong xaml, "setup_top_ref_name" là tên của biến trong python
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
        #Trả về giá trị là tên của textbox trong xaml
        is_check_dim_3 = self.setup_dim_3
        is_check_dim_2 = self.setup_dim_2
        is_check_dim_1 = self.setup_dim_1
        total_setting_dim_in_need = [is_check_dim_3,is_check_dim_2,is_check_dim_1]
        save_configs_setup_family(total_setting)
        save_configs_setup_dim_in_need(total_setting_dim_in_need)
        self.Close()

if __name__ == "__main__": #Cần phải có hàm này bởi vì nếu không có thì khi lần đầu mở revit và mở tool lên, form xaml sẽ hiện lên dù không nhấn shift
    MyWindow().ShowDialog()
