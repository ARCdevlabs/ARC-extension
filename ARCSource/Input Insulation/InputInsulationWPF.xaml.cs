using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;




namespace Input_Insulation
{
    public partial class MainWindow : Window
    {
        
        public MainWindow()
        {
            InitializeComponent();
            Cbb_SelectTypeInsulation.Items.Add(Utility.TypeOfInsulation.けいカル);
            Cbb_SelectTypeInsulation.Items.Add(Utility.TypeOfInsulation.巻き付け);
            Cbb_SelectTypeInsulation.SelectedIndex = 0;
        }

        private void ClickButtonInsulationColumn(object sender, RoutedEventArgs e)
        {

        }
    }

}
