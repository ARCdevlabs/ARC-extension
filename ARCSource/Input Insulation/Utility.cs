﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Forms.PropertyGridInternal;
using System.Xml.Linq;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Autodesk.Revit.UI;

namespace Input_Insulation
{
    public class Utility
    {
        public void InputBeamInsulation(Document doc, List<Element> listElement, FamilySymbol familySymbol, double thickness)
        {
            FamilyInstance newBeam = null;


            ARCLibrary lib = new ARCLibrary();

            double H_c = 2;
            double B_c = 1;
            double tw_c = 0.1;
            double tf_c = 0.1;

            TransactionGroup trangroup = new TransactionGroup(doc, "Input Beam Insulation Group Trans");
            {
                try
                {
                    foreach (Element ele in listElement)
                    {
                        ElementId categoryId = ele.Category.Id;

                        if (categoryId.IntegerValue != (int)BuiltInCategory.OST_StructuralFraming)
                        {
                            //TaskDialog.Show("Beam Information", categoryBuiltinId.ToString());
                            continue;
                        }
                        else
                        {
                            double lastStartLevelOffset = 0;
                            double lastEndLevelOffset = 0;

                            double startLevelOffset = ele.get_Parameter(BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION).AsDouble();
                            double endLevelOffset = ele.get_Parameter(BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION).AsDouble();

                            Element type = doc.GetElement(ele.GetTypeId());

                            //Parameter kích thước
                            try
                            {
                                H_c = type.LookupParameter("H_c").AsDouble();
                                B_c = type.LookupParameter("B_c").AsDouble();
                                tw_c = type.LookupParameter("tw_c").AsDouble();
                                tf_c = type.LookupParameter("tf_c").AsDouble();
                            }
                            catch
                            {
                                //TaskDialog.Show("Beam Information", "Đã có lỗi xảy ra");
                                //throw new Exception("Đã xảy ra lỗi!");

                                continue;
                            }

                            int yz_jus = ele.get_Parameter(BuiltInParameter.YZ_JUSTIFICATION).AsInteger();
                            if (yz_jus == 0)
                            {
                                double zOffset = ele.get_Parameter(BuiltInParameter.Z_OFFSET_VALUE).AsDouble();
                                lastStartLevelOffset = startLevelOffset + zOffset;
                                lastEndLevelOffset = endLevelOffset + zOffset;
                            }
                            if (yz_jus == 1)
                            {
                                double startZOffset = ele.get_Parameter(BuiltInParameter.START_Z_OFFSET_VALUE).AsDouble();
                                lastStartLevelOffset = startLevelOffset + startZOffset;
                                double endZOffset = ele.get_Parameter(BuiltInParameter.END_Z_OFFSET_VALUE).AsDouble();
                                lastEndLevelOffset = endLevelOffset + endZOffset;
                            }

                            Line location = lib.GetBeamLocation(ele);

                            FamilySymbol beamTypeSymbol = familySymbol;

                            lib.ActivateSymbol(doc, beamTypeSymbol);

                            ElementId levelId = ele.get_Parameter(BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM).AsElementId();

                            Level level = doc.GetElement(levelId) as Level;

                            Transaction trans1 = new Transaction(doc, "Input Beam Insulation");
                            {
                                trans1.Start();

                                newBeam = lib.CreateBeam(doc, location, beamTypeSymbol, level);  //Cần điều chỉnh lại beamTypeSymbol dựa vào form WPF

                                trans1.Commit();

                            }
                            Transaction trans2 = new Transaction(doc, "Setting Shape Insulation");
                            {
                                trans2.Start();
                                Parameter paramStartLevelOffset = newBeam.get_Parameter(BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION);
                                Parameter paramEndLevelOffset = newBeam.get_Parameter(BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION);

                                paramStartLevelOffset.Set(lastStartLevelOffset);
                                paramEndLevelOffset.Set(lastEndLevelOffset);

                                newBeam.LookupParameter("H").Set(H_c);
                                newBeam.LookupParameter("B").Set(B_c);
                                newBeam.LookupParameter("tw").Set(tw_c);
                                newBeam.LookupParameter("tf").Set(tf_c);

                                StructuralFramingUtils.DisallowJoinAtEnd(newBeam, 0);
                                StructuralFramingUtils.DisallowJoinAtEnd(newBeam, 1);
                                try
                                {
                                    Parameter paramStartJoinCutBack = newBeam.get_Parameter(BuiltInParameter.START_JOIN_CUTBACK);
                                    paramStartJoinCutBack.Set(0);
                                }
                                catch { }

                                try
                                {
                                    Parameter paramEndJoinCutBack = newBeam.get_Parameter(BuiltInParameter.END_JOIN_CUTBACK);
                                    paramEndJoinCutBack.Set(0);
                                }
                                catch { }

                                try
                                {
                                    Parameter paramStartExtend = newBeam.get_Parameter(BuiltInParameter.START_EXTENSION);
                                    paramStartExtend.Set(0);
                                }
                                catch { }

                                try
                                {
                                    Parameter paramEndExtend = newBeam.get_Parameter(BuiltInParameter.END_EXTENSION);
                                    paramEndExtend.Set(0);
                                }
                                catch { }

                                newBeam.get_Parameter(BuiltInParameter.Z_JUSTIFICATION).Set(2);

                                //TaskDialog.Show("Beam Information", "Last Start Level Offset: " + lastStartLevelOffset.ToString());

                                trans2.Commit();
                            }
                            Transaction trans3 = new Transaction(doc, "Setting Start End Level Offset and Cut Length");
                            {
                                trans3.Start();
                                newBeam.LookupParameter("Start_Level_Offset").Set(lastStartLevelOffset);
                                newBeam.LookupParameter("End_Level_Offset").Set(lastEndLevelOffset);
                                trans3.Commit();
                                //listInsulation.Add(newBeam);
                            }
                            Transaction trans4 = new Transaction(doc, "Setting Cut Length");
                            {
                                trans4.Start();
                                double cutLength = newBeam.get_Parameter(BuiltInParameter.STRUCTURAL_FRAME_CUT_LENGTH).AsDouble();
                                //TaskDialog.Show("Beam Information", "Cut Length trước: " + cutLength.ToString());
                                // Phương pháp chỉnh Cut_Length thất bại vì nếu chỉnh
                                // Cut_Length thì chiều dài dầm thay đổi => BuiltIn Cut Legnth lại bị thay đổi => Cần phải có công thức để BuiltIn Cut Legnth không ảnh hưởng 
                                newBeam.LookupParameter("Cut_Length").Set(cutLength);
                                trans4.Commit();
                            }
                        }

                        trangroup.Assimilate();
                    }
                }
                catch
                {
                    trangroup.RollBack();
                }
            }
            return;
        }

        public static void ColumnInsulation(Document m_doc, IList<Element> ids, TypeOfInsulation typeOfInsulation,string InsulationThickness)
        {
            Transaction t = new Transaction(m_doc, "Column Insulation");

            t.Start();
            foreach (Element element in ids)
            {
                //Element element = m_doc.GetElement(id);

                if (element.Category.Id != new ElementId(BuiltInCategory.OST_StructuralColumns))
                {
                    continue;
                }

                //Data ColumnInstance
                FamilyInstance m_instance = element as FamilyInstance;
                ColumnInstanceProperties m_ColumnProperties = new ColumnInstanceProperties();
                
                m_ColumnProperties = GetColumnProperties(m_doc, m_instance);

                
                try
                {
                    ColumnInsulation(m_doc, m_ColumnProperties, typeOfInsulation, InsulationThickness);
                    
                }
                catch 
                {
                   
                    

                }
                

                
                   
            }
            t.Commit();
            
        }

        /// <summary>
        /// Nhập tấm cách nhiệt cho cột có hình dạng là H
        /// </summary>
        /// <param name="m_doc"></param>
        /// <param name="properties"> Thông tin từ columnn cần nhập cách nhiệt</param>
        public static void ColumnInsulation(Document m_doc, ColumnInstanceProperties properties, TypeOfInsulation typeOfInsulation, string InsulationThickness)
        {
            string familyName = "gIns_Column-ver4";
            string symbolName ="t"+ InsulationThickness;
            

            Family family = (from f in new FilteredElementCollector(m_doc).OfClass(typeof(Family)).
                                Cast<Family>()
                                where (f.Name == familyName)
                                select f).First(); 
            
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

            insulation.LookupParameter("H").Set(properties.H);
            insulation.LookupParameter("B").Set(properties.B);

            try
            {
                insulation.LookupParameter("tw").Set(properties.tw.Value);
                insulation.LookupParameter("tf").Set(properties.tf.Value);

            }
            catch
            {


            }

            insulation.LookupParameter("合成耐火上").Set(0);
            insulation.LookupParameter("合成耐火下").Set(0);
            insulation.LookupParameter("合成耐火右").Set(0);
            insulation.LookupParameter("合成耐火左").Set(0);

            if (typeOfInsulation==TypeOfInsulation.けいカル||!properties.IsColumnH)
            {
                insulation.LookupParameter("H_type").Set(0);
            }
            else 
            {
                insulation.LookupParameter("H_type").Set(1);
            }

            insulation.LookupParameter("長さ__").Set(properties.Height);

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
            double offsetX, offsetY;
            try
            {
                offsetX = m_instance.LookupParameter("ex_project").AsDouble();
                offsetY = m_instance.LookupParameter("ey_project").AsDouble();
            }
            catch 
            {

                offsetX = m_instance.LookupParameter("フランジ方向_柱偏芯").AsDouble();
                offsetY = m_instance.LookupParameter("ウェブ方向_柱偏芯").AsDouble();
            }


            



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
                m_instanceProperties.IsColumnH = true;
            }
            catch 
            {

                m_instanceProperties.IsColumnH= false;
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
            private bool m_IsColumnH;

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
            public bool IsColumnH
            {
                get { return m_IsColumnH; }
                set { m_IsColumnH = value; }
            }
            
        }


        public enum TypeOfInsulation
        {
            けいカル = 0,
            巻き付け = 1,
        }
    }
}
