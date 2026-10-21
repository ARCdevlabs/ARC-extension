# -*- coding: utf-8 -*-
# pylint: skip-file
import hooks_logger as hl
import pickle
from pyrevit import revit
from pyrevit.coreutils import appdata
from pyrevit.compat import get_elementid_value_func

#Lưu ý: Code mẫu đang dùng Cpython3, nhưng mà hàm pickle sẽ bị lỗi. Cho nên hãy dùng python 2 với "# -*- coding: utf-8 -*-""

# hl.log_hook(
#     __file__,
#     {
#         "cancellable?": str(__eventargs__.Cancellable),
#         "doc": str(__eventargs__.Document),
#         "current_view": str(__eventargs__.CurrentActiveView),
#         "prev_view": str(__eventargs__.PreviousActiveView),
#         "status": str(__eventargs__.Status),
#     },
#     log_doc_access=True,
# )

def get_document_data_file(file_id, file_ext):

    proj_info = revit.query.get_project_info()

    script_file_id = '{}_{}'.format(file_id,proj_info.name or
                                        proj_info.filename
                                        )
    return appdata.get_data_file(script_file_id, file_ext)

datafile = get_document_data_file("LastView", "txt")

last_view = (__eventargs__.PreviousActiveView)

try:
    get_elementid_value_func = get_elementid_value_func()

    selected_ids = {get_elementid_value_func(last_view.Id)}

    f = open(datafile, 'w')

    pickle.dump(selected_ids, f)

    f.close()
except:
    pass