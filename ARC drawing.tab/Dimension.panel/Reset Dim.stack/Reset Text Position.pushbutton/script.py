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
import traceback
if module.AutodeskData():
	uidoc = __revit__.ActiveUIDocument
	doc = uidoc.Document
from Autodesk.Revit.UI.Selection import ObjectType, Selection
try:
    t0 = Transaction(doc,"Set Work Plane")
    t0.Start()        
    current_view = uidoc.ActiveView
    try:
        module.set_work_plane_for_view (current_view)
    except:
        pass
    t0.Commit() 

    current_selection = module.get_selected_elements(uidoc,doc, False)

    if current_selection == False:
        collector = FilteredElementCollector(uidoc.Document, current_view.Id).OfCategory(BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType()
        pick = uidoc.Selection.PickObject(ObjectType.Element)
        element = doc.GetElement(pick.ElementId)
    else:
        element = current_selection[0]

    # print return_point
    number_of_segments =  element.NumberOfSegments
    t = Transaction(doc,"Reset Text Position")
    t.Start() 
    number_of_segments =  element.NumberOfSegments
    if number_of_segments != 0:
        segments = element.Segments
        for tung_seg in segments:
            tung_seg.ResetTextPosition()
    else:
        element.ResetTextPosition()
    t.Commit()
except:
    # print(traceback.format_exc())
    pass




