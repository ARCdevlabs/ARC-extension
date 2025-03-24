# -*- coding: utf-8 -*-
import Autodesk
import Autodesk.Revit.DB as DB

class BeamSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
    def AllowElement(self, element):
        return isinstance(element, DB.FamilyInstance) and element.Category.Name in "Structural Framing , 構造フレーム"

def pick_beams_by_rectangle(iuidoc):
    from nances import forms
    with forms.WarningBar(title='Drag to select beams'):
        selection = iuidoc.Selection
        selected_elements = selection.PickElementsByRectangle(BeamSelectionFilter(), "Select Beams")
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