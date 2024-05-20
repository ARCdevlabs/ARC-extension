__doc__ = 'NguyenThanhSon'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
from re import I
import string
import importlib

ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
try:
    if module.AutodeskData():
        import Autodesk
        from Autodesk.Revit.DB import Transaction, Wall,Level, BuiltInCategory, FilteredElementCollector, WallType
        from Autodesk.Revit.UI.Selection import ObjectType
        import clr
        clr.AddReference("System.Windows.Forms")
        from System.Windows.Forms import Form, Label, TextBox, Button, ComboBox, ComboBoxStyle, MessageBox, FormStartPosition
        from System.Drawing import Point, Size, Font, FontStyle, Color
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        MessageBox.Show("Please select the DWG importinstance, Click OK to continue", "Message")
        pick = uidoc.Selection.PickObject(ObjectType.Element)
        element_id = pick.ElementId
        covert_reference_to_element = doc.GetElement(element_id)
        class InputForm(Form):
            def __init__(self):
                self.Text = "Wall from DWG"
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
                self.textBox.Text = "wallA"  # Set default value

                self.comboBox_level = ComboBox()
                self.comboBox_level.Location = Point(10, 90)
                self.comboBox_level.Size = Size(200, 20)
                self.comboBox_level.DropDownStyle = ComboBoxStyle.DropDownList
                self.PopulateLevels()

                self.comboBox_wall_type = ComboBox()
                self.comboBox_wall_type.Location = Point(10, 130)
                self.comboBox_wall_type.Size = Size(200, 20)
                self.comboBox_wall_type.DropDownStyle = ComboBoxStyle.DropDownList
                self.PopulateWallTypes()
                
                self.button_create_wall = Button()
                self.button_create_wall.Text = "Create wall"
                self.button_create_wall.Location = Point(200, 270)
                self.button_create_wall.Click += self.button_Click


                # Them cac nut vao trong form, sap theo thu tu cho de quan ly
                self.Controls.Add(self.label_picked)
                self.Controls.Add(self.label_layer)
                self.Controls.Add(self.textBox)
                self.Controls.Add(self.button_create_wall)
                self.Controls.Add(self.comboBox_level)
                self.Controls.Add(self.comboBox_wall_type)

            def PopulateLevels(self):
                levels = FilteredElementCollector(doc).OfClass(Level)
                level_names = []
                for level in levels:
                    level_names.append(level.Name)
                level_names.sort()
                for level_name in level_names:
                    self.comboBox_level.Items.Add(level_name)
                if levels:
                    self.comboBox_level.SelectedIndex = 0
                self.comboBox_level.SelectedItem

            def PopulateWallTypes(self):
                wall_type_names = []
                wall_types = FilteredElementCollector(doc).OfClass(WallType)
                for wall_type in wall_types:
                    wall_type_names.append(Autodesk.Revit.DB.Element.Name.GetValue(wall_type))
                wall_type_names.sort()
                for wall_type_name in wall_type_names:
                    self.comboBox_wall_type.Items.Add(wall_type_name)
                    self.comboBox_wall_type.Items.Add(wall_type_name)
                if wall_types:
                    self.comboBox_wall_type.SelectedIndex = 0
                # selected_wall_type = self.comboBox_wall_type.SelectedItem
                # self.wall_type = next((x for x in FilteredElementCollector(doc).OfClass(WallType).ToElements() if (Autodesk.Revit.DB.Element.Name.GetValue(x)) == selected_wall_type), None)

            def button_Click(self, sender, e):
                t = Transaction (doc, "Wall from DWG")
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
                            # det_line = doc.Create.NewDetailCurve(acview, arc) #Neu khong ve detail line thi thoi khong dung
                def create_wall(doc, curve, wall_type, level):
                    wall = Wall.Create(doc, curve, level.Id, False)
                    wall.WallType = wall_type
                    # param = wall.get_Parameter(Autodesk.Revit.DB.BuiltInParameter.WALL_BASE_CONSTRAINT)
                    # if param is not None and param.HasValue:
                    #     param.Set(level)
                    return wall
                selected_wall_type = self.comboBox_wall_type.SelectedItem
                all_wall_type = FilteredElementCollector(doc).OfClass(WallType).ToElements()
                selected_level = self.comboBox_level.SelectedItem
                levels_2 = FilteredElementCollector(doc).OfClass(Level)
                for wall_type_2 in all_wall_type:
                    if selected_wall_type == Autodesk.Revit.DB.Element.Name.GetValue(wall_type_2):
                        for level_2 in levels_2:
                            if level_2.Name == selected_level:            
                                for curve in list_curve:
                                    create_wall(doc, curve, wall_type_2, level_2)
                self.Close() 
                t.Commit()
        form = InputForm()
        form.ShowDialog()     
except:
    pass
