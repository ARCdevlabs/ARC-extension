# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import codecs
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
try:
    if module.AutodeskData():
        from nances import forms
        import clr
        clr.AddReference("System")
        from System import Array
        import System
        import sys
        import random
        from System.Drawing import Size, Color, Font, FontStyle
        from System import Drawing
        from System.Collections.Generic import List
        import Autodesk
        from Autodesk.Revit import DB
        from Autodesk.Revit.DB import View, OverrideGraphicSettings, FilteredElementCollector,FillPatternTarget, ElementParameterFilter, FilterRule, ParameterFilterRuleFactory, FilterElement, FilteredElementCollector, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, ParameterFilterElement, Transaction, BuiltInParameter, BuiltInCategory, WallType, ElementId, FilterRule, ParameterFilterElement, ElementParameterFilter, ParameterFilterRuleFactory
        import Autodesk.Revit.UI.Selection
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        view = doc.ActiveView
        def get_filter_elements():
            filter_elements = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()
            return filter_elements
        all_view_filters = get_filter_elements()
        name = []
        for i in all_view_filters:
            name.append(Autodesk.Revit.DB.Element.Name.GetValue(i))
            name.sort()

        def get_elements_by_view_filter(doc, view_filter):
            # Lấy tất cả các đối tượng trong view hiện tại
            collector = FilteredElementCollector(doc, doc.ActiveView.Id)
            all_elements = collector.ToElements()
            get_ele_filter = view_filter.GetElementFilter()
            # Tạo danh sách để lưu trữ các đối tượng thỏa mãn điều kiện của view filter
            selected_elements = []

            # Kiểm tra từng đối tượng xem nó có thỏa mãn view filter không
            for element in all_elements:
                try:
                    if get_ele_filter.PassesFilter(element):
                        selected_elements.append(element)
                except:
                    pass
            return selected_elements

        select_filter = forms.select_view_filter()
        if str(select_filter) == "None":
            module.message_box("0 filter was selected")
            sys.exit()
        else:
            checked_items = select_filter
            list_filter = []
            list_selected_element = []
            list_selected_element_thu_cap =[]
            for each_name in checked_items:  
                for filter in all_view_filters:
                    if filter.Name == each_name:
                        list_filter.append(filter)
            # filter = doc.GetElement(filter_id)
            for filter in list_filter:
            # Sử dụng hàm get_elements_by_view_filter để lấy tất cả các đối tượng thỏa mãn view filter và lưu vào danh sách selected_elements
                selected_elements = get_elements_by_view_filter(doc, filter)
                list_selected_element.append(selected_elements)
                # Bây giờ selected_elements chứa tất cả các đối tượng mà view filter đang áp dụng
            for tung_doi_tuong in list_selected_element:
                for tung_doi_tuong_2 in tung_doi_tuong:
                    list_selected_element_thu_cap.append(tung_doi_tuong_2)
            if len(list_selected_element_thu_cap) == 0:
                module.message_box("There are no objects matching the selected filter")
            else:
                chon_doi_tuong = module.get_current_selection(uidoc,list_selected_element_thu_cap)
except:
    # import traceback
    # print(traceback.format_exc())
    pass

