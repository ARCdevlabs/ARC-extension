__doc__ = 'nguyenthanhson1712@gmail.com'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
from codecs import Codec
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *
from Autodesk.Revit.UI.Selection import ObjectType, Selection
import traceback
try:
    if module.AutodeskData():
        uidoc = __revit__.ActiveUIDocument
        doc = uidoc.Document
        Ele = module.get_selected_elements(uidoc,doc,False)
        element = []
        if Ele == False:

            pick = uidoc.Selection.PickObject(ObjectType.Element)
            element.append(doc.GetElement(pick.ElementId))
        else:
            for i in Ele:
                element.append(i)

        select = uidoc.Selection
        list_id = []
        pick = element
        try:
            for i in pick:  
                EleId = i.Id
                ele = doc.GetElement(EleId)
                host = ele.Host.Id
                list_id.append(host)
                Icollection = List[ElementId](list_id)
                select.SetElementIds(Icollection)
        except:
            pass
except:
    # print(traceback.format_exc())
    pass