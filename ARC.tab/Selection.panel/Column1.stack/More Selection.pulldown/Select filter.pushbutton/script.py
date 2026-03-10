# -*- coding: utf-8 -*-
import nances
try:
    if nances.AutodeskData():
        from nances import forms
        import sys
        from Autodesk.Revit import DB        
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        view = doc.ActiveView
        def get_filter_elements():
            filter_elements = DB.FilteredElementCollector(doc).OfClass(DB.ParameterFilterElement).ToElements()
            return filter_elements
        all_view_filters = get_filter_elements()
        name = []
        for i in all_view_filters:
            name.append(DB.Element.Name.GetValue(i))
            name.sort()

        select_filter = forms.select_view_filter()
        if str(select_filter) == "None":
            nances.message_box("0 filter was selected")
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
        nances.get_current_selection(uidoc,list_filter)
except:
    pass

