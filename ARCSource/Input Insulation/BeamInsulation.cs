using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Input_Insulation;
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
    public class BeamInsulation_Form
    {
        public void ChayChuongTrinh(Document doc, List<Element> listElement, FamilySymbol familySymbol, double thickness)
        {
            FamilyInstance newBeam = null;

            ARCLibrary lib = new ARCLibrary();

            double H_c = 2;
            double B_c = 1;
            double tw_c = 0.1;
            double tf_c = 0.1;

            TransactionGroup trangroup = new TransactionGroup(doc, "Input Beam Insulation Group Trans");
            {
                trangroup.Start();
                Transaction trans0 = new Transaction(doc, "Setting Thickness");
                {
                    trans0.Start();

                    familySymbol.LookupParameter("耐火被覆t").Set(thickness);

                    trans0.Commit();
                }

                try
                {

                    //List<Element> listInsulation = new List<Element>();
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
                            Transaction trans3 = new Transaction(doc, "Setting Start End Level Offset");
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
                    }

                    trangroup.Assimilate();
                }
                catch
                {
                    trangroup.RollBack();
                }
            }
            return;
        }
    }
}
