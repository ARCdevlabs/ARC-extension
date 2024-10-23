using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Input_Insulation;

namespace Input_Insulation
{
    public partial class FormTest : System.Windows.Forms.Form
    {
        private IList<ElementId> elementIds = new List<ElementId>();
        private Document m_doc;
        public FormTest(Document document, ICollection<ElementId> ids)
        {
            InitializeComponent();
            elementIds = ids.ToList();
            m_doc= document;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Transaction t= new Transaction(m_doc, "Input Column Insulation");
            t.Start();
            Ultility.ColumnInsulation(m_doc, elementIds);
            t.Commit();
        }
    }
}
