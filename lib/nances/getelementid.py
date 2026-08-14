# -*- coding: utf-8 -*-
import sys
import System

def _get_revit_version():
    """Returns the current Revit version as an integer."""
    if __revit__ is None:
        return NO_REVIT
    try:
        # UIApplication
        return int(__revit__.Application.VersionNumber)
    except AttributeError:
        pass
    try:
        # Application, (ControlledApplication)
        return int(__revit__.VersionNumber)
    except AttributeError:
        # ControlledApplication
        return int(__revit__.ControlledApplication.VersionNumber)
    
def get_elementid_value_func():
    """Returns the ElementId value extraction function based on the Revit version.

    Follows API changes in Revit 2024.

    Returns:
        function: A function returns the value of an ElementId.

    Examples:
        ```python
        get_elementid_value = get_elementid_value_func()
        sheet_revids = {get_elementid_value(x) for x in self.revit_sheet.GetAllRevisionIds()}
        add_sheet_revids = {get_elementid_value(x) for x in self.revit_sheet.GetAdditionalRevisionIds()}
        ```
    """
    attr = "Value" if _get_revit_version() > 2023 else "IntegerValue"
    def from_elementid(item):
        return getattr(item, attr)
    return from_elementid


def get_elementid_from_value_func():
    """Returns the ElementId constructor function based on the Revit version.

    Follows API changes in Revit 2024.

    Returns:
        function: A function that takes a numeric value and returns an ElementId.

    Example:
        ```python
        get_elementid_from_value = get_elementid_from_value_func()
        element_id = get_elementid_from_value(123456)
        ```
    """
    from pyrevit.api import DB
    cast_class = System.Int64 if _get_revit_version() > 2023 else int
    def from_value(value):
        return DB.ElementId(cast_class(value))
    return from_value



