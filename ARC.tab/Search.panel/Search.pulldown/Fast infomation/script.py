# -*- coding: utf-8 -*-
import Autodesk
import nances
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
if nances.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    Ele = nances.get_selected_elements(uidoc,doc)
    selection = uidoc.Selection
    # t = Transaction (doc, "Quick Properties")
    list_noname_ref = []
    for tung_element in Ele:
        name = tung_element.Name
        if name == "Reference Plane":
            list_noname_ref.append(tung_element.Id)
            print name
    Icollection = List[ElementId](list_noname_ref)
    selection.SetElementIds(Icollection)
    ''' Ham nay dung de in ra traceback truoc khi bo qua loi
    try:
        Code
    except:
        print(traceback.format_exc())
        pass
    '''
    # def encode_to_base64(input_string):

    # def flatten_list(list):

    # def get_selected_elements(tem_uidoc, tem_doc):

    # def Active_view(idoc):

    # def get_parameter_by_name(element, name, is_UTF8 = False)

    # def get_parameter_value_by_name(element, name, is_UTF8 = False)

    # def set_parameter_value_by_name(element, name, value, is_UTF8 = False)

    # def get_type(idoc, element)

    # def get_type_name (idoc, element)

    # def all_type_of_class_and_OST (idoc, ofClass, BuiltInCategory_OST): 
        ##### vi du khi category co san Class: list_type = all_type_of_class_and_OST(doc, FloorType, BuiltInCategory.OST_Floors)
        ##### vi du ve FamilySymbol: list_type = all_type_of_class_and_OST(FamilySymbol, BuiltInCategory.OST_StructuralFraming)

    # def get_all_elements_of_OST(idoc, BuiltInCategory_OST): "Vi du: floor = module.get_all_elements_of_OST(doc, BuiltInCategory.OST_Floors)"

    # def get_current_selection(iuidoc,element)



    # t.Start()
    # list_ele = []
    # for i in Ele:
    #     print i.UniqueId

    # # module.get_current_selection(uidoc,list_ele)
    # # floor = module.get_all_elements_of_OST(doc, DB.BuiltInCategory.OST_Floors)
    # t.Commit()        
