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
from nances import getelementid
try:
    if module.AutodeskData():
        import pickle
        from pyrevit.coreutils import appdata
        from pyrevit.framework import List
        from pyrevit import revit, DB

        def get_document_data_file(file_id, file_ext):
            proj_info = revit.query.get_project_info()

            script_file_id = '{}_{}'.format(file_id,
                                            proj_info.filename
                                            or proj_info.name)

            return appdata.get_data_file(script_file_id, file_ext)
        
        datafile = get_document_data_file("RememberType1", "txt")
        
        selection = revit.get_selection()
        try:
            f = open(datafile, 'r')

            current_selection = pickle.load(f)

            f.close()

            element_ids = []

            get_elementid_from_string_func = getelementid.get_elementid_from_value_func()

            for elid in current_selection:

                element_ids.append(get_elementid_from_string_func(elid))

            if len(element_ids) == 0:

                from pyrevit.coreutils import applocales

                current_applocale = applocales.get_current_applocale()

                if str(current_applocale) == "日本語 / Japanese (ja)":

                    message = "このコマンドを使用する前に、タイプ記憶 (1) コマンドを使用してください。"
                else:

                    message = "Hãy sử dụng tool Ghi nhớ type (1) trước khi sử dụng tool này"

                module.message_box(message)
                import sys
                sys.exit()
        except Exception:
            pass    

    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    def ChangeType(element, typeId):
        try:
            element.ChangeTypeId(typeId)
            return element
        except:
            pass

    try:
        Ele = module.get_elements(uidoc,doc, "Select Element to Change Type", noti = False)
        t = Transaction (doc, "Change type 1")
        t.Start()
        for i in Ele:
            ChangeType(i, element_ids[0])
        t.Commit()
    except:
        pass
except:
    pass