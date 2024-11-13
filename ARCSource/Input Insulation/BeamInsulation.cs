using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Xml.Linq;

namespace Input_Insulation
{
    public class BeamInsulation
    {
        public static void InputBeamInsulation(Document doc, UIDocument uidoc)
        { 
            LibARC lib = new LibARC();

            List<Element> listElement = null;

            List<Element> selectedElement = lib.CurrentSelection(uidoc, doc);

            if (listElement == null)
                {
                    List<Element> pickElements = lib.PickElements(uidoc, doc);
                    listElement = pickElements;

                }
            else
            {
                listElement = selectedElement;
            }

            foreach (Element ele in listElement)
            {
                Line location = lib.GetBeamLocation(ele);
                    
                Element beamType = doc.GetElement(new ElementId (13038672));

                FamilySymbol beamTypeSymbol = beamType as FamilySymbol;

                lib.ActivateSymbol(doc, beamTypeSymbol);

                ElementId levelId = ele.get_Parameter(BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM).AsElementId();

                Level level = doc.GetElement(levelId) as Level;

                FamilyInstance newBeam = lib.CreateBeam(doc, location, beamTypeSymbol, level);

            }    

        }
    }
}
