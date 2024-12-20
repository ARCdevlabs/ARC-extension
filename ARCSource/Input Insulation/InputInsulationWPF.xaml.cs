﻿using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Input_Insulation;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
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
        private Utility _utility;
        
       

        public MainWindow(Document doc, List<Element> listElement)
        {
            InitializeComponent();       
            _doc = doc;
            _listElement = listElement;
            InitializeControls();
            Utility _utility = new Utility();
        }

        private void TbThickness_PreviewTextInput(object sender, TextCompositionEventArgs e)
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
            
            FamilySymbol m_FamilySymbol = null;

            Utility.TypeOfInsulation _typeOfInsulation = (Utility.TypeOfInsulation)Cbb_SelectTypeOfInsulation.SelectedValue;

            string textBoxValue = TbThickness.Text;

            double covertToDouble = double.Parse(textBoxValue) / 304.8;


            this.Close();
            if (RadioBtn_BeamInsolutation.IsChecked==true)
            {
                
                Element beamType = _doc.GetElement(new ElementId(13042529)); //Cần điều chỉnh lại beamTypeSymbol dựa vào form WPF

                FamilySymbol beamTypeSymbol = beamType as FamilySymbol;

                _utility.InputBeamInsulation(_doc, _listElement, beamTypeSymbol, covertToDouble);
            }
            else if(Radiobtn_ColumnInsulation.IsChecked==true) 
            {
                Utility.ColumnInsulation(_doc, _listElement, _typeOfInsulation, textBoxValue);
            } 
                

        }
        private void InitializeControls()
        {
            
            Cbb_SelectTypeOfInsulation.Items.Add(Utility.TypeOfInsulation.けいカル);
            Cbb_SelectTypeOfInsulation.Items.Add(Utility.TypeOfInsulation.巻き付け);
            Cbb_SelectTypeOfInsulation.SelectedIndex = 0;

            if (_listElement.First().Category.Id == new ElementId(BuiltInCategory.OST_StructuralColumns))
            {
                Radiobtn_ColumnInsulation.IsChecked = true;
            }
            else if (_listElement.First().Category.Id== new ElementId(BuiltInCategory.OST_StructuralFraming))
            {
               double angle= _listElement.First().get_Parameter(BuiltInParameter.STRUCTURAL_BEND_DIR_ANGLE).AsDouble();
                if (angle == 0) { RadioBtn_BeamInsolutation.IsChecked = true; }
                else {  RadioBtn_HorizontalBeamInsulation.IsChecked = true; }
            }           
        }

        
    }
}
