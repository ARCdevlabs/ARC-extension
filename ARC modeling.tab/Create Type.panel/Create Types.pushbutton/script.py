# encoding: utf-8
from nances import HOST_APP, UI, message_box
from Autodesk.Revit.UI import UIApplication, RevitCommandId, PostableCommand
try:
    uiapp = HOST_APP.uiapp
    uiapp.PostCommand(UI.RevitCommandId.LookupCommandId("1CustomCtrl_%CustomCtrl_%Add-Ins%Create and Update Type%Create and Update Type"))
except:
    message_box("Hãy cài AddIn Tạo type của M.Cường để dùng được tool này. "
                "Liên hệ Sơn hoặc M.Cường để biết cách sử dụng.")