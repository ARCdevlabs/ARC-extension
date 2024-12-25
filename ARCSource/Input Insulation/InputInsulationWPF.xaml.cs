using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Input_Insulation;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Data.Common;
using System.Linq;
using System.Runtime.Remoting.Lifetime;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Input;
using System.Windows.Media;
using static Autodesk.Revit.DB.SpecTypeId;
using static Input_Insulation.Utility;


namespace Input_Insulation
{
    public class FamilyTypeInfo
    {
        public string FamilyName { get; set; }
        public string TypeName { get; set; }
        public ElementId TypeId { get; set; } // Để lưu Id nếu cần sử dụng sau
    }

    public partial class MainWindow : Window
    {
        private Document _doc;

        private UIDocument _uidoc;

        private List<Element> _listElement;

        private Utility _utility;

        private List<FamilyTypeInfo> familyTypeInfos;
        public static Element GlobalElement { get; set; }
        public static bool shapeH { get; set; }
        public ObservableCollection<string> TypeOfInsulations { get; set; }

        TypeOfInsulation insulationType;
        public MainWindow(UIDocument uidoc, Document doc, List<Element> listElement)
        {
            InitializeComponent();
            _doc = doc;
            _uidoc = uidoc;
            _listElement = listElement;
            _utility = new Utility();
            LoadFamilyTypes();
        }

        private void Radiobtn_ColumnInsulation_Checked(object sender, RoutedEventArgs e)
        {
            ButtonInsulationColumn.Content = "Pick the sample";
        }
        private void Radiobtn_BeamInsulation_Checked(object sender, RoutedEventArgs e)
        {
            ButtonInsulationColumn.Content = "Create Beam Insulation";
        }
        private void RadioBtn_HorizontalBeamInsulation_Checked(object sender, RoutedEventArgs e)
        {
            ButtonInsulationColumn.Content = "Create Horizontal Beam Insulation";
        }

        private void LoadFamilyTypes()
        {
            // Filter for FamilySymbols (Types)
            var collector = new FilteredElementCollector(_doc)
                .OfClass(typeof(FamilySymbol))
                .Cast<FamilySymbol>()
                .Where(fs => fs.FamilyName.StartsWith("gIns", System.StringComparison.OrdinalIgnoreCase))
                .ToList();

            familyTypeInfos = collector.Select(fs => new FamilyTypeInfo
            {
                FamilyName = fs.FamilyName,
                TypeName = fs.Name,
                TypeId = fs.Id,
            }).ToList();

            TypeOfInsulations = new ObservableCollection<string> { "Default" };

            foreach (var familyTypeInfo in familyTypeInfos)
            {

                if (familyTypeInfo.FamilyName != null)
                {
                    string DisplayName = familyTypeInfo.FamilyName + ":" + familyTypeInfo.TypeName;

                    TypeOfInsulations.Add(DisplayName);
                }
            }
            Cbb_SelectTypeOfInsulation.Items.Clear();

            Cbb_SelectTypeOfInsulation.ItemsSource = TypeOfInsulations;
        }

        private void TbThickness_PreviewTextInput(object sender, TextCompositionEventArgs e)
        {
            Regex regex = new Regex(@"^[0-9]*(?:[.]?[0-9]*)$");


            var textBox = sender as System.Windows.Controls.TextBox;
            string proposedText = textBox.Text.Insert(textBox.SelectionStart, e.Text);

            e.Handled = !regex.IsMatch(proposedText);
        }


        private void OnCreateInsulationButton_Click(object sender, RoutedEventArgs e)
        {
            string selectedValue = Cbb_SelectTypeOfInsulation.SelectedItem as string;
            if (selectedValue != null)
            {
                if (selectedValue == "Default" & Radiobtn_ColumnInsulation.IsChecked == false)
                {
                    foreach (var familyTypeInfo in familyTypeInfos)
                    {
                        string DisplayName = familyTypeInfo.FamilyName + ":" + familyTypeInfo.TypeName;

                        if (DisplayName.ToString() == "gIns_Frame-ver4.0:Default")
                        {
                            try
                            {
                                Element selectedType = _doc.GetElement(familyTypeInfo.TypeId);

                                GlobalElement = selectedType;
                            }
                            catch
                            {
                                throw;
                            }
                        }
                    }
                }
                else if (selectedValue == "Default" & Radiobtn_ColumnInsulation.IsChecked == true)
                {
                    foreach (var familyTypeInfo in familyTypeInfos)
                    {
                        string DisplayName = familyTypeInfo.FamilyName + ":" + familyTypeInfo.TypeName;

                        if (DisplayName.ToString() == "gIns_Column-ver4.0:Default")
                        {
                            try
                            {
                                Element selectedType = _doc.GetElement(familyTypeInfo.TypeId);

                                GlobalElement = selectedType;
                            }
                            catch
                            {
                                return;
                            }
                        }
                    }
                }

                else if (selectedValue != "Default")
                {
                    foreach (var familyTypeInfo in familyTypeInfos)
                    {
                        string DisplayName = familyTypeInfo.FamilyName + ":" + familyTypeInfo.TypeName;

                        if (DisplayName.ToString() == selectedValue)
                        {
                            Element selectedType = _doc.GetElement(familyTypeInfo.TypeId);

                            GlobalElement = selectedType;
                        }

                    }
                }
                if (GlobalElement != null)
                {
                    string textBoxValue = TbThickness.Text;

                    double covertToDouble = double.Parse(textBoxValue) / 304.8;
                    if (ShapeType1.IsChecked == true)
                    {
                        shapeH = true;
                    }
                    else
                    {
                        shapeH = false;
                    }
                    if (RadioBtn_BeamInsolutation.IsChecked == true)
                    {

                        //Element beamType = _doc.GetElement(new ElementId(13042529)); //Cần điều chỉnh lại beamTypeSymbol dựa vào form WPF

                        Element beamType = GlobalElement;

                        //TaskDialog.Show("Beam Information", GlobalElement.ToString());

                        FamilySymbol beamTypeSymbol = beamType as FamilySymbol;

                        _utility.InputBeamInsulation(_doc, _listElement, beamTypeSymbol, shapeH, covertToDouble);

                    }
                    else if (RadioBtn_HorizontalBeamInsulation.IsChecked == true)
                    {
                        Element beamType = GlobalElement;

                        FamilySymbol beamTypeSymbol = beamType as FamilySymbol;

                        _utility.InputBeamHorizontalInsulation(_doc, _listElement, beamTypeSymbol, shapeH, covertToDouble);

                    }

                    else if (Radiobtn_ColumnInsulation.IsChecked == true)
                    {

                        //Utility.ColumnInsulation(_doc, _listElement, shapeH, textBoxValue.ToString());
                        if (shapeH == true)
                        {
                            insulationType = TypeOfInsulation.巻き付け;
                        }
                        else
                        {
                            insulationType = TypeOfInsulation.けいカル;
                        }
                       
                        Element columnType = GlobalElement;

                        FamilySymbol columnTypeSymbol = columnType as FamilySymbol;

                        //TaskDialog.Show("Beam Information", columnTypeSymbol.Id.ToString());
                        this.Hide();
                        ARCLibrary lib = new ARCLibrary();
                        try
                        {
                            Element sourceElement = lib.PickElement(_uidoc, _doc);
                            ElementId sourceElementId = sourceElement.Id;                      
                            Utility.ColumnInsulation(_doc, _listElement, sourceElementId, columnTypeSymbol, insulationType, covertToDouble.ToString());
                        }
                        catch (Exception ex)
                        {
                            TaskDialog.Show("Error", "Please input the sample Insulation for column at level, then pick them");
                        }
                    }
                }
                this.Close();
            }

        }
    }
}