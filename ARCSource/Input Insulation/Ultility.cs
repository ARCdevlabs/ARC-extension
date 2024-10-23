using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace Input_Insulation
{
    public class Ultility
    {
       
        public static void ColumnInsulation (Document m_doc, IList<ElementId> ids)
        {
            //Lấy family symbol
            //RW symbol
           
            

            //Bố trí family theo vị trí cột.
            foreach (ElementId id in ids)
            {
                Element element = m_doc.GetElement(id);

                if (element.Category.Id != new ElementId(BuiltInCategory.OST_StructuralColumns))
                {
                    continue;
                }

                //Vị trí cột và data type cột
                FamilyInstance m_instance= element as FamilyInstance;
                ElementType ColumnType= m_doc.GetElement(m_instance.GetTypeId()) as ElementType;
                string familyName= ColumnType.FamilyName;

                XYZ m_ColumnlocationPoint = (m_instance.Location as LocationPoint).Point;
                double offsetX = m_instance.LookupParameter("ex_project").AsDouble();
                double offsetY = m_instance.LookupParameter("ey_project").AsDouble();
                double rotation = (m_instance.Location as LocationPoint).Rotation;
                XYZ p= new XYZ(m_ColumnlocationPoint.X+offsetX, m_ColumnlocationPoint.Y+offsetY,m_ColumnlocationPoint.Z);





                if (familyName.Contains("Column_Box"))
                {
                    ColumnBoxInsulation(m_doc, m_instance, p, rotation);
                }


            }

            //Set parameter
        }
        public static void ColumnBoxInsulation(Document m_doc,FamilyInstance m_instance, XYZ Point, double rotation)
        {
            
            ElementType ColumnType = m_doc.GetElement(m_instance.GetTypeId()) as ElementType;
           

            Level LevelBase = m_doc.GetElement(m_instance.get_Parameter(BuiltInParameter.FAMILY_BASE_LEVEL_PARAM).AsElementId()) as Level;
            double baseOffset = m_instance.get_Parameter(BuiltInParameter.FAMILY_BASE_LEVEL_OFFSET_PARAM).AsDouble();
            double OffsetAtBase = m_instance.LookupParameter("柱脚 x オフセット値").AsDouble();


            double LevelTopelevation = (m_doc.GetElement(m_instance.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM).AsElementId()) as Level).Elevation;
            double TopOffset = m_instance.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM).AsDouble();
            double OffsetAtTop = m_instance.LookupParameter("柱頭 x オフセット値").AsDouble();

            double Height_Insulation = LevelTopelevation + TopOffset + OffsetAtTop - (LevelBase.Elevation + baseOffset + OffsetAtBase);

            double H = ColumnType.LookupParameter("H").AsDouble();
            double B = ColumnType.LookupParameter("B").AsDouble();
            double r = ColumnType.LookupParameter("r").AsDouble();

            FamilySymbol RWSymbol = (from fs in new FilteredElementCollector(m_doc).
                                   OfClass(typeof(FamilySymbol)).
                                   Cast<FamilySymbol>()

                                     where (fs.Family.Name.Contains("gIns_柱被覆_Box_RW") && fs.Name == "Box柱_RW25")
                                     select fs).First();

            FamilyInstance insulation=m_doc.Create.NewFamilyInstance(Point, RWSymbol, Autodesk.Revit.DB.Structure.StructuralType.NonStructural);
            //rotate
           
            XYZ cc = new XYZ(Point.X, Point.Y, Point.Z + 10);
            Line axis = Line.CreateBound(Point, cc);
            ElementTransformUtils.RotateElement(m_doc, insulation.Id, axis, rotation);

            insulation.LookupParameter("W上").Set(H / 2);
            insulation.LookupParameter("W下").Set(H/2);
            insulation.LookupParameter("W右").Set(B / 2);
            insulation.LookupParameter("W左").Set(B / 2);
            insulation.LookupParameter("長さ").Set(Height_Insulation);

            insulation.LookupParameter("合成耐火上").Set(0);
            insulation.LookupParameter("合成耐火下").Set(0);
            insulation.LookupParameter("合成耐火右").Set(0);
            insulation.LookupParameter("合成耐火左").Set(0);
        }
        public static void ColumnHInsulation(Document m_doc, FamilyInstance m_instance, XYZ Point, double rotation)
        {
            string familyName = "gIns_柱被覆_H_RW_";
            string symbolName = "t25";

            ElementType ColumnType = m_doc.GetElement(m_instance.GetTypeId()) as ElementType;
            

            Level LevelBase = m_doc.GetElement(m_instance.get_Parameter(BuiltInParameter.FAMILY_BASE_LEVEL_PARAM).AsElementId()) as Level;
            double baseOffset = m_instance.get_Parameter(BuiltInParameter.FAMILY_BASE_LEVEL_OFFSET_PARAM).AsDouble();
            double OffsetAtBase = m_instance.LookupParameter("柱脚 x オフセット値").AsDouble();


            double LevelTopelevation = (m_doc.GetElement(m_instance.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM).AsElementId()) as Level).Elevation;
            double TopOffset = m_instance.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM).AsDouble();
            double OffsetAtTop = m_instance.LookupParameter("柱頭 x オフセット値").AsDouble();

            double Height_Insulation = LevelTopelevation + TopOffset + OffsetAtTop - (LevelBase.Elevation + baseOffset + OffsetAtBase);

            double H = ColumnType.LookupParameter("H").AsDouble();
            double B = ColumnType.LookupParameter("B").AsDouble();
            double tw = ColumnType.LookupParameter("tw").AsDouble();
            double tf = ColumnType.LookupParameter("tf").AsDouble();
            double r = ColumnType.LookupParameter("r").AsDouble();

            FamilySymbol RWSymbol = (from fs in new FilteredElementCollector(m_doc).
                                   OfClass(typeof(FamilySymbol)).
                                   Cast<FamilySymbol>()

                                     where (fs.Family.Name.Contains(familyName) && fs.Name == symbolName)
                                     select fs).First();

            FamilyInstance insulation = m_doc.Create.NewFamilyInstance(Point, RWSymbol, Autodesk.Revit.DB.Structure.StructuralType.NonStructural);
            //rotate

            XYZ cc = new XYZ(Point.X, Point.Y, Point.Z + 10);
            Line axis = Line.CreateBound(Point, cc);
            ElementTransformUtils.RotateElement(m_doc, insulation.Id, axis, rotation);

            insulation.LookupParameter("ColumnD__").Set(H);
            insulation.LookupParameter("ColumnW__").Set(B);
            insulation.LookupParameter("Columnウェブt__").Set(tw);
            insulation.LookupParameter("Columnフランジt__").Set(tf);

            insulation.LookupParameter("合成耐火上").Set(0);
            insulation.LookupParameter("合成耐火下").Set(0);
            insulation.LookupParameter("合成耐火右").Set(0);
            insulation.LookupParameter("合成耐火左").Set(0);

            insulation.LookupParameter("長さ").Set(Height_Insulation);
        }

    }
}
