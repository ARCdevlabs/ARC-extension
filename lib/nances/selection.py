# -*- coding: utf-8 -*-
import Autodesk
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List

class BeamSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
    def AllowElement(self, element):
        return isinstance(element, DB.FamilyInstance) and element.Category.Name in "Structural Framing , 構造フレーム"

def pick_beams_by_rectangle(iuidoc):
    from nances import forms
    with forms.WarningBar(title='Drag to select beams'):
        selection = iuidoc.Selection
        selected_elements = selection.PickElementsByRectangle(BeamSelectionFilter(), "Select Beams")
    return selected_elements

class MassSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
    # standard API override function
    def AllowElement(self, element):
        if not element.ViewSpecific:
            return True
        else:
            return False

    # standard API override function
    def AllowReference(self, refer, point):
        return False

def pick_model_by_rectangle(iuidoc):
    from nances import forms
    with forms.WarningBar(title='Drag to select element'):
        selection = iuidoc.Selection
        selected_elements = selection.PickElementsByRectangle(MassSelectionFilter(), "Select Elements")
    return selected_elements

    
class DimensionSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
    def AllowElement(self, element):
        return element.Category.Name in "Dimensions , 寸法"


def pick_dimension_by_rectangle(iuidoc):
    from nances import forms
    with forms.WarningBar(title='Drag to select dimensions'):
        selection = iuidoc.Selection
        selected_elements = selection.PickElementsByRectangle(DimensionSelectionFilter(), "Select Dimensions")
    return selected_elements

class LineSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
    def AllowElement(self, element):
        return element.Category.Name in "Lines, 線分"

def pick_lines_by_rectangle(iuidoc):
    from nances import forms
    with forms.WarningBar(title='Drag to select lines'):
        selection = iuidoc.Selection
        selected_elements = selection.PickElementsByRectangle(LineSelectionFilter(), "Select Lines")
    return selected_elements

def select_sau_khi_chay_tool (list_elements, uidoc):
    if len(list_elements) > 0:
        select = uidoc.Selection
        list_id = []
        for tung_element in list_elements:
            element_id = tung_element.Id
            list_id.append(element_id)
        Icollection = List[DB.ElementId](list_id)
        select.SetElementIds(Icollection)
    return

def get_all_grid(doc, active_view):
    collector = DB.FilteredElementCollector(doc, active_view.Id).OfClass(DB.Grid)
    visible_grids = [grid for grid in collector if not grid.ViewSpecific]
    return visible_grids