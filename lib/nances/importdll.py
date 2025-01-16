# -*- coding: utf-8 -*-
import os
import os.path as op
import clr
class ImportDLL:
    def __init__(self):
        self.LibARC_Geometry = None
        self.LibARC_Method = None
        self.LibARC_Security = None
        self.LibARC_Selection = None
        self.LibARC_VectorMath = None
    def get_dll(self):
        appdata_path = os.path.join(os.getenv('APPDATA'), 'pyRevit', 'Extensions')
        programdata_path = (r"C:\ProgramData\pyRevit\Extensions")
        nances_lib_path = os.path.join(appdata_path, 'ARC extension.extension', 'lib', 'nances', 'dll')
        path_string = op.join(nances_lib_path, 'LibARC_250108.dll')
        path_string_programdata = op.join(programdata_path, 'LibARC_250108.dll')
        try:
            clr.AddReferenceToFileAndPath(path_string)
        except:
            clr.AddReferenceToFileAndPath(path_string_programdata)
        from NS.LibARC import LibARCSecurity, LibARC_Geometry, LibARC_VectorMath, LibARC_Selection, LibARC_Geometry, LibARC_Method
        self.LibARC_Geometry = LibARC_Geometry
        self.LibARC_Method = LibARC_Method
        self.LibARC_Security = LibARCSecurity
        self.LibARC_Selection = LibARC_Selection
        self.LibARC_VectorMath = LibARC_VectorMath        
        return self
