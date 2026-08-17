# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import pickle
from pyrevit import revit
from pyrevit.coreutils import appdata
import nances
from nances import getelementid
if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document

    def get_document_data_file(file_id, file_ext):
        proj_info = revit.query.get_project_info()
        script_file_id = '{}_{}'.format(file_id,
                                        proj_info.filename
                                        or proj_info.name)

        return appdata.get_data_file(script_file_id, file_ext)

    datafile = get_document_data_file("RememberType1", "txt")

    selection = nances.get_element(uidoc,doc, "Select Element to Remember Type", noti = False)

    list_id = []

    for i in selection:

        type = i.GetTypeId()
        
        list_id.append(type)

    get_elementid_value_func = getelementid.get_elementid_value_func()

    list_string_id = []
    
    for tung_string_id in list_id:

        tung_id = get_elementid_value_func(tung_string_id)

        list_string_id.append(tung_id)

    selected_ids = set(list_string_id)

    f = open(datafile, 'w')

    pickle.dump(selected_ids, f)

    f.close()
