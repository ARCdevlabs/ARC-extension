import pickle
from pyrevit import revit
from pyrevit.coreutils import appdata
def get_document_data_file(file_id, file_ext, add_cmd_name=False):
    """Return filename to be used by a user script to store data.

    File name is generated in this format:
    ``pyRevit_{Revit Version}_{file_id}_{Project Name}.{file_ext}``

    Example:
        >>> script.get_document_data_file('mydata', 'data')
        '.../pyRevit_2018_mydata_Project1.data'
        >>> script.get_document_data_file('mydata', 'data', add_cmd_name=True)
        '.../pyRevit_2018_Command Name_mydata_Project1.data'

    Document data files are not cleaned up at pyRevit startup.
    Script should manage cleaning up these files.

    Args:
        file_id (str): unique id for the filename
        file_ext (str): file extension
        add_cmd_name (bool, optional): add command name to file name

    Returns:
        str: full file path
    """
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

datafile = get_document_data_file("List2", "txt")
selection = revit.get_selection()
selected_ids = {str(elid.IntegerValue) for elid in selection.element_ids}

f = open(datafile, 'w')
pickle.dump(selected_ids, f)
f.close()
