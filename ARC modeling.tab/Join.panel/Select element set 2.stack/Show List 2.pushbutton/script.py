# -*- coding: utf-8 -*-
import pickle
from pyrevit.coreutils import appdata
from pyrevit import revit
import nances
import Autodesk.Revit.DB as DB
from nances import getelementid

if nances.AutodeskData():
    def get_document_data_file(file_id, file_ext):
        proj_info = revit.query.get_project_info()

        script_file_id = '{}_{}'.format(file_id,
                                        proj_info.filename
                                        or proj_info.name)

        return appdata.get_data_file(script_file_id, file_ext)
    datafile = get_document_data_file("List2", "txt")
    selection = revit.get_selection()
    try:
        
        f = open(datafile, 'r')

        current_selection = pickle.load(f)

        f.close()

        element_ids = []

        get_func = getelementid.get_elementid_from_value_func()

        for elid in current_selection:

            element_ids.append(get_func(elid))

        selection.set_to(element_ids)
    except:
        pass