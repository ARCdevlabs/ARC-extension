# -*- coding: utf-8 -*-
import string
import codecs
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
from pyrevit import revit, DB
from nances import forms
from pyrevit import script
if module.AutodeskData():
    logger = script.get_logger()
    selected_views = forms.select_views(use_selection=True)
    # module.message_box("Tiếp theo, chỉ được 1 sheet mà muốn add view vào thôi")
    if selected_views:
        logger.debug('View đã chọn {}'.format(len(selected_views)))
        # get the destination sheets from user
        dest_sheets = forms.select_sheets(multiple=False, include_placeholder=False)
        # print type(dest_sheets)

        if dest_sheets:
            # logger.debug('Sheet đã chọn: {}'.format(len(dest_sheets)))
            with revit.Transaction("Đặt view đang chọn vào sheet có sẵn"):
                for selected_view in selected_views:
                    # for sheet in dest_sheets:
                    logger.debug('Đang đặt vào %s',
                                revit.query.get_name(selected_view))
                    try:
                        DB.Viewport.Create(revit.doc,
                                        dest_sheets.Id,
                                        selected_view.Id,
                                        DB.XYZ(420.5/304.8,297/304.8,0))
                    except Exception as place_err:
                        logger.debug('Lỗi đặt view vào sheet {} -> {}'
                                    .format(selected_view.Id, dest_sheets.Id))
    else:
        forms.alert('Không có view nào được chọn')
