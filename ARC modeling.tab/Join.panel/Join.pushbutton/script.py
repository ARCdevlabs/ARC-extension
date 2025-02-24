# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib
try:
    ARC = string.ascii_lowercase
    begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
    module = importlib.import_module(str(begin))
    if module.AutodeskData():
        import Autodesk
        from Autodesk.Revit.DB import *
        from System.Collections.Generic import *
        from Autodesk.Revit.DB import*
        from Autodesk.Revit.DB import *
        from System.Collections.Generic import *
        from rpw.ui.forms import Alert
        import sys
        #Get UIDocument
        uidoc = __revit__.ActiveUIDocument
        #Get Document 
        doc = uidoc.Document
        Currentview = doc
        # Khai bao
        List1 = []
        Input1 = []
        Input2 =[]
        List2 = []
        ListIntersected = []
        Join = []
        CountSwitchJoin = []
        ListElePick = []

        # Def join geometry
        def joingeometry(List1, List2):
            import Autodesk
            CountSwitchJoin = []
            Join = []
            for i in List1:
                Bdb = i.get_BoundingBox(None)
                Outlineofbb = (Outline(Bdb.Min, Bdb.Max))
                for intersected in Autodesk.Revit.DB.FilteredElementCollector(doc).WherePasses(Autodesk.Revit.DB.BoundingBoxIntersectsFilter(Outlineofbb)):
                # Check xem list filter
                    for a in List2:
                        if a.Id == intersected.Id:
                    # Code join geometry
                            try:
                                result = Autodesk.Revit.DB.JoinGeometryUtils.JoinGeometry(doc,i,intersected)
                                checkcutting = Autodesk.Revit.DB.JoinGeometryUtils.IsCuttingElementInJoin(doc,i,intersected)
                                Join.Add("OK")
                                if str(checkcutting) == "False":
                                    switchjoin = Autodesk.Revit.DB.JoinGeometryUtils.SwitchJoinOrder(doc,i,intersected)
                            except:
                                try:
                                    checkcutting = Autodesk.Revit.DB.JoinGeometryUtils.IsCuttingElementInJoin(doc,i,intersected)
                                    if str(checkcutting) == "False":
                                        switchjoin = Autodesk.Revit.DB.JoinGeometryUtils.SwitchJoinOrder(doc,i,intersected)
                                        CountSwitchJoin.append("OK")
                                except:
                                    pass
            LenJoin = str(len (Join))
            LenSwitchjoin = str(len (CountSwitchJoin))
            Mes = "Joined: " + LenJoin + " and Switch join: " + LenSwitchjoin
            Alert(Mes,title="Mes",header= "Report number Join and Switch joined")
            return 


        '''lay list 1 ra'''
        import pickle
        from pyrevit.coreutils import appdata
        from pyrevit.framework import List
        from pyrevit import revit, DB


        def get_document_data_file(file_id, file_ext, add_cmd_name=False):
            proj_info = revit.query.get_project_info()

            if add_cmd_name:
                script_file_id = '{}_{}_{}'.format(EXEC_PARAMS.command_name,
                                                file_id,
                                                proj_info.filename
                                                or proj_info.name)
            else:
                script_file_id = '{}_{}'.format(file_id,
                                                proj_info.filename
                                                or proj_info.name)

            return appdata.get_data_file(script_file_id, file_ext)
        datafile1 = get_document_data_file("List1", "txt")
        selection = revit.get_selection()
        try:
            f = open(datafile1, 'r')
            current_selection = pickle.load(f)
            f.close()
            element_ids = []
            for elid in current_selection:
                Input1.append(doc.GetElement(ElementId(int(elid))))
        except Exception:
            pass


        # '''Lay list 2 ra'''
        datafile2 = get_document_data_file("List2", "txt")
        try:
            f = open(datafile2, 'r')
            current_selection = pickle.load(f)
            f.close()
            element_ids = []
            for elid in current_selection:
                Input2.append(doc.GetElement(ElementId(int(elid))))
        except Exception:
            pass


        if len(Input1) == 0 or len(Input2) == 0:
            from pyrevit.coreutils import applocales
            current_applocale = applocales.get_current_applocale()
            if str(current_applocale) == "日本語 / Japanese (ja)":
                message = "このコマンドを使用する前に、リスト選択1 and リスト選択2 コマンドを使用してください。"
            else:
                message = "Hãy sử dụng tool Select List 1 và Select list 2 trước khi sử dụng tool này"
            module.message_box(message)
            import sys
            sys.exit()
        # Dao nguoc input
        from rpw.ui.forms import SelectFromList
        value = SelectFromList('Priority', ['@Please choose which list to prioritize','List 1','List 2'])
        if value =="List 1":
            List1 = Input1
            List2 = Input2
        else:
            if value == "List 2":
                List1 = Input2
                List2 = Input1
            else:
                Alert('Please choose which list to prioritize',title="Warning",header= "Something wrong")
                sys.exit()
        t = Transaction (doc, "JoinGeometry")
        t.Start()
        joingeometry(List1, List2)
        t.Commit()
except:
    pass
