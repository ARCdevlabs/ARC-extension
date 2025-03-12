# -*- coding: utf-8 -*-
import string
import codecs
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    def xac_dinh_dam_doc(elements):
        list_dam_doc = []
        for tung_dam in elements:
            try:
                param_start_level_offset = module.get_builtin_parameter_by_name(tung_dam, BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION)
            except:
                pass
            if param_start_level_offset:
                param_get_elevation_at_top = module.get_builtin_parameter_by_name(tung_dam, BuiltInParameter.STRUCTURAL_ELEVATION_AT_TOP)
                if param_get_elevation_at_top:
                    if not param_get_elevation_at_top.HasValue:
                        list_dam_doc.append(tung_dam)
        return list_dam_doc

    beam = module.get_all_elements_of_OST_in_current_view(doc, BuiltInCategory.OST_StructuralFraming)
    chon_dam_doc = xac_dinh_dam_doc(beam)
    select = module.get_current_selection(uidoc,chon_dam_doc)
 
