# encoding: utf-8
from nances import HOST_APP, UI, message_box
from Autodesk.Revit.UI import UIApplication, RevitCommandId, PostableCommand
try:
    uiapp = HOST_APP.uiapp
    uiapp.PostCommand(UI.RevitCommandId.LookupCommandId("CustomCtrl_%CustomCtrl_%Add-Ins%Create and Update Type%Create and Update Type"))
except:
    from pyrevit.coreutils import applocales
    current_applocale = applocales.get_current_applocale()
    if str(current_applocale) == '日本語 / Japanese (ja)':
        message = 'このツールを使用するには、Mau Cuongさんのタイプ作成のアドインをインストールしてください。使用方法については、SonさんまたはMau Cuongさんにお問い合わせください。'
    else:
        message = 'Hãy cài AddIn Tạo type của M.Cường để dùng được tool này. Liên hệ Sơn hoặc M.Cường để biết cách sử dụng.'
    message_box(message)