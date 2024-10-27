using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Forms.PropertyGridInternal;
using System.Xml.Linq;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace Input_Insulation
{
    public class Utility
    {
        public static void ColumnInsulation(Document m_doc, IList<ElementId> ids)
        {

            foreach (ElementId id in ids)
            {
                Element element = m_doc.GetElement(id);

                if (element.Category.Id != new ElementId(BuiltInCategory.OST_StructuralColumns))
                {
                    continue;
                }

                //Data ColumnInstance
                FamilyInstance m_instance = element as FamilyInstance;
                ColumnInstanceProperties m_ColumnProperties = new ColumnInstanceProperties();
                m_ColumnProperties = GetColumnProperties(m_doc, m_instance);

                if (m_ColumnProperties.ColumnTypeName.Contains("Column_Box"))
                {
                    ColumnBoxInsulation(m_doc, m_ColumnProperties);
                }
                else if ((m_ColumnProperties.ColumnTypeName.Contains("Column_H")))
                {
                    ColumnHInsulation(m_doc, m_ColumnProperties);
                }
                   
            }
            
        }
        /// <summary>
        /// Nhập cách nhiệt cho cột có hình dạng box
        /// </summary>
        /// <param name="m_doc"></param>
        /// <param name="properties">Thuộc tính lấy từ cột cần nhập cách nhiệt</param>
        public static void ColumnBoxInsulation(Document m_doc, ColumnInstanceProperties properties)
        {

            FamilySymbol RWSymbol = (from fs in new FilteredElementCollector(m_doc).
                                   OfClass(typeof(FamilySymbol)).
                                   Cast<FamilySymbol>()

                                     where (fs.Family.Name.Contains("gIns_柱被覆_Box_RW") && fs.Name == "Box柱_RW25")
                                     select fs).First();

            FamilyInstance insulation = m_doc.Create.NewFamilyInstance(properties.Location, RWSymbol, Autodesk.Revit.DB.Structure.StructuralType.NonStructural);

            //Xoay cách nhiệt theo hướng của cột.
            XYZ cc = new XYZ(properties.Location.X, properties.Location.Y, properties.Location.Z + 10);
            Line axis = Line.CreateBound(properties.Location, cc);
            ElementTransformUtils.RotateElement(m_doc, insulation.Id, axis, properties.Rotation);

            insulation.LookupParameter("W上").Set(properties.H / 2);
            insulation.LookupParameter("W下").Set(properties.H / 2);
            insulation.LookupParameter("W右").Set(properties.B / 2);
            insulation.LookupParameter("W左").Set(properties.B / 2);
            insulation.LookupParameter("長さ").Set(properties.Height);

            insulation.LookupParameter("合成耐火上").Set(0);
            insulation.LookupParameter("合成耐火下").Set(0);
            insulation.LookupParameter("合成耐火右").Set(0);
            insulation.LookupParameter("合成耐火左").Set(0);
        }


        /// <summary>
        /// Nhập tấm cách nhiệt cho cột có hình dạng là H
        /// </summary>
        /// <param name="m_doc"></param>
        /// <param name="properties"> Thông tin từ columnn cần nhập cách nhiệt</param>
        public static void ColumnHInsulation(Document m_doc, ColumnInstanceProperties properties)
        {
            string familyName = "gIns_柱被覆_H_RW_";
            string symbolName = "t25";

            FamilySymbol RWSymbol = (from fs in new FilteredElementCollector(m_doc).
                                   OfClass(typeof(FamilySymbol)).
                                   Cast<FamilySymbol>()

                                     where (fs.Family.Name.Contains(familyName) && fs.Name == symbolName)
                                     select fs).First();

            FamilyInstance insulation = m_doc.Create.NewFamilyInstance(properties.Location, RWSymbol, Autodesk.Revit.DB.Structure.StructuralType.NonStructural);
            //rotate

            XYZ cc = new XYZ(properties.Location.X, properties.Location.Y, properties.Location.Z + 10);
            Line axis = Line.CreateBound(properties.Location, cc);
            ElementTransformUtils.RotateElement(m_doc, insulation.Id, axis, properties.Rotation);

            insulation.LookupParameter("ColumnD__").Set(properties.H);
            insulation.LookupParameter("ColumnW__").Set(properties.B);

            insulation.LookupParameter("Columnウェブt__").Set(properties.tw.Value);
            insulation.LookupParameter("Columnフランジt__").Set(properties.tf.Value);

            insulation.LookupParameter("合成耐火上").Set(0);
            insulation.LookupParameter("合成耐火下").Set(0);
            insulation.LookupParameter("合成耐火右").Set(0);
            insulation.LookupParameter("合成耐火左").Set(0);

            insulation.LookupParameter("長さ").Set(properties.Height);
        }
        /// <summary>
        /// Lấy thông tin từ column để nhập tấm cách nhiệt
        /// </summary>
        /// <param name="m_doc"> Document từ project </param>
        /// <param name="m_instance">Cột cần lấy thông tin</param>
        /// <returns></returns>
        private static ColumnInstanceProperties GetColumnProperties(Document m_doc, FamilyInstance m_instance)
        {
            ColumnInstanceProperties m_instanceProperties = new ColumnInstanceProperties();
            //LocationPoint
            XYZ m_ColumnlocationPoint = (m_instance.Location as LocationPoint).Point;
            double offsetX = m_instance.LookupParameter("ex_project").AsDouble();
            double offsetY = m_instance.LookupParameter("ey_project").AsDouble();
            m_instanceProperties.Location = new XYZ(m_ColumnlocationPoint.X + offsetX, m_ColumnlocationPoint.Y + offsetY, m_ColumnlocationPoint.Z);

            //Rotation
            m_instanceProperties.Rotation = (m_instance.Location as LocationPoint).Rotation;

            ElementType ColumnType = m_doc.GetElement(m_instance.GetTypeId()) as ElementType;
            m_instanceProperties.ColumnTypeName = ColumnType.Name;
            m_instanceProperties.ColumnFamilyName = ColumnType.FamilyName;

            //Level ID
            m_instanceProperties.BaseLevelId = m_instance.get_Parameter(BuiltInParameter.FAMILY_BASE_LEVEL_PARAM).AsElementId();

            Level LevelBase = m_doc.GetElement(m_instanceProperties.BaseLevelId) as Level;


            //Calculate column height
            double baseOffset = m_instance.get_Parameter(BuiltInParameter.FAMILY_BASE_LEVEL_OFFSET_PARAM).AsDouble();
            double OffsetAtBase = m_instance.LookupParameter("柱脚 x オフセット値").AsDouble();


            double LevelTopelevation = (m_doc.GetElement(m_instance.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM).AsElementId()) as Level).Elevation;
            double TopOffset = m_instance.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM).AsDouble();
            double OffsetAtTop = m_instance.LookupParameter("柱頭 x オフセット値").AsDouble();

            m_instanceProperties.Height = LevelTopelevation + TopOffset + OffsetAtTop - (LevelBase.Elevation + baseOffset + OffsetAtBase);



            m_instanceProperties.H = ColumnType.LookupParameter("H").AsDouble();
            m_instanceProperties.B = ColumnType.LookupParameter("B").AsDouble();
            try
            {
                m_instanceProperties.tw = ColumnType.LookupParameter("tw").AsDouble();
                m_instanceProperties.tf = ColumnType.LookupParameter("tf").AsDouble();
            }
            catch (Exception)
            {

                throw;
            }

            //double r = ColumnType.LookupParameter("r").AsDouble();

            return m_instanceProperties;
        }

        /// <summary>
        /// Class các thông tin từ column
        /// </summary>
        public class ColumnInstanceProperties
        {
            private double m_H;
            private double m_B;
            private double? m_tw;
            private double? m_tf;
            private double m_Height;
            private XYZ m_location;
            private double m_rotation;
            private ElementId m_BaseLevelId;
            private string m_TypeName;
            private string m_FamilyName;

            public double H
            {
                get { return m_H; }
                set { m_H = value; }
            }
            public double B
            { get { return m_B; } set { m_B = value; } }

            public double? tw
            { get { return m_tw; } set { m_tw = value; } }
            public double? tf
            {
                get { return m_tf; }
                set { m_tf = value; }
            }

            public double Height
            { get { return m_Height; } set { m_Height = value; } }

            public XYZ Location
            { get { return m_location; } set { m_location = value; } }
            public double Rotation
            { get { return m_rotation; } set { m_rotation = value; } }

            public ElementId BaseLevelId
            { get { return m_BaseLevelId; } set { m_BaseLevelId = value; } }
            public string ColumnTypeName
            {
                get { return m_TypeName; }
                set { m_TypeName = value; }
            }

            public string ColumnFamilyName
            {
                get { return m_FamilyName; }
                set { m_FamilyName = value; }

            }  
        }


        public enum TypeOfInsulation
        {
            けいカル = 1,
            巻き付け = 1,
        }
    }
}
