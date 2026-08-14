# -*- coding: utf-8 -*-
import clr
clr.AddReference("System")
from System import Array
import System
import sys
import random
from System.Drawing import Size, Color, Font, FontStyle
from System import Drawing
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Form, SelectionMode , CheckedListBox,CheckedListBox, Keys, Button, TextBox, Label, Panel, MessageBox, SelectionMode
from System.Collections.Generic import List
import Autodesk
from Autodesk.Revit import DB
from Autodesk.Revit.DB import View, OverrideGraphicSettings, FilteredElementCollector,FillPatternTarget, ElementParameterFilter, FilterRule, ParameterFilterRuleFactory, FilterElement, FilteredElementCollector, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, ParameterFilterElement, Transaction, BuiltInParameter, BuiltInCategory, WallType, ElementId, FilterRule, ParameterFilterElement, ElementParameterFilter, ParameterFilterRuleFactory
import Autodesk.Revit.UI.Selection
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    view = doc.ActiveView
    t = Transaction (doc, "Apply filter to view")
    t.Start()
    # List corlor
    Color0 = Autodesk.Revit.DB.Color(152,251,152)
    Color1 = Autodesk.Revit.DB.Color(0,255,127)
    Color2 = Autodesk.Revit.DB.Color(224,255,255)
    Color3 = Autodesk.Revit.DB.Color(127,255,212)
    Color4 = Autodesk.Revit.DB.Color(175,238,238)
    Color5 = Autodesk.Revit.DB.Color(32,178,170)
    Color6 = Autodesk.Revit.DB.Color(0,139,139)
    Color7 = Autodesk.Revit.DB.Color(176,224,230)
    Color8 = Autodesk.Revit.DB.Color(135,206,250)
    Color9 = Autodesk.Revit.DB.Color(135,206,235)
    Color10 = Autodesk.Revit.DB.Color(176,196,222)
    Color11 = Autodesk.Revit.DB.Color(65,105,225)
    Color12 = Autodesk.Revit.DB.Color(123,104,238)
    Color13 = Autodesk.Revit.DB.Color(230,230,250)
    Color14 = Autodesk.Revit.DB.Color(216,191,216)
    Color15 = Autodesk.Revit.DB.Color(238,130,238)
    Color16 = Autodesk.Revit.DB.Color(255,182,193)
    Color17 = Autodesk.Revit.DB.Color(255,250,250)
    Color18 = Autodesk.Revit.DB.Color(245,255,250)
    Color19 = Autodesk.Revit.DB.Color(253,245,230)
    Color20 = Autodesk.Revit.DB.Color(250,240,230)
    Color21 = Autodesk.Revit.DB.Color(47,79,79)
    Color22 = Autodesk.Revit.DB.Color(255,248,220)
    Color23 = Autodesk.Revit.DB.Color(222,184,135)
    Color24 = Autodesk.Revit.DB.Color(210,180,140)
    Color25 = Autodesk.Revit.DB.Color(210,105,30)
    Color26 = Autodesk.Revit.DB.Color(250,235,215)
    Color27 = Autodesk.Revit.DB.Color(240,248,255)
    Color28 = Autodesk.Revit.DB.Color(230,230,250)
    Color29 = Autodesk.Revit.DB.Color(240,255,255)
    Color30 = Autodesk.Revit.DB.Color(224,255,255)
    Color31 = Autodesk.Revit.DB.Color(245,245,245)
    Color32 = Autodesk.Revit.DB.Color(220,220,220)
    Color33 = Autodesk.Revit.DB.Color(211,211,211)
    Color34 = Autodesk.Revit.DB.Color(192,192,192)
    Color35 = Autodesk.Revit.DB.Color(169,169,169)
    Color36 = Autodesk.Revit.DB.Color(128,128,128)
    Color37 = Autodesk.Revit.DB.Color(105,105,105)
    Color38 = Autodesk.Revit.DB.Color(119,136,153)
    Color39 = Autodesk.Revit.DB.Color(112,128,144)
    Color40 = Autodesk.Revit.DB.Color(100,149,237)
    Color41 = Autodesk.Revit.DB.Color(70,130,180)
    Color42 = Autodesk.Revit.DB.Color(176,224,230)
    Color43 = Autodesk.Revit.DB.Color(95,158,160)
    Color44 = Autodesk.Revit.DB.Color(72,61,139)
    Color45 = Autodesk.Revit.DB.Color(106,90,205)
    Color46 = Autodesk.Revit.DB.Color(123,104,238)
    Color47 = Autodesk.Revit.DB.Color(148,0,211)
    Color48 = Autodesk.Revit.DB.Color(139,0,139)
    Color49 = Autodesk.Revit.DB.Color(148,0,150)
    Color50 = Autodesk.Revit.DB.Color(139,0,139)
    Color51 = Autodesk.Revit.DB.Color(176,224,230)
    Color52 = Autodesk.Revit.DB.Color(135,206,250)
    Color53 = Autodesk.Revit.DB.Color(135,206,235)
    Color54 = Autodesk.Revit.DB.Color(176,196,222)
    Color55 = Autodesk.Revit.DB.Color(65,105,225)
    Color56 = Autodesk.Revit.DB.Color(123,104,238)
    Color57 = Autodesk.Revit.DB.Color(230,230,250)
    Color58 = Autodesk.Revit.DB.Color(216,191,216)
    Color59 = Autodesk.Revit.DB.Color(238,130,238)
    Color60 = Autodesk.Revit.DB.Color(255,182,193)
    Color61 = Autodesk.Revit.DB.Color(255,250,250)
    Color62 = Autodesk.Revit.DB.Color(245,255,250)
    Color63 = Autodesk.Revit.DB.Color(253,245,230)
    Color64 = Autodesk.Revit.DB.Color(250,240,230)
    Color65 = Autodesk.Revit.DB.Color(47,79,79)
    Color66 = Autodesk.Revit.DB.Color(255,248,220)
    Color67 = Autodesk.Revit.DB.Color(222,184,135)
    Color68 = Autodesk.Revit.DB.Color(210,180,140)
    Color69 = Autodesk.Revit.DB.Color(210,105,30)
    Color70 = Autodesk.Revit.DB.Color(250,235,215)
    Color71 = Autodesk.Revit.DB.Color(240,248,255)
    Color72 = Autodesk.Revit.DB.Color(230,230,250)
    Color73 = Autodesk.Revit.DB.Color(240,255,255)
    Color74 = Autodesk.Revit.DB.Color(224,255,255)
    Color75 = Autodesk.Revit.DB.Color(245,245,245)
    Color76 = Autodesk.Revit.DB.Color(220,220,220)
    Color77 = Autodesk.Revit.DB.Color(211,211,211)
    Color78 = Autodesk.Revit.DB.Color(192,192,192)
    Color79 = Autodesk.Revit.DB.Color(169,169,169)
    Color80 = Autodesk.Revit.DB.Color(128,128,128)
    Color81 = Autodesk.Revit.DB.Color(105,105,105)
    Color82 = Autodesk.Revit.DB.Color(119,136,153)
    Color83 = Autodesk.Revit.DB.Color(112,128,144)
    Color84 = Autodesk.Revit.DB.Color(100,149,237)
    Color85 = Autodesk.Revit.DB.Color(70,130,180)
    Color86 = Autodesk.Revit.DB.Color(176,224,230)
    Color87 = Autodesk.Revit.DB.Color(95,158,160)
    Color88 = Autodesk.Revit.DB.Color(72,61,139)
    Color89 = Autodesk.Revit.DB.Color(106,90,205)
    Color90 = Autodesk.Revit.DB.Color(123,104,238)
    Color91 = Autodesk.Revit.DB.Color(148,0,211)
    Color92 = Autodesk.Revit.DB.Color(139,0,5)
    Color93 = Autodesk.Revit.DB.Color(148,0,211)
    Color94 = Autodesk.Revit.DB.Color(139,0,255)
    Color95 = Autodesk.Revit.DB.Color(176,224,230)
    Color96 = Autodesk.Revit.DB.Color(135,206,250)
    Color97 = Autodesk.Revit.DB.Color(135,206,235)
    Color98 = Autodesk.Revit.DB.Color(176,196,222)
    Color99 = Autodesk.Revit.DB.Color(65,105,225)
    Color100 = Autodesk.Revit.DB.Color(255,250,250)
    list_color = [
        Color0 ,Color5, Color10, Color15, Color20, Color25,
        Color1, Color6, Color11, Color16, Color21,
        Color2, Color7, Color12, Color17, Color22,
        Color3, Color8, Color13, Color18, Color23,
        Color4, Color9, Color14, Color19, Color24,
        Color26, Color31, Color36, Color41, Color46,
        Color27, Color32, Color37, Color42, Color47,
        Color28, Color33, Color38, Color43, Color48,
        Color29, Color34, Color39, Color44, Color49,
        Color30, Color35, Color40, Color45, Color50,
        Color51, Color56, Color61, Color66, Color71,
        Color52, Color57, Color62, Color67, Color72,
        Color53, Color58, Color63, Color68, Color73,
        Color54, Color59, Color64, Color69, Color74,
        Color55, Color60, Color65, Color70, Color75,
        Color76, Color81, Color86, Color91, Color96,
        Color77, Color82, Color87, Color92, Color97,
        Color78, Color83, Color88, Color93, Color98,
        Color79, Color84, Color89, Color94, Color99,
        Color80, Color85, Color90, Color95, Color100,
        Color0 ,Color5, Color10, Color15, Color20, Color25,
        Color1, Color6, Color11, Color16, Color21,
        Color2, Color7, Color12, Color17, Color22,
        Color3, Color8, Color13, Color18, Color23,
        Color4, Color9, Color14, Color19, Color24,
        Color26, Color31, Color36, Color41, Color46,
        Color27, Color32, Color37, Color42, Color47,
        Color28, Color33, Color38, Color43, Color48,
        Color29, Color34, Color39, Color44, Color49,
        Color30, Color35, Color40, Color45, Color50,
        Color51, Color56, Color61, Color66, Color71,
        Color52, Color57, Color62, Color67, Color72,
        Color53, Color58, Color63, Color68, Color73,
        Color54, Color59, Color64, Color69, Color74,
        Color55, Color60, Color65, Color70, Color75,
        Color76, Color81, Color86, Color91, Color96,
        Color77, Color82, Color87, Color92, Color97,
        Color78, Color83, Color88, Color93, Color98,
        Color79, Color84, Color89, Color94, Color99,
        Color80, Color85, Color90, Color95, Color100,
        Color0 ,Color5, Color10, Color15, Color20, Color25,
        Color1, Color6, Color11, Color16, Color21,
        Color2, Color7, Color12, Color17, Color22,
        Color3, Color8, Color13, Color18, Color23,
        Color4, Color9, Color14, Color19, Color24,
        Color26, Color31, Color36, Color41, Color46,
        Color27, Color32, Color37, Color42, Color47,
        Color28, Color33, Color38, Color43, Color48,
        Color29, Color34, Color39, Color44, Color49,
        Color30, Color35, Color40, Color45, Color50,
        Color51, Color56, Color61, Color66, Color71,
        Color52, Color57, Color62, Color67, Color72,
        Color53, Color58, Color63, Color68, Color73,
        Color54, Color59, Color64, Color69, Color74,
        Color55, Color60, Color65, Color70, Color75,
        Color76, Color81, Color86, Color91, Color96,
        Color77, Color82, Color87, Color92, Color97,
        Color78, Color83, Color88, Color93, Color98,
        Color79, Color84, Color89, Color94, Color99,
        Color80, Color85, Color90, Color95, Color100,
        Color0 ,Color5, Color10, Color15, Color20, Color25,
        Color1, Color6, Color11, Color16, Color21,
        Color2, Color7, Color12, Color17, Color22,
        Color3, Color8, Color13, Color18, Color23,
        Color4, Color9, Color14, Color19, Color24,
        Color26, Color31, Color36, Color41, Color46,
        Color27, Color32, Color37, Color42, Color47,
        Color28, Color33, Color38, Color43, Color48,
        Color29, Color34, Color39, Color44, Color49,
        Color30, Color35, Color40, Color45, Color50,
        Color51, Color56, Color61, Color66, Color71,
        Color52, Color57, Color62, Color67, Color72,
        Color53, Color58, Color63, Color68, Color73,
        Color54, Color59, Color64, Color69, Color74,
        Color55, Color60, Color65, Color70, Color75,
        Color76, Color81, Color86, Color91, Color96,
        Color77, Color82, Color87, Color92, Color97,
        Color78, Color83, Color88, Color93, Color98,
        Color79, Color84, Color89, Color94, Color99,
        Color80, Color85, Color90, Color95, Color100,
        Color0 ,Color5, Color10, Color15, Color20, Color25,
        Color1, Color6, Color11, Color16, Color21,
        Color2, Color7, Color12, Color17, Color22,
        Color3, Color8, Color13, Color18, Color23,
        Color4, Color9, Color14, Color19, Color24,
        Color26, Color31, Color36, Color41, Color46,
        Color27, Color32, Color37, Color42, Color47,
        Color28, Color33, Color38, Color43, Color48,
        Color29, Color34, Color39, Color44, Color49,
        Color30, Color35, Color40, Color45, Color50,
        Color51, Color56, Color61, Color66, Color71,
        Color52, Color57, Color62, Color67, Color72,
        Color53, Color58, Color63, Color68, Color73,
        Color54, Color59, Color64, Color69, Color74,
        Color55, Color60, Color65, Color70, Color75,
        Color76, Color81, Color86, Color91, Color96,
        Color77, Color82, Color87, Color92, Color97,
        Color78, Color83, Color88, Color93, Color98,
        Color79, Color84, Color89, Color94, Color99,
        Color80, Color85, Color90, Color95, Color100,
        Color0 ,Color5, Color10, Color15, Color20, Color25,
        Color1, Color6, Color11, Color16, Color21,
        Color2, Color7, Color12, Color17, Color22,
        Color3, Color8, Color13, Color18, Color23,
        Color4, Color9, Color14, Color19, Color24,
        Color26, Color31, Color36, Color41, Color46,
        Color27, Color32, Color37, Color42, Color47,
        Color28, Color33, Color38, Color43, Color48,
        Color29, Color34, Color39, Color44, Color49,
        Color30, Color35, Color40, Color45, Color50,
        Color51, Color56, Color61, Color66, Color71,
        Color52, Color57, Color62, Color67, Color72,
        Color53, Color58, Color63, Color68, Color73,
        Color54, Color59, Color64, Color69, Color74,
        Color55, Color60, Color65, Color70, Color75,
        Color76, Color81, Color86, Color91, Color96,
        Color77, Color82, Color87, Color92, Color97,
        Color78, Color83, Color88, Color93, Color98,
        Color79, Color84, Color89, Color94, Color99,
        Color80, Color85, Color90, Color95, Color100,
        Color0 ,Color5, Color10, Color15, Color20, Color25,
        Color1, Color6, Color11, Color16, Color21,
        Color2, Color7, Color12, Color17, Color22,
        Color3, Color8, Color13, Color18, Color23,
        Color4, Color9, Color14, Color19, Color24,
        Color26, Color31, Color36, Color41, Color46,
        Color27, Color32, Color37, Color42, Color47,
        Color28, Color33, Color38, Color43, Color48,
        Color29, Color34, Color39, Color44, Color49,
        Color30, Color35, Color40, Color45, Color50,
        Color51, Color56, Color61, Color66, Color71,
        Color52, Color57, Color62, Color67, Color72,
        Color53, Color58, Color63, Color68, Color73,
        Color54, Color59, Color64, Color69, Color74,
        Color55, Color60, Color65, Color70, Color75,
        Color76, Color81, Color86, Color91, Color96,
        Color77, Color82, Color87, Color92, Color97,
        Color78, Color83, Color88, Color93, Color98,
        Color79, Color84, Color89, Color94, Color99,
        Color80, Color85, Color90, Color95, Color100,
        Color0 ,Color5, Color10, Color15, Color20, Color25,
        Color1, Color6, Color11, Color16, Color21,
        Color2, Color7, Color12, Color17, Color22,
        Color3, Color8, Color13, Color18, Color23,
        Color4, Color9, Color14, Color19, Color24,
        Color26, Color31, Color36, Color41, Color46,
        Color27, Color32, Color37, Color42, Color47,
        Color28, Color33, Color38, Color43, Color48,
        Color29, Color34, Color39, Color44, Color49,
        Color30, Color35, Color40, Color45, Color50,
        Color51, Color56, Color61, Color66, Color71,
        Color52, Color57, Color62, Color67, Color72,
        Color53, Color58, Color63, Color68, Color73,
        Color54, Color59, Color64, Color69, Color74,
        Color55, Color60, Color65, Color70, Color75,
        Color76, Color81, Color86, Color91, Color96,
        Color77, Color82, Color87, Color92, Color97,
        Color78, Color83, Color88, Color93, Color98,
        Color79, Color84, Color89, Color94, Color99,
        Color80, Color85, Color90, Color95, Color100
    ]
    # random.shuffle(list_color)

    def all_type():
        all_OST_type = FilteredElementCollector(doc).OfClass(WallType).OfCategory(BuiltInCategory.OST_Walls)
        return all_OST_type
    def get_filter_elements():
        filter_elements = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()
        return filter_elements
    list_wall = get_filter_elements()
    name = []
    for i in list_wall:
        name.append(Autodesk.Revit.DB.Element.Name.GetValue(i))
        name.sort()

    class MyForm(Form):
        def __init__(self):
            self.Text = "ARC"
            self.ShowIcon = False  #An icon nho
            self.Size = Size(520, 500)
            self.checkedListBox = CheckedListBox()
            items = Array[object](list(name))
            self.checkedListBox.Items.AddRange(items)
            self.checkedListBox.Size = Size(400, 300)
            self.checkedListBox.Location = Drawing.Point(10, 50)
            self.checkedListBox.CheckOnClick = True
            self.label1 = Label()
            self.label1.Text = "Prefix"
            self.label1.Location = Drawing.Point(10, 5)

            self.textBox_1 = TextBox()
            self.textBox_1.Location = Drawing.Point(10, 20)
            self.textBox_1.Size = Size(250, 20)
            self.textBox_1.Text = "wallA_type name_e_"

            self.label2 = Label()
            self.label2.Text = "Suffix"
            self.label2.Location = Drawing.Point(360, 5)

            self.typeNameLabel = Label()
            self.typeNameLabel.Text = "type name"
            self.typeNameLabel.Location = Drawing.Point(280, 22)
            self.typeNameLabel.AutoSize = True
            self.typeNameLabel.ForeColor = Color.Gray
            self.typeNameLabel.Font = Font(self.typeNameLabel.Font, FontStyle.Bold)



            self.typeNamePanel = Panel()
            self.typeNamePanel.Location = Drawing.Point(270, 20)
            self.typeNamePanel.Size = Size(80, 20)
            self.typeNamePanel.BackColor = Color.Transparent
            self.typeNamePanel.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle


            self.textBox_2 = TextBox()
            self.textBox_2.Location = Drawing.Point(360, 20)
            self.textBox_2.Size = Size(50, 20)
            self.textBox_2.Text = "_kw"


            self.selectAllButton = Button()
            self.selectAllButton.Text = "Select All"
            self.selectAllButton.Location = Drawing.Point(420, 50)
            self.selectAllButton.Click += self.on_select_all_button_click

            self.nonebutton = Button()
            self.nonebutton.Text = "None"
            self.nonebutton.Location = Drawing.Point(420, 80)
            self.nonebutton.Click += self.on_none_click

            self.signatureLabel = Label()
            self.signatureLabel.Text = "nguyenthanhson1712@gmail.com"
            self.signatureLabel.Size = Size(485, 20)
            self.signatureLabel.Location = Drawing.Point(320, 440)



            # Ham nay de chon tat ca type tuong khi hien windowform
            default_checked = Array[object](list(name))
            for item in default_checked:
                index = self.checkedListBox.FindStringExact(item)
                if index != -1:
                    self.checkedListBox.SetItemChecked(index, False)

            # self.checkedListBox.ItemCheck += self.on_item_check
            self.printButton = Button()
            self.printButton.Text = "Apply filter"
            self.printButton.Location = Drawing.Point(420, 400)
            self.printButton.Click += self.on_print_button_click
            # Add the CheckedListBox to the Form
            self.Controls.Add(self.checkedListBox)
            self.Controls.Add(self.printButton)
            # self.Controls.Add(self.textBox_1)
            # self.Controls.Add(self.textBox_2)
            self.Controls.Add(self.selectAllButton)
            self.Controls.Add(self.nonebutton)
            self.Controls.Add(self.signatureLabel)
            # self.Controls.Add(self.label1)
            # self.Controls.Add(self.label2)
            # self.Controls.Add(self.typeNameLabel)
            # self.Controls.Add(self.typeNamePanel)

        def on_select_all_button_click(self, sender, e):
            for i in range(self.checkedListBox.Items.Count):
                self.checkedListBox.SetItemChecked(i, True)

        def on_none_click(self, sender, e):
            for i in range(self.checkedListBox.Items.Count):
                self.checkedListBox.SetItemChecked(i, False)

        def on_item_check(self, sender, e):
            checked_items = [self.checkedListBox.GetItemText(item) for item in self.checkedListBox.CheckedItems]
            print("Checked items:", checked_items)
        def on_checkedListBox_key_down(self, sender, e):
            if e.Control:
                e.Handled = True

        def on_print_button_click(self, sender, e):
            checked_items = [self.checkedListBox.GetItemText(item) for item in self.checkedListBox.CheckedItems]
            list_tem = []  
            GetFillPattern = Autodesk.Revit.DB.FillPatternElement.GetFillPatternElementByName(doc,FillPatternTarget.Drafting,"<Solid fill>")
            if str(GetFillPattern) == "None":
                GetFillPattern = Autodesk.Revit.DB.FillPatternElement.GetFillPatternElementByName(doc,FillPatternTarget.Drafting,"<塗り潰し>")
            for i in list_wall:
                list_tem.append(i)
            for i_name in checked_items:
                override_settings = OverrideGraphicSettings()
                # random_colors = random.sample(list_color, k=25)
                index_i = checked_items.index(i_name)
                # random_color = random.choice(list_color)
                random_color = list_color[index_i]
                override_settings.SetSurfaceForegroundPatternColor(random_color)
                override_settings.SetSurfaceForegroundPatternId(GetFillPattern.Id)
                override_settings.SetCutForegroundPatternColor(random_color)
                override_settings.SetCutForegroundPatternId(GetFillPattern.Id)
                for wall in list_tem:
                    wall_name = Autodesk.Revit.DB.Element.Name.GetValue(wall)
                    if i_name == wall_name:
                        try:
                            view_template = doc.GetElement(view.ViewTemplateId)
                            view_template_name = Autodesk.Revit.DB.Element.Name.GetValue(view_template)
                            if view_template:
                            # if MessageBox.Show("Are you sure to apply these filter to view template") + str(view_template_name):
                                view_template.AddFilter(wall.Id)
                                view_template.SetFilterOverrides(wall.Id, override_settings)
                                index = list_tem.index(wall)
                                list_tem.pop(index)
                                self.Close()
                            # else:
                                # sys.exit()
                                # self.Close()

                            else:
                                view.AddFilter(wall.Id)
                                view.SetFilterOverrides(wall.Id, override_settings)
                                index = list_tem.index(wall)
                                list_tem.pop(index)
                                self.Close()  
                        except:
                            pass
            
    form = MyForm()

    # Run the application
    form.ShowDialog()
    t.Commit()  


