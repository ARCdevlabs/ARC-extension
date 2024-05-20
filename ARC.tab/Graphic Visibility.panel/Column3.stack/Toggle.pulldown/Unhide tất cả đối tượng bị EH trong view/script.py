# -*- coding: utf-8 -*-
__doc__ = Version = 1.0

from Autodesk.Revit.DB import *

# .NET Imports
import os, clr
clr.AddReference("System")
from System.Collections.Generic import List

# ==================================================
doc   = __revit__.ActiveUIDocument.Document

# ==================================================
if __name__ == '__main__':
    all_elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElementIds()
    unhide_elements = List[ElementId](all_elements)

    with Transaction(doc,'Unhide All Elements') as t:
        t.Start()
        doc.ActiveView.UnhideElements(unhide_elements)
        t.Commit()