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
        
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            UIDocument uIDocument = commandData.Application.ActiveUIDocument;
            m_doc =uIDocument.Document;
            ICollection<ElementId> ids = uIDocument.Selection.GetElementIds();

            
            try
            {
                
                FormTest m_form = new FormTest(m_doc, ids);
                m_form.ShowDialog();
                return Autodesk.Revit.UI.Result.Succeeded;

            }
            catch (Exception ex)
            {
                message = ex.Message;
                return Autodesk.Revit.UI.Result.Failed;
            }
            
        }
    }
}