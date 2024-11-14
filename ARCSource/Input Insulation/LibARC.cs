using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Autodesk.Revit.UI;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI.Selection;
using Autodesk.Revit.DB.Structure;
using System.Windows.Controls;

namespace Input_Insulation
{
    public class ARCLibrary
    {
        public static Parameter GetBuiltInParameterByName(Element element, BuiltInParameter builtInParameter)
        {
            Parameter param = element.get_Parameter(builtInParameter);

            return param;
        }

        public static string GetParameterValueByName(Element element, string name)
        {
            // Lấy danh sách các tham số có tên tương ứng
            IList<Parameter> listParam = element.GetParameters(name);

            // Nếu không tìm thấy tham số, trả về null hoặc xử lý lỗi tùy ý
            if (listParam == null || listParam.Count == 0)
            {
                return null;
            }

            // Lấy tham số đầu tiên từ danh sách
            Parameter param = listParam[0];

            // Trả về giá trị của tham số dưới dạng chuỗi
            return param.AsValueString();
        }
        public Element PickElement(UIDocument uidoc, Document doc)
        {

            try
            {
                // Create a reference to pick an object
                Selection choices = uidoc.Selection;

                Reference pickedObjectRef = choices.PickObject(ObjectType.Element);

                if (pickedObjectRef != null)
                {
                    // Get the element ID of the picked object
                    ElementId elementId = pickedObjectRef.ElementId;

                    // Get the element corresponding to the picked object
                    Element pickedElement = doc.GetElement(elementId);

                    return pickedElement;

                    // Return null if no element was picked

                }
            }
            catch
            {
            }

            return null;
        }

        public List<Element> PickElements(UIDocument uidoc, Document doc)
        {

            // Create a reference to pick an object
            Selection choices = uidoc.Selection;

            IList<Reference> pickedObjectsRef = choices.PickObjects(ObjectType.Element);

            List<Element> listElements = new List<Element>();

            if (pickedObjectsRef != null)
            {
                foreach (Reference reference in pickedObjectsRef)
                {
                    ElementId elementId = reference.ElementId;
                    Element pickedElement = doc.GetElement(elementId);
                    listElements.Add(pickedElement);
                }
                return listElements;

            }
            return null;
        }

        public List<Element> CurrentSelection(UIDocument uidoc, Document doc)
        {
            try
            {
                List<Element> listElements = new List<Element>();

                Selection selection = uidoc.Selection;

                ICollection<ElementId> selectedIds = uidoc.Selection.GetElementIds();

                if (0 != selectedIds.Count)
                {
                    foreach (ElementId id in selectedIds)
                    {
                        Element getElements = doc.GetElement(id);

                        listElements.Add(getElements);

                    }
                    return listElements;
                }
                else
                {
                    return null;
                }

            }
            catch
            {
                return null;
            }

        }
        public Line GetBeamLocation(Element beam)
        {
            // Kiểm tra nếu Element không phải là dầm hoặc không có thông tin về vị trí
            if (beam == null || beam.Location == null || !(beam.Location is LocationCurve locationCurve))
            {
                throw new InvalidOperationException("Element không phải là dầm hoặc không có vị trí.");
            }

            // Lấy thông tin đường cong vị trí (LocationCurve)
            Curve beamCurve = locationCurve.Curve;

            // Lấy tọa độ điểm đầu và điểm cuối của dầm
            XYZ startPoint = beamCurve.GetEndPoint(0);
            XYZ endPoint = beamCurve.GetEndPoint(1);

            Line line = Line.CreateBound(startPoint, endPoint);

            return line;
        }

        public FamilyInstance CreateBeam(Document doc, Curve curve, FamilySymbol beamType, Level level)
        {
            // Tạo dầm mới
            FamilyInstance beam = doc.Create.NewFamilyInstance(curve, beamType, level, StructuralType.Beam);

            return beam;
        }

        public void ActivateSymbol(Document doc, FamilySymbol element)
        {
            try
            {
                // Kích hoạt FamilySymbol nếu chưa được kích hoạt
                if (element != null && !element.IsActive)
                {
                    element.Activate();
                    doc.Regenerate(); // Regenerate document to update changes in Revit
                }
            }
            catch
            {
                // Xử lý lỗi khi không kích hoạt được FamilySymbol
            }
        }
    }
}
