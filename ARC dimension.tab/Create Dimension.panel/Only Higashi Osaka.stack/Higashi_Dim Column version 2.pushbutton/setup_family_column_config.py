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
my_config = script.get_config("configs_setup_family_column")

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
        "tooldimcolumnwithfukashi",
        "03022026picture",
        str(ten_image)
        )

    return image_link


image_path_guide_0 = get_link_image ("guide_0.png")
bitmap_guide_0 = BitmapImage()
bitmap_guide_0.BeginInit()
bitmap_guide_0.UriSource = Uri(image_path_guide_0, UriKind.Absolute)
bitmap_guide_0.EndInit()


image_path_guide_1 = get_link_image ("guide_1.png")
bitmap_guide_1 = BitmapImage()
bitmap_guide_1.BeginInit()
bitmap_guide_1.UriSource = Uri(image_path_guide_1, UriKind.Absolute)
bitmap_guide_1.EndInit()

default_settup_family = ["背面","正面","左","右","D","B","C","A","フカシD","フカシB","フカシC","フカシA"]

default_settup_dim_in_need_in_plan_view = [bool(True),bool(True),bool(True)]

default_settup_setup_position_of_dim = [bool(False),bool(False),bool(False),bool(True)]

default_setup_dim = str(9)

def load_configs_setup_family():
    setup_beam = my_config.get_option("setup_family_column", [])
    get_setup_column = [(x) for x in (setup_beam or default_settup_family)]
    return filter(None, get_setup_column)

def save_configs_setup_family(content):
    my_config.setup_family_column = content
    script.save_config()

def load_configs_setup_offset_dim():
    setup_offset = my_config.get_option("setup_offset_dim", [])
    get_setup_offset_dim = setup_offset or default_setup_dim
    return filter(None, get_setup_offset_dim)

def save_configs_setup_offset_dim(content):
    my_config.setup_offset_dim = content
    script.save_config()

def load_configs_setup_dim_in_need_in_plan_view():
    setup_dim_in_plan = my_config.get_option("setup_dim_in_need_in_plan_view", [])
    get_setup_dim_in_plan = [(x) for x in (setup_dim_in_plan or default_settup_dim_in_need_in_plan_view)]
    return get_setup_dim_in_plan

def save_configs_setup_dim_in_need_in_plan_view(content):
    my_config.setup_dim_in_need_in_plan_view = content
    script.save_config()

def load_configs_setup_position_of_dim():
    setup_position = my_config.get_option("setup_position_of_dim", [])
    get_setup_position_of_dim = [(x) for x in (setup_position or default_settup_setup_position_of_dim)]
    return get_setup_position_of_dim

def save_configs_get_setup_position_of_dim(content):
    my_config.setup_position_of_dim = content
    script.save_config()

import re

xamlfile = script.get_bundle_file('WPF_setup_family_column_for_dim.xaml')

class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

        self.guide_image_1.Source = bitmap_guide_1
        # self.guide_image_2.Source = bitmap_guide_2
        self.guide_image_0.Source = bitmap_guide_0

        self._updating = False

        self.MK_柱_RC = ["背面","正面","左","右","D","B","C","A","フカシD","フカシB","フカシC","フカシA"]
        self.KJ_RC柱 = ["背面","正面","左","右","D","B","C","A","フカシ上","フカシ下","フカシ左","フカシ右"]
        self.MK_S_構柱_RC_柱 = ["背面","正面","左","右","前ふかし_厚さ","後ふかし_厚さ","左ふかし_厚さ","右ふかし_厚さ","Srp005_前部_ふかし厚さF","Srp006_後部_ふかし厚さF","Srp007_左部_ふかし厚さF","Srp008_右部_ふかし厚さF"]
        self.T_柱RC角柱 = ["構造体-Y方向R","構造体-Y方向L","構造体-X方向L","構造体-X方向R","外形-Y方向R","外形-Y方向L","外形-X方向L","外形-X方向R","Y方向Rﾌｶｼ","Y方向Lﾌｶｼ","X方向Lﾌｶｼ","X方向Rﾌｶｼ"]
        self.custom_family_obayashi = ["背面","正面","左","右","背面+Y+","正面+Y-","左+X-","右+X+","増打ち_Y正面_project","増打ち_Y負面_project","増打ち_X負面_project","増打ち_X正面_project"]
        self.list_other = [""] * 12 #Tạo ra list có 12 đối tượng trống.

        values =[
                    "Last setting",
                    "MK_柱〈RC〉",
                    "T_柱RC-角柱",                   
                    "MK_S_構柱_RC_柱 or MK_S_構柱_RC_根巻柱",
                    "Custom_KJ_RC柱",
                    "Custom family_Obayashi",
                    "Other"
                ]
        self.combo_box_select_family.ItemsSource = values
        self.combo_box_select_family.SelectedIndex = 0

        load_setting_dim_in_plan_view = load_configs_setup_dim_in_need_in_plan_view()

        load_setting_position_of_dim= load_configs_setup_position_of_dim()

        load_configs_offset_dim = load_configs_setup_offset_dim()

        self.apply_load_setting_dim_in_need_in_plan_view(load_setting_dim_in_plan_view)

        self.apply_load_setting_position_of_dim(load_setting_position_of_dim)   

        self.update_total_input()

        self.setup_offset_dim = load_configs_offset_dim[0]

    def number_only(self, sender, args):
        # Cho số + dấu chấm
        if not re.match(r'^[0-9.]$', args.Text):
            args.Handled = True

    def top_reference_name_changed(self, sender, args):
        self.update_total_input()

    def bottom_reference_name_changed(self, sender, args):
        self.update_total_input()

    def left_reference_name_changed(self, sender, args):
        self.update_total_input()

    def right_reference_name_changed(self, sender, args):
        self.update_total_input()

    def top_fukashi_reference_name_changed(self, sender, args):
        self.update_total_input()

    def bottom_fukashi_reference_name_changed(self, sender, args):
        self.update_total_input()

    def left_fukashi_reference_name_changed(self, sender, args):
        self.update_total_input()

    def right_fukashi_reference_name_changed(self, sender, args):
        self.update_total_input()

    def top_fukashi_parameter_name_changed(self, sender, args):
        self.update_total_input()

    def bottom_fukashi_parameter_name_changed(self, sender, args):
        self.update_total_input()

    def left_fukashi_parameter_name_changed(self, sender, args):
        self.update_total_input()

    def right_fukashi_parameter_name_changed(self, sender, args):
        self.update_total_input()

    def update_total_input(self): 
        self.all_textboxes = [
            self.top_reference_name,
            self.bottom_reference_name,
            self.left_reference_name,
            self.right_reference_name,
            self.top_fukashi_reference_name,
            self.bottom_fukashi_reference_name,
            self.left_fukashi_reference_name,
            self.right_fukashi_reference_name,
            self.top_fukashi_parameter_name,
            self.bottom_fukashi_parameter_name,
            self.left_fukashi_parameter_name,
            self.right_fukashi_parameter_name,
        ]
        #tránh vòng lặp vô hạn
        if self._updating:
            return

        self._updating = True
        values = [tb.Text or "" for tb in self.all_textboxes]
        self.total_input.Text = u'["{}"]'.format(u'","'.join(values))
        self._updating = False

    def parse_total_input(self, text):
        """
        Nhận: Định dạng giống với list python
        ["A","B","C"]
        Trả: Định dạng list python chuẩn
        ["A","B","C"]
        """
        if not text:
            return []

        # Lấy tất cả chuỗi nằm trong dấu "
        values = re.findall(r'"(.*?)"', text)
        return values
    
    def on_total_input_changed(self, sender, args):
        if self._updating:
            return

        self._updating = True
        values = self.parse_total_input(self.total_input.Text)

        if len(values) == len(self.all_textboxes):
            for tb, value in zip(self.all_textboxes, values):
                tb.Text = value

        self._updating = False


    def combo_box_select_family_changed(self, sender, args): 
        #Điều này có nghĩa là bất cứ khi nào combox bị đổi giá trị thì 
        #dòng cuối [self.apply_load_setting(load_setting)] sẽ load lại 1 lần, và từ đó gán lại giá trị cho các text box.
        selected = self.combo_box_select_family.SelectedItem

        # if selected == "MK_S_構フ_RC_梁":
        #     load_setting = self.MK_S_構フ_RC_梁

        if selected == "MK_柱〈RC〉":
            load_setting = self.MK_柱_RC
        
        if selected == "Custom_KJ_RC柱":
            load_setting = self.KJ_RC柱
        
        elif selected == "T_柱RC-角柱":
            load_setting = self.T_柱RC角柱

        elif selected == "MK_S_構柱_RC_柱 or MK_S_構柱_RC_根巻柱":
            load_setting = self.MK_S_構柱_RC_柱

        elif selected == "Last setting":
            load_setting = load_configs_setup_family()
    
        elif selected == "Custom family_Obayashi":
            load_setting = self.custom_family_obayashi

        elif selected == "Other":
            load_setting = self.list_other
       
        self.apply_load_setting(load_setting)

        # self.update_total_input()


    def radio_button_top_left_changed(self, sender, args):
        if self.radio_button_top_left.IsChecked:
            self.set_guide_image("top_left.png")

    def radio_button_top_right_changed(self, sender, args):
        if self.radio_button_top_right.IsChecked:
            self.set_guide_image("top_right.png")

    def radio_button_bot_left_changed(self, sender, args):
        if self.radio_button_bot_left.IsChecked:
            self.set_guide_image("bot_left.png")

    def radio_button_bot_right_changed(self, sender, args):
        if self.radio_button_bot_right.IsChecked:
            self.set_guide_image("bot_right.png")

    def set_guide_image(self, image_name):
        # image_path = script.get_bundle_file(image_name)
        image_path = get_link_image (image_name)
        bitmap = BitmapImage()
        bitmap.BeginInit()
        bitmap.UriSource = Uri(image_path, UriKind.Absolute)
        bitmap.EndInit()

        self.guide_image_3.Source = bitmap

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

    def apply_load_setting_dim_in_need_in_plan_view(self, load_setting_dim_in_plan_view):
        self.setup_dim_3 = load_setting_dim_in_plan_view[0]
        self.setup_dim_2 = load_setting_dim_in_plan_view[1]
        self.setup_dim_1 = load_setting_dim_in_plan_view[2]

    # def apply_load_setting_dim_in_need_in_section_view(self, load_setting_dim_in_section_dim):
    #     self.setup_dim_A = load_setting_dim_in_section_dim[0]
    #     self.setup_dim_B = load_setting_dim_in_section_dim[1]
    #     self.setup_dim_C = load_setting_dim_in_section_dim[2]
    #     self.setup_dim_D = load_setting_dim_in_section_dim[3]
    #     self.setup_dim_E = load_setting_dim_in_section_dim[4]

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


    # Setup dim in need_in_plan_view
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

    # # Setup dim in need_in_section_view
    # @property
    # def setup_dim_A(self):
    #     return self.check_box_combo_A_section.IsChecked
    
    # @setup_dim_A.setter
    # def setup_dim_A(self,value):
    #     self.check_box_combo_A_section.IsChecked =  bool(value)

    # @property
    # def setup_dim_B(self):
    #     return self.check_box_combo_B_section.IsChecked
    
    # @setup_dim_B.setter
    # def setup_dim_B(self,value):
    #     self.check_box_combo_B_section.IsChecked =  bool(value)

    # @property
    # def setup_dim_C(self):
    #     return self.check_box_combo_C_section.IsChecked
    
    # @setup_dim_C.setter
    # def setup_dim_C(self,value):
    #     self.check_box_combo_C_section.IsChecked =  bool(value)

    # @property
    # def setup_dim_D(self):
    #     return self.check_box_combo_D_section.IsChecked
    
    # @setup_dim_D.setter
    # def setup_dim_D(self,value):
    #     self.check_box_combo_D_section.IsChecked =  bool(value)

    # @property
    # def setup_dim_E(self):
    #     return self.check_box_combo_E_section.IsChecked
    
    # @setup_dim_E.setter
    # def setup_dim_E(self,value):
    #     self.check_box_combo_E_section.IsChecked =  bool(value)

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

        total_setting_dim_in_need_in_plan_view = [is_check_dim_3,is_check_dim_2,is_check_dim_1]


        offset_of_dim = self.setup_offset_dim
        # is_check_dim_B = self.setup_dim_B
        # is_check_dim_C = self.setup_dim_C
        # is_check_dim_D = self.setup_dim_D
        # is_check_dim_E = self.setup_dim_E
        total_offset_dim = [offset_of_dim]
        # total_setting_dim_in_need_in_section_view = [is_check_dim_A,is_check_dim_B,is_check_dim_C,is_check_dim_D,is_check_dim_E]

        is_check_top_left = self.setup_top_left
        is_check_top_right = self.setup_top_right
        is_check_bot_left = self.setup_bot_left
        is_check_bot_right = self.setup_bot_right

        total_setting_position_of_dim = [is_check_top_left,is_check_top_right,is_check_bot_left,is_check_bot_right]

        save_configs_setup_family(total_setting)

        save_configs_setup_dim_in_need_in_plan_view(total_setting_dim_in_need_in_plan_view)

        save_configs_setup_offset_dim(total_offset_dim)

        save_configs_get_setup_position_of_dim(total_setting_position_of_dim)
        
        self.Close()

if __name__ == "__main__": #Cần phải có hàm này bởi vì nếu không có thì khi lần đầu mở revit và mở tool lên, form xaml sẽ hiện lên dù không nhấn shift
    MyWindow().ShowDialog()
