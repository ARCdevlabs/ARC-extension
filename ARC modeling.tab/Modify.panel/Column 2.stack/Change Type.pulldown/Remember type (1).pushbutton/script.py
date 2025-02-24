# -*- coding: utf-8 -*-
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = ''.join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
import traceback
import pickle
from pyrevit import revit
from pyrevit.coreutils import appdata

import nances
if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
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

    datafile = get_document_data_file("Remember_type_1", "txt")
    selection = module.get_element(uidoc,doc, "Select Element to Remember Type", noti = False)
    for i in selection:
        type = str(i.GetTypeId())
    selected_ids = {str(elid.GetTypeId().IntegerValue) for elid in selection}
    f = open(datafile, 'w')
    pickle.dump(selected_ids, f)
    f.close()
