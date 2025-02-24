
# -*- coding: utf-8 -*-
__doc__ = 'nguyenthanhson1712@gmail.com'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
from Autodesk.Revit.DB import *
from pyrevit import DB, script, revit
# .NET Imports
import os, clr
clr.AddReference("System")
from System.Collections.Generic import List

# ==================================================
doc   = __revit__.ActiveUIDocument.Document

# ==================================================
active_view = revit.active_view

all_elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
list_3D =[]
for i in all_elements:
    try:
        category_type = i.Category.CategoryType
        if str(category_type) == "Model":
            list_3D.append(i.Id)
    except:
        pass

unhide_elements = List[ElementId]([x for x in list_3D])
t = Transaction (doc, "Unhide đối tượng 3D")
t.Start()  
doc.ActiveView.UnhideElements(unhide_elements)
t.Commit()