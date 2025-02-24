__doc__ = 'python for revit api'
__author__ = 'SonKawamura'
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection  import ObjectType
from Autodesk.Revit.DB import*
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Element
from System.Collections.Generic import *
from rpw import ui
from rpw.ui.forms import Alert
from rpw.ui.forms import SelectFromList
import nances
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
if nances.AutodeskData():
    try:
        Currentview = doc.ActiveView
        NewList = []
        ListAnotation =[]
        ListAnotationInCurrentView = []
        ListClone = []
        value = SelectFromList('Please select category', ['Floor','Wall','Door','Window','StructuralColumn','StructuralFraming'])
        def all_elements_of_category(category):
            return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()
        if value == 'Floor':
            AllEleOfCategory = all_elements_of_category(BuiltInCategory.OST_Floors)
        elif value == 'Wall':
            AllEleOfCategory = all_elements_of_category(BuiltInCategory.OST_Walls)
        elif value == 'Door':
            AllEleOfCategory = all_elements_of_category(BuiltInCategory.OST_Doors)
        elif value == 'Window':
            AllEleOfCategory = all_elements_of_category(BuiltInCategory.OST_Windows)
        elif value == 'StructuralColumn':
            AllEleOfCategory = all_elements_of_category(BuiltInCategory.OST_StructuralColumns)
        elif value == 'StructuralFraming':
            AllEleOfCategory = all_elements_of_category(BuiltInCategory.OST_StructuralFraming)
        #List tag in current view
        ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_WallTags))
        ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_DoorTags))
        ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_WindowTags))
        ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_FloorTags))
        ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_StructuralColumnTags))
        ListAnotation.append(all_elements_of_category(BuiltInCategory.OST_StructuralFramingTags))
        ListAnotation = [item for items in ListAnotation for item in items]
        CurrentviewId = Currentview.Id
        ParentView = Currentview.GetPrimaryViewId()
        for a in ListAnotation:
            WhatView = a.OwnerViewId
            if str(WhatView) == str(CurrentviewId):
                ListAnotationInCurrentView.append(a)
            elif str(WhatView) == str(ParentView):
                ListAnotationInCurrentView.append(a)
        for i in AllEleOfCategory:
            EleId = i.Id
            ListClone.append(i)
            for b in ListAnotationInCurrentView:
                host = b.TaggedLocalElementId
                if host == EleId:
                    ListClone.Remove(i)
        def TempIsolate(view, items):
            ielements = List[ElementId]([x.Id for x in items])
            view.IsolateElementsTemporary(ielements)
        t = Transaction(doc,"Isolate Elements don't have tag")
        t.Start()
        TempIsolate(Currentview, ListClone)
        t.Commit()
    except:
        pass
