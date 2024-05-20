__doc__ = 'NguyenThanhSon'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
from re import I
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import Transaction, Wall,Level, BuiltInCategory, FilteredElementCollector, WallType, Line, XYZ, SetComparisonResult, IntersectionResultArray, Curve, FamilySymbol
from Autodesk.Revit.UI.Selection import ObjectType
import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Form, Label, TextBox, Button, ComboBox, ComboBoxStyle, MessageBox, FormStartPosition
from System.Drawing import Point, Size, Font, FontStyle, Color
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
if module.AutodeskData():
    def active_symbol(element):
        try:
            if element.IsActive == False:
                element.Activate()
        except:
            pass
        return 
    def get_selected_elements():
        selection = uidoc.Selection
        selection_ids = selection.GetElementIds()
        elements = []
        for element_id in selection_ids:
            elements.append(doc.GetElement(element_id))
        return elements
    selected_ele = get_selected_elements()
    def get_intersection(line1, line2):
        results = clr.Reference[IntersectionResultArray]()
        result = line1.Intersect(line2, results)
        return results

    def input_door(point, type, host):
        structural_type = Autodesk.Revit.DB.Structure.StructuralType.NonStructural
        level = doc.GetElement(host.LevelId)
        door = doc.Create.NewFamilyInstance(point,type,host,level,structural_type)
        return door
    all_door_type = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_Doors)
    MessageBox.Show("Please select the DWG importinstance, Click OK to continue", "Message")
    pick = uidoc.Selection.PickObject(ObjectType.Element)
    element_id = pick.ElementId
    covert_reference_to_element = doc.GetElement(element_id)

    class InputForm(Form):
        def __init__(self):
            self.Text = "Door from DWG"
            self.InitializeComponents()
            self.Size = Size (300,350)
            self.StartPosition = FormStartPosition.CenterScreen

        def InitializeComponents(self):
            self.label_picked = Label() #In ra gia tri file DWG da chon
            self.label_picked.Text = "Selected DWG:" + str(covert_reference_to_element.Category.Name)
            self.label_picked.Size = Size(500, 20)
            self.label_picked.Location = Point(10, 10)
            self.label_picked.Font = Font(self.label_picked.Font, FontStyle.Bold)  # Set bold font
            self.label_picked.ForeColor = Color.Red

            self.label_layer = Label()
            self.label_layer.Text = "Enter the layer name"
            self.label_layer.Size = Size(500, 20)
            self.label_layer.Location = Point(10, 30)


            self.textBox = TextBox()
            self.textBox.Location = Point(10, 50)
            self.textBox.Size = Size(200, 20)
            self.textBox.Text = "Door"  # Set default value


            self.comboBox_wall_type = ComboBox()
            self.comboBox_wall_type.Location = Point(10, 130)
            self.comboBox_wall_type.Size = Size(200, 20)
            self.comboBox_wall_type.DropDownStyle = ComboBoxStyle.DropDownList
            self.PopulateWallTypes()
            
            self.button_create_wall = Button()
            self.button_create_wall.Text = "Input Door"
            self.button_create_wall.Location = Point(200, 270)
            self.button_create_wall.Click += self.button_Click


            # Them cac nut vao trong form, sap theo thu tu cho de quan ly
            self.Controls.Add(self.label_picked)
            self.Controls.Add(self.label_layer)
            self.Controls.Add(self.textBox)
            self.Controls.Add(self.button_create_wall)
            # self.Controls.Add(self.comboBox_level)
            self.Controls.Add(self.comboBox_wall_type)


        def PopulateWallTypes(self):
            framing_type_names = []

            framing_symbols = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_Doors)
            for symbol in framing_symbols:
                framing_type_names.append(Autodesk.Revit.DB.Element.Name.GetValue(symbol))
            framing_type_names.sort()
            for framing_type_name in framing_type_names:
                self.comboBox_wall_type.Items.Add(framing_type_name)
            if framing_symbols:
                self.comboBox_wall_type.SelectedIndex = 0



        def button_Click(self, sender, e):
            t = Transaction (doc, "Door from DWG")
            t.Start()
            global LAYER_NAME
            LAYER_NAME = self.textBox.Text
            acview= module.Active_view(doc)
            dwg = covert_reference_to_element
        # Nhap layer cua line trong dwg
        # Khai bao option cua "get_Geometry"
            geo_opt = Autodesk.Revit.DB.Options()
            geo_opt.ComputeReferences = True
            geo_opt.IncludeNonVisibleObjects = True
            geo_opt.View = acview
            list_curve=[]
        # get_Geometry cua tat ca line trong file dwg
            geometry = dwg.get_Geometry(geo_opt)
            for geo_inst in geometry:
                geo_elem = geo_inst.GetInstanceGeometry()
                for polyline in geo_elem:
                    element = doc.GetElement(polyline.GraphicsStyleId)
                    if not element:
                        continue

        # Kiem tra layer cua line trong file dwg thong qua "GraphicsStyleCategory.Name"
        # Dung de ve cac doi tuong "polyline"
                    is_target_layer = element.GraphicsStyleCategory.Name == LAYER_NAME
                    is_polyline = polyline.GetType().Name == "PolyLine"
                    if is_polyline and is_target_layer:

                        begin = None
                        for pts in polyline.GetCoordinates():
                            if not begin:
                                begin = pts
                                continue
                            end = pts
                            line = Autodesk.Revit.DB.Line.CreateBound(begin, end)
                            list_curve.append(line)
                            # det_line = doc.Create.NewDetailCurve(acview, line)
                            begin = pts

        # Dung de ve cac doi tuong "line"
                    is_line = polyline.GetType().Name == "Line"
                    if is_line and is_target_layer:
                            straight_line = polyline
                            list_curve.append(straight_line)
                            # det_line = doc.Create.NewDetailCurve(acview, straight_line)
        # Dung de ve cac doi tuong "arc"
                    is_arc = polyline.GetType().Name == "Arc"
                    if is_arc and is_target_layer:
                        arc = polyline
                        list_curve.append(arc)
            list_point =[]
            selected_door_type = self.comboBox_wall_type.SelectedItem
            all_door_type = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_Doors)
            for door_type in all_door_type:
                if (Autodesk.Revit.DB.Element.Name.GetValue(door_type)) == selected_door_type:
                    if door_type.IsActive == False:
                        door_type.Activate()
                        
                    for curve in list_curve:
                        start_point_in_dwg_curve = curve.GetEndPoint(0)
                        end_point_in_dwg_curve = curve.GetEndPoint(1)
                        for ele in selected_ele:
                            location_curve = ele.Location.Curve
                            point_in_wall_curve = location_curve.GetEndPoint(0).Z
                            new_start_point = XYZ(start_point_in_dwg_curve.X, start_point_in_dwg_curve.Y, point_in_wall_curve)
                            new_end_point = XYZ(end_point_in_dwg_curve.X, end_point_in_dwg_curve.Y, point_in_wall_curve)
                            new_curve_of_dwg = Line.CreateBound(new_start_point,new_end_point)
                            intersect_point = get_intersection(new_curve_of_dwg, location_curve)
                            try:
                                point_inter = intersect_point.Item[0].XYZPoint
                                list_point.append (point_inter)
                                door = input_door(point_inter, door_type, ele)
                            except:
                                # import traceback
                                # print(traceback.format_exc())
                                pass
            self.Close() 
            t.Commit()
    form = InputForm()
    form.ShowDialog()
