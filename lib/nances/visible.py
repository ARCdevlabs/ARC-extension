# -*- coding: utf-8 -*-
import Autodesk
import Autodesk.Revit.DB as DB
import math

def check_hide_isolate(element,view):
    view_mode = DB.TemporaryViewMode.TemporaryHideIsolate
    boolean = view.IsElementVisibleInTemporaryViewMode(view_mode, element.Id)
    return boolean
def check_hidden(element, view):
    boolean = element.IsHidden(view)
    not_boolean = not(boolean)
    return not_boolean


