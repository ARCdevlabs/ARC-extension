using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;


namespace Input_Insulation
{
    [Autodesk.Revit.Attributes.Transaction(Autodesk.Revit.Attributes.TransactionMode.Manual)]
    [Autodesk.Revit.Attributes.Regeneration(Autodesk.Revit.Attributes.RegenerationOption.Manual)]
    [Autodesk.Revit.Attributes.Journaling(Autodesk.Revit.Attributes.JournalingMode.NoCommandData)]
    public class InputInsulation_Command : IExternalCommand
    {
        #region Properties

        Document m_doc=null;

        #endregion

        public Result Execute(ExternalCommandData revit, ref string message, ElementSet elements)
        {
            UIDocument iuidoc = revit.Application.ActiveUIDocument;

            Document idoc = iuidoc.Document;

            ARCLibrary lib = new ARCLibrary();

            List<Element> listElement = null;

            List<Element> selectedElement = lib.CurrentSelection(iuidoc, idoc);

            if (selectedElement == null)
            {
                List<Element> pickElements = lib.PickElements(iuidoc, idoc);

                listElement = pickElements;
            }
            else
            {
                listElement = selectedElement;
            }
            try
            {

                MainWindow m_form = new MainWindow(idoc, listElement);

               
                m_form.ShowDialog();

                return Result.Succeeded;

            }
            catch (Exception ex)
            {
                message = ex.Message;
                return Result.Failed;
            }
        }
    }
}