# -*- coding: utf-8 -*-
from pyrevit import forms, script
import clr
import System
import os
import codecs # Thư viện xử lý file text và encoding

# Import Revit API
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

# Class đại diện cho 1 dòng kết quả
class ParamItem:
    def __init__(self, name, group):
        self.Name = name
        self.Group = group

class SearchWindow(forms.WPFWindow):
    def __init__(self, xaml_file):
        forms.WPFWindow.__init__(self, xaml_file)
        
        self.all_params = [] # List chứa data gốc
        
        # Chạy hàm đọc file "thông minh"
        self.load_shared_params_smart()
        
        # Focus vào ô nhập liệu ngay lập tức
        self.search_tb.Focus()

    def load_shared_params_smart(self):
        """Đọc file SP bỏ qua Revit API và tự dò bảng mã"""
        
        # 1. Lấy đường dẫn file từ setting của Revit
        sp_filename = app.SharedParametersFilename
        
        # Kiểm tra file có tồn tại không
        if not sp_filename or not os.path.exists(sp_filename):
            self.status_lb.Text = "Lỗi: Không tìm thấy đường dẫn file Shared Parameter trong Revit!"
            return

        # 2. Danh sách các bảng mã cần thử (Revit thường dùng utf-16 hoặc utf-8)
        encodings_to_try = ['utf-16', 'utf-8-sig', 'utf-8', 'mbcs']
        
        lines = []
        success_encoding = None

        # Vòng lặp thử mở file với từng bảng mã
        for enc in encodings_to_try:
            try:
                with codecs.open(sp_filename, 'r', encoding=enc) as f:
                    temp_lines = f.readlines()
                
                # Kiểm tra nhanh: Nếu 20 dòng đầu có chữ "GROUP" hoặc "PARAM" là đọc đúng
                content_check = "".join(temp_lines[:20])
                if "GROUP" in content_check or "PARAM" in content_check:
                    lines = temp_lines
                    success_encoding = enc
                    break # Đã tìm thấy chìa khóa đúng, thoát vòng lặp
            except:
                continue # Thử chìa khóa tiếp theo

        if not lines:
            self.status_lb.Text = "Lỗi nghiêm trọng: Không thể đọc nội dung file (Sai Encoding hoặc File hỏng)."
            return

        # 3. Phân tích nội dung text
        try:
            group_map = {} 
            temp_params = []

            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'): continue 

                parts = line.split('\t') # File SP ngăn cách bằng dấu Tab

                # Xử lý dòng GROUP (Lưu ID và Tên Group vào từ điển)
                # Cấu trúc: *GROUP   ID   NAME
                if "GROUP" in parts[0] and len(parts) >= 3:
                    clean_id = parts[1].strip()
                    clean_name = parts[2].strip()
                    group_map[clean_id] = clean_name

                # Xử lý dòng PARAM (Lấy Tên và tra cứu Group ID)
                # Cấu trúc: *PARAM   GUID   NAME   ...   GROUP_ID ...
                elif "PARAM" in parts[0] and len(parts) >= 6:
                    p_name = parts[2].strip()
                    group_id = parts[5].strip()
                    
                    # Tra cứu tên group từ ID, nếu không thấy thì để Unknown
                    g_name = group_map.get(group_id, "Unknown Group")
                    
                    temp_params.append(ParamItem(p_name, g_name))
            
            self.all_params = temp_params
            
            # Cập nhật giao diện
            self.status_lb.Text = "Sẵn sàng. Đã load {} parameters (Mã: {}).".format(len(self.all_params), success_encoding)
            self.update_list(self.all_params)

        except Exception as e:
            self.status_lb.Text = "Lỗi xử lý dữ liệu: " + str(e)

    def search_box_changed(self, sender, args):
        """Sự kiện khi gõ text tìm kiếm"""
        keyword = self.search_tb.Text.lower()
        
        if not self.all_params: return

        if not keyword:
            self.update_list(self.all_params) 
            return

        # Lọc dữ liệu (Contains - Không phân biệt hoa thường)
        filtered_list = [p for p in self.all_params if keyword in p.Name.lower()]
        
        self.update_list(filtered_list)
        self.status_lb.Text = "Tìm thấy {} kết quả.".format(len(filtered_list))

    def update_list(self, data):
        """Đưa dữ liệu lên bảng"""
        self.result_dg.ItemsSource = data

# --- MAIN BLOCK ---
if __name__ == '__main__':
    xaml_path = script.get_bundle_file('ui.xaml')
    if os.path.exists(xaml_path):
        window = SearchWindow(xaml_path)
        window.ShowDialog()
    else:
        forms.alert("Không tìm thấy file giao diện ui.xaml!", exitscript=True)