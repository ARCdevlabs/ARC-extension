import pickle
from pyrevit import revit,forms
from pyrevit.coreutils import appdata
from nances import getelementid


def get_document_data_file(file_id, file_ext):
    proj_info = revit.query.get_project_info()

    script_file_id = '{}_{}'.format(file_id,proj_info.name 
                                    or proj_info.filename
                                    )   
    return appdata.get_data_file(script_file_id, file_ext)

selected_views = forms.select_views(use_selection=True)
list_view_id = []
for tung_view in selected_views:
    list_view_id.append(tung_view.Id)
datafile = get_document_data_file("FavoriteView", "txt")

# selection = revit.get_selection()

get_elementid_value_func = getelementid.get_elementid_value_func()

selected_ids = {get_elementid_value_func(elid) for elid in list_view_id}

f = open(datafile, 'w')

pickle.dump(selected_ids, f)

f.close()

