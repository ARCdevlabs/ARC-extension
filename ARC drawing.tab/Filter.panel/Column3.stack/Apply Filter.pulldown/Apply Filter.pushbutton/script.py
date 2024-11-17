# -*- coding: utf-8 -*-
import clr
import Autodesk
from Autodesk.Revit.DB import View, OverrideGraphicSettings, FilteredElementCollector,FillPatternTarget, ElementParameterFilter, FilterRule, ParameterFilterRuleFactory, FilterElement, FilteredElementCollector, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, ParameterFilterElement, Transaction, BuiltInParameter, BuiltInCategory, WallType, ElementId, FilterRule, ParameterFilterElement, ElementParameterFilter, ParameterFilterRuleFactory
import Autodesk.Revit.UI.Selection
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
if module.AutodeskData():    
    from nances import forms
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    view = doc.ActiveView
    # List corlor
    Color0 = Autodesk.Revit.DB.Color(232,232,255)
    Color1 = Autodesk.Revit.DB.Color(244,204,204)
    Color2 = Autodesk.Revit.DB.Color(252,229,205)
    Color3 = Autodesk.Revit.DB.Color(207,226,243)
    Color4 = Autodesk.Revit.DB.Color(225,230,236)
    Color5 = Autodesk.Revit.DB.Color(234,209,220)
    Color6 = Autodesk.Revit.DB.Color(234,153,153)
    Color7 = Autodesk.Revit.DB.Color(249,203,156)
    Color8 = Autodesk.Revit.DB.Color(255,229,153)
    Color9 = Autodesk.Revit.DB.Color(224,234,209)
    Color10 = Autodesk.Revit.DB.Color(162,196,201)
    Color11 = Autodesk.Revit.DB.Color(159,197,232)
    Color12 = Autodesk.Revit.DB.Color(225,220,236)
    Color13 = Autodesk.Revit.DB.Color(213,166,189)
    Color14 = Autodesk.Revit.DB.Color(234, 209, 220)
    Color15 = Autodesk.Revit.DB.Color(111, 168, 220)
    # Color16 = Autodesk.Revit.DB.Color(248,250,244)
    # Color17 = Autodesk.Revit.DB.Color(244,204,204)
    # Color18 = Autodesk.Revit.DB.Color(252,229,205)
    # Color19 = Autodesk.Revit.DB.Color(207,226,243)
    # Color20 = Autodesk.Revit.DB.Color(175,238,238)
    # Color21 = Autodesk.Revit.DB.Color(234,209,220)
    # Color22 = Autodesk.Revit.DB.Color(234,153,153)
    # Color23 = Autodesk.Revit.DB.Color(249,203,156)
    # Color24 = Autodesk.Revit.DB.Color(255,229,153)
    # Color25 = Autodesk.Revit.DB.Color(224,234,209)
    # Color26 = Autodesk.Revit.DB.Color(162,196,201)
    # Color27 = Autodesk.Revit.DB.Color(159,197,232)
    # Color28 = Autodesk.Revit.DB.Color(225,220,236)
    # Color29 = Autodesk.Revit.DB.Color(213, 166, 189)
    # Color30 = Autodesk.Revit.DB.Color(234, 209, 220)
    # Color31 = Autodesk.Revit.DB.Color(111, 168, 220)    
    # Color32 = Autodesk.Revit.DB.Color(248,250,244)
    # Color33 = Autodesk.Revit.DB.Color(244,204,204)
    # Color34 = Autodesk.Revit.DB.Color(252,229,205)
    # Color35 = Autodesk.Revit.DB.Color(207,226,243)
    # Color36 = Autodesk.Revit.DB.Color(175,238,238)
    # Color37 = Autodesk.Revit.DB.Color(234,209,220)
    # Color38 = Autodesk.Revit.DB.Color(234,153,153)
    # Color39 = Autodesk.Revit.DB.Color(249,203,156)
    # Color40 = Autodesk.Revit.DB.Color(255,229,153)
    # Color41 = Autodesk.Revit.DB.Color(224,234,209)
    # Color42 = Autodesk.Revit.DB.Color(162,196,201)
    # Color43 = Autodesk.Revit.DB.Color(159,197,232)
    # Color44 = Autodesk.Revit.DB.Color(225,220,236)
    # Color45 = Autodesk.Revit.DB.Color(213, 166, 189)
    # Color46 = Autodesk.Revit.DB.Color(234, 209, 220)
    # Color47 = Autodesk.Revit.DB.Color(111, 168, 220)
    # Color48 = Autodesk.Revit.DB.Color(248,250,244)
    # Color49 = Autodesk.Revit.DB.Color(244,204,204)
    # Color50 = Autodesk.Revit.DB.Color(252,229,205)
    # Color51 = Autodesk.Revit.DB.Color(207,226,243)
    # Color52 = Autodesk.Revit.DB.Color(175,238,238)
    # Color53 = Autodesk.Revit.DB.Color(234,209,220)
    # Color54 = Autodesk.Revit.DB.Color(234,153,153)
    # Color55 = Autodesk.Revit.DB.Color(249,203,156)
    # Color56 = Autodesk.Revit.DB.Color(255,229,153)
    # Color57 = Autodesk.Revit.DB.Color(224,234,209)
    # Color58 = Autodesk.Revit.DB.Color(162,196,201)
    # Color59 = Autodesk.Revit.DB.Color(159,197,232)
    # Color60 = Autodesk.Revit.DB.Color(225,220,236)
    # Color61 = Autodesk.Revit.DB.Color(213, 166, 189)
    # Color62 = Autodesk.Revit.DB.Color(234, 209, 220)
    # Color63 = Autodesk.Revit.DB.Color(111, 168, 220)
    # Color64 = Autodesk.Revit.DB.Color(248,250,244)
    # Color65 = Autodesk.Revit.DB.Color(244,204,204)
    # Color66 = Autodesk.Revit.DB.Color(252,229,205)
    # Color67 = Autodesk.Revit.DB.Color(207,226,243)
    # Color68 = Autodesk.Revit.DB.Color(175,238,238)
    # Color69 = Autodesk.Revit.DB.Color(234,209,220)
    # Color70 = Autodesk.Revit.DB.Color(234,153,153)
    # Color71 = Autodesk.Revit.DB.Color(249,203,156)
    # Color72 = Autodesk.Revit.DB.Color(255,229,153)
    # Color73 = Autodesk.Revit.DB.Color(248,250,244)
    # Color74 = Autodesk.Revit.DB.Color(162,196,201)
    # Color75 = Autodesk.Revit.DB.Color(159,197,232)
    # Color76 = Autodesk.Revit.DB.Color(225,220,236)
    # Color77 = Autodesk.Revit.DB.Color(213, 166, 189)
    # Color78 = Autodesk.Revit.DB.Color(234, 209, 220)
    # Color79 = Autodesk.Revit.DB.Color(111, 168, 220)
    # Color80 = Autodesk.Revit.DB.Color(224,234,209)
    # Color81 = Autodesk.Revit.DB.Color(244,204,204)
    # Color82 = Autodesk.Revit.DB.Color(252,229,205)
    # Color83 = Autodesk.Revit.DB.Color(207,226,243)
    # Color84 = Autodesk.Revit.DB.Color(175,238,238)
    # Color85 = Autodesk.Revit.DB.Color(234,209,220)
    # Color86 = Autodesk.Revit.DB.Color(234,153,153)
    # Color87 = Autodesk.Revit.DB.Color(249,203,156)
    # Color88 = Autodesk.Revit.DB.Color(255,229,153)
    # Color89 = Autodesk.Revit.DB.Color(224,234,209)
    # Color90 = Autodesk.Revit.DB.Color(162,196,201)
    # Color91 = Autodesk.Revit.DB.Color(159,197,232)
    # Color92 = Autodesk.Revit.DB.Color(225,220,236)
    # Color93 = Autodesk.Revit.DB.Color(213, 166, 189)
    # Color94 = Autodesk.Revit.DB.Color(234, 209, 220)
    # Color95 = Autodesk.Revit.DB.Color(111, 168, 220)
    # Color96 = Autodesk.Revit.DB.Color(248,250,244)
    # Color97 = Autodesk.Revit.DB.Color(244,204,204)
    # Color98 = Autodesk.Revit.DB.Color(252,229,205)
    # Color99 = Autodesk.Revit.DB.Color(207,226,243)
    # Color100 = Autodesk.Revit.DB.Color(175,238,238)



    
    # list_color = [
    #             Color0, Color1, Color2, Color3, Color4, Color5, 
    #             Color6, Color7, Color8, Color9, Color10, 
    #             Color11, Color12, Color13, Color14, Color15,
    #             Color16, Color17, Color18, Color19, Color20,
    #             Color21, Color22, Color23, Color24, Color25,
    #             Color26, Color27, Color28, Color29, Color30,
    #             Color31, Color32, Color33, Color34, Color35,
    #             Color36, Color37, Color38, Color39, Color40,
    #             Color41, Color42, Color43, Color44, Color45,
    #             Color46, Color47, Color48, Color49, Color50,
    #             Color51, Color52, Color53, Color54, Color55,
    #             Color56, Color57, Color58, Color59, Color60,
    #             Color61, Color62, Color63, Color64, Color65,
    #             Color66, Color67, Color68, Color69, Color70,
    #             Color71, Color72, Color73, Color74, Color75,
    #             Color76, Color77, Color78, Color79, Color80,
    #             Color81, Color82, Color83, Color84, Color85,
    #             Color86, Color87, Color88, Color89, Color90,
    #             Color91, Color92, Color93, Color94, Color95,
    #             Color96, Color97, Color98, Color99, Color100
    #             ]
    list_color = [
                Color0, Color1, Color2, Color3, Color4, Color5, 
                Color6, Color7, Color8, Color9, Color10, 
                Color11, Color12, Color13, Color14, Color15,
                Color0, Color1, Color2, Color3, Color4, Color5, 
                Color6, Color7, Color8, Color9, Color10, 
                Color11, Color12, Color13, Color14, Color15,
                Color0, Color1, Color2, Color3, Color4, Color5, 
                Color6, Color7, Color8, Color9, Color10, 
                Color11, Color12, Color13, Color14, Color15,
                Color0, Color1, Color2, Color3, Color4, Color5, 
                Color6, Color7, Color8, Color9, Color10, 
                Color11, Color12, Color13, Color14, Color15,
                Color0, Color1, Color2, Color3, Color4, Color5, 
                Color6, Color7, Color8, Color9, Color10, 
                Color11, Color12, Color13, Color14, Color15,
                Color0, Color1, Color2, Color3, Color4, Color5, 
                Color6, Color7, Color8, Color9, Color10, 
                Color11, Color12, Color13, Color14, Color15,
                Color0, Color1, Color2, Color3, Color4, Color5, 
                Color6, Color7, Color8, Color9, Color10, 
                Color11, Color12, Color13, Color14, Color15,
                Color0, Color1, Color2, Color3, Color4, Color5, 
                Color6, Color7, Color8, Color9, Color10, 
                Color11, Color12, Color13, Color14, Color15,
                Color0, Color1, Color2, Color3, Color4, Color5, 
                Color6, Color7, Color8, Color9, Color10, 
                Color11, Color12, Color13, Color14, Color15,                
                ]
    # random.shuffle(list_color)

    def all_type():
        all_OST_type = FilteredElementCollector(doc).OfClass(WallType).OfCategory(BuiltInCategory.OST_Walls)
        return all_OST_type
    def get_filter_elements():
        filter_elements = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()
        return filter_elements
    list_filters = get_filter_elements()
    name = []
    select_filter = forms.select_view_filter()
    checked_items = select_filter
    if checked_items and len(checked_items) > 0:
        from rpw.ui.forms import SelectFromList
        value = SelectFromList('Override Fore ground or Back ground?', ['Fore ground','Back ground'])
        t = Transaction (doc, "Apply filter to view")
        t.Start()
        list_tem = []  
        GetFillPattern = Autodesk.Revit.DB.FillPatternElement.GetFillPatternElementByName(doc,FillPatternTarget.Drafting,"<Solid fill>")
        if str(GetFillPattern) == "None":
            GetFillPattern = Autodesk.Revit.DB.FillPatternElement.GetFillPatternElementByName(doc,FillPatternTarget.Drafting,"<塗り潰し>")
        for i in list_filters:
            list_tem.append(i)
        for i_name in checked_items:
            override_settings = OverrideGraphicSettings()
            index_i = checked_items.index(i_name)
            random_color = list_color[index_i]
            if value == "Fore ground":
                override_settings.SetSurfaceForegroundPatternColor(random_color)
                override_settings.SetSurfaceForegroundPatternId(GetFillPattern.Id)
                override_settings.SetCutForegroundPatternColor(random_color)
                override_settings.SetCutForegroundPatternId(GetFillPattern.Id)
            else:
                override_settings.SetSurfaceBackgroundPatternColor(random_color)
                override_settings.SetSurfaceBackgroundPatternId(GetFillPattern.Id)
                override_settings.SetCutBackgroundPatternColor(random_color)
                override_settings.SetCutBackgroundPatternId(GetFillPattern.Id)
            for wall in list_tem:
                wall_name = Autodesk.Revit.DB.Element.Name.GetValue(wall)
                if i_name == wall_name:
                    try:
                        view_template = doc.GetElement(view.ViewTemplateId)
                        view_template_name = Autodesk.Revit.DB.Element.Name.GetValue(view_template)
                        if view_template:
                            view_template.AddFilter(wall.Id)
                            view_template.SetFilterOverrides(wall.Id, override_settings)
                            index = list_tem.index(wall)
                            list_tem.pop(index)
                        else:
                            view.AddFilter(wall.Id)
                            view.SetFilterOverrides(wall.Id, override_settings)
                            index = list_tem.index(wall)
                            list_tem.pop(index)
                    except:
                        pass
        t.Commit()  
    else:
        module.message_box("No any Filter was selected")
        import sys
        sys.exit()

