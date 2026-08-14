# -*- coding: utf-8 -*-
import pickle
from pyrevit.coreutils import appdata
from pyrevit import revit
import nances
from nances import getelementid
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
# create an instance of _ExecutorParams wrapping current runtime.
if nances.AutodeskData():
    
    def get_document_data_file(file_id, file_ext):

        proj_info = revit.query.get_project_info()

        script_file_id = '{}_{}'.format(file_id,
                                        proj_info.filename
                                        or proj_info.name)
        
        return appdata.get_data_file(script_file_id, file_ext)

    datafile = get_document_data_file("List2", "txt")
    selection = nances.get_elements(uidoc,doc, "Select List Element 2 to Join Geometry", noti = False)
    list_id =[]
    for tung_element in selection:
        list_id.append(tung_element.Id)

    get_elementid_value = getelementid.get_elementid_value_func()
    selected_ids = {str(get_elementid_value(elid)) for elid in list_id}

    f = open(datafile, 'w')
    pickle.dump(selected_ids, f)
    f.close()
