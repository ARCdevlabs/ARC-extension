import pickle
from pyrevit import revit
from pyrevit.coreutils import appdata
def get_document_data_file(file_id, file_ext, add_cmd_name=False):
    proj_info = revit.query.get_project_info()

    if add_cmd_name:
        script_file_id = '{}_{}_{}'.format(EXEC_PARAMS.command_name,
                                           file_id,
                                           proj_info.filename
                                           or proj_info.name)
    else:
        script_file_id = '{}_{}'.format(file_id,
                                        proj_info.filename
                                        or proj_info.name)

    return appdata.get_data_file(script_file_id, file_ext)

datafile = get_document_data_file("Remember_type_2", "txt")
selection = revit.get_selection()
for i in selection:
    type = str(i.GetTypeId())
selected_ids = {str(elid.GetTypeId().IntegerValue) for elid in selection}
f = open(datafile, 'w')
pickle.dump(selected_ids, f)
f.close()
