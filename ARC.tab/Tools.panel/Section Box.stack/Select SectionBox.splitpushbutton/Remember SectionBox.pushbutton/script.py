import pickle
from pyrevit import revit
from pyrevit.coreutils import appdata
from nances import getelementid

def get_document_data_file(file_id, file_ext):
    proj_info = revit.query.get_project_info()

    script_file_id = '{}_{}'.format(file_id,
                                        proj_info.filename
                                        or proj_info.name)

    return appdata.get_data_file(script_file_id, file_ext)

datafile = get_document_data_file("Sectionbox", "txt")

selection = revit.get_selection()

get_elementid_value_func = getelementid.get_elementid_value_func()

selected_ids = {get_elementid_value_func(elid) for elid in selection.element_ids}

f = open(datafile, 'w')

pickle.dump(selected_ids, f)

f.close()

