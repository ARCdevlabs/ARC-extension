__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib
from nances import getelementid
from pyrevit import script, revit
try:
    ARC = string.ascii_lowercase
    begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
    module = importlib.import_module(str(begin))
    import Autodesk
    from Autodesk.Revit.DB import *
    from System.Collections.Generic import *
    if module.AutodeskData():
        import pickle
        from pyrevit.coreutils import appdata
        from pyrevit.framework import List
        from pyrevit import revit, DB
        def get_document_data_file(file_id, file_ext):
            proj_info = revit.query.get_project_info()

            script_file_id = '{}_{}'.format(file_id,proj_info.name or
                                            proj_info.filename
                                            )

            return appdata.get_data_file(script_file_id, file_ext)
        
        datafile = get_document_data_file("FavoriteView", "txt")

        selection = revit.get_selection()

        try:
            f = open(datafile, 'r')

            current_selection = pickle.load(f)

            f.close()

            element_ids = []

            get_elementid_from_string_func = getelementid.get_elementid_from_value_func()

            for elid in current_selection:

                element_ids.append(get_elementid_from_string_func(elid))

            selection.set_to(element_ids)

            output = script.get_output()

            output.close_others(True)

            # print dir(output)

            if len(selection.element_ids) > 0:
                output.set_width(300)

                # if len(selection.element_ids) < 50:
                #     print('{}'.format(output.linkify(selection.element_ids,
                #                                     title='All Elements')))

                for idx, element in enumerate(selection.elements):
                    print('{}: {} {}'.format(idx+1,
                                            output.linkify(element.Id),
                                            revit.query.get_name(element)
                                            ))

        except Exception:
            pass
except:
    pass        
