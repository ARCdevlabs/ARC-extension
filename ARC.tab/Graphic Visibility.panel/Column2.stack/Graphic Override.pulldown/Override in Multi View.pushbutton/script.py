# -*- coding: utf-8 -*-
import string
import importlib
import Autodesk
import nances
import traceback
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit import script
from nances import forms

if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    
    current_view= nances.Active_view(doc)

    Ele = nances.get_elements(uidoc,doc, 'Select elements to copy override', noti = False)

    def get_all_views(idoc):

        collector = FilteredElementCollector(idoc).OfCategory(DB.BuiltInCategory.OST_Views).WhereElementIsNotElementType()

        views = collector.OfClass(View).ToElements()

        valid_views = []

        view_name = []

        for tung_view in views:
                
            if not tung_view.IsTemplate:   
                    
                if str(tung_view.ViewType) in "FloorPlan, CeilingPlan, Elevation, EngineeringPlan, Section, ThreeD":  

                    valid_views.append(tung_view)

                    view_name.append(tung_view.Name)

        return valid_views,view_name

    trans_group = TransactionGroup(doc, "ARC_Override element to other views")

    trans_group.Start()

    # output = script.get_output()

    if Ele:

        all_view = get_all_views(doc)

        list_valid_views = all_view [0]

        list_view_name = all_view [1]
            
        view_elements = forms.SelectFromList.show(list_view_name,title = 'Select Views',width = 500 ,button_name = 'Select',multiselect = True)

        view_dau_ra = []

        if view_elements:

            list_view_da_override = []

            for tung_selected_view_name in view_elements:

                for tung_view,view_name in zip(list_valid_views,list_view_name):
        
                    if view_name == tung_selected_view_name:

                        view_dau_ra.append(tung_view)

            count = 0

            for tung_element in Ele:

                try:

                    t = Transaction(doc, "ARC_subtrans_Override element to other views")

                    t.Start()  

                    override = current_view.GetElementOverrides(tung_element.Id)

                    for tung_view_dau_ra in view_dau_ra:
                                        
                        set_override = tung_view_dau_ra.SetElementOverrides(tung_element.Id,override)

                        

                        list_view_da_override.append(tung_view_dau_ra.Name)

                    t.Commit()
                    
                    count += 1

                except:

                    t.RollBack()

                    pass

            # set_view_dau_ra = set(list_view_da_override)

            nances.message_box("Override " + str(count) + " views")

    trans_group.Assimilate()