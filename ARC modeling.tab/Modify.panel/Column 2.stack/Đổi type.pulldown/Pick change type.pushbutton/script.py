__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import *

# Get UIDocument
uidoc = __revit__.ActiveUIDocument
# Get Document
doc = uidoc.Document
Currentview = doc.ActiveView


def ChangeType(element, typeId):
    element.ChangeTypeId(typeId)
    return element

def main():
    first_pick = uidoc.Selection.PickObject(ObjectType.Element)
    first_id = first_pick.ElementId
    first_ele = doc.GetElement(first_id)
    while True:
        try:
            second_pick = uidoc.Selection.PickObject(ObjectType.Element)
            second_id = second_pick.ElementId
            second_ele = doc.GetElement(second_id)
            try:
                t = Transaction(doc, "Change type same category")
                t.Start()
                try:
                    ChangeType(second_ele, first_ele.GetTypeId())
                except:
                    pass
                t.Commit()
            except:
                pass
        except Exception as ex:
            if "Operation canceled by user." in str(ex):
                break
            else:
                break
main()