using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Input_Insulation;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Input;

namespace Input_Insulation
{
    public partial class MainWindow : Window
    {
        private Document _doc;
        private List<Element> _listElement;
        private BeamInsulation_Form _beamInsulationForm;

        public MainWindow(Document doc, List<Element> listElement)
        {
            InitializeComponent();
            _doc = doc;
            _listElement = listElement;
            _beamInsulationForm = new BeamInsulation_Form(); // Khởi tạo BeamInsulation_Form
        }

        private void NumberTextBox_PreviewTextInput(object sender, TextCompositionEventArgs e)
        {
            // Regular expression for numbers with optional decimal separator (dot or comma)
            Regex regex = new Regex(@"^[0-9]*(?:[.]?[0-9]*)$");

            // Get the proposed new text with the input character included
            var textBox = sender as System.Windows.Controls.TextBox;
            string proposedText = textBox.Text.Insert(textBox.SelectionStart, e.Text);

            // Check if the proposed text matches the regex pattern
            e.Handled = !regex.IsMatch(proposedText);
        }

        private void OnCreateInsulationButton_Click(object sender, RoutedEventArgs e)
        {
            this.Close();

            string textBoxValue = TbThickness.Text;

            double covertToDouble = double.Parse(textBoxValue) / 304.8;

            Element beamType = _doc.GetElement(new ElementId(13042529)); //Cần điều chỉnh lại beamTypeSymbol dựa vào form WPF

            FamilySymbol beamTypeSymbol = beamType as FamilySymbol;

            _beamInsulationForm.ChayChuongTrinh(_doc, _listElement, beamTypeSymbol, covertToDouble);

        }
    }

}
