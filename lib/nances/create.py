# -*- coding: utf-8 -*-
import Autodesk
import Autodesk.Revit.DB as DB
import math

def detail_line (doc, view, line):
    detail_line= doc.Create.NewDetailCurve(view,line)
    return detail_line