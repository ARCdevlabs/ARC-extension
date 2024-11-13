# -*- coding: utf-8 -*-
import Autodesk.Revit.DB as DB
def get_geometry_non_reference(element):
    all_gemetry = []
    try:
        geo_opt = DB.Options()
        geometry =  element.get_Geometry(geo_opt)
        for instance_geometry in geometry:
            element_geometry = instance_geometry.GetInstanceGeometry()
            for tung_geometry in element_geometry:
                if isinstance(tung_geometry, DB.Solid) and tung_geometry.Volume > 0:
                    all_gemetry.append(tung_geometry)
        return all_gemetry #Trả về dạng list các solid
    except:
        return all_gemetry

def find_intersect_elements(idoc, element_A, list_element_B):
    result_element = []
    try:
        list_solid = get_geometry_non_reference(element_A)
        list_element_id_dau_vao = []
        for tung_element_dau_vao in list_element_B:
            list_element_id_dau_vao.append(tung_element_dau_vao.Id)
        for tung_solid in list_solid:
            tat_ca_intersect_elements = DB.FilteredElementCollector(idoc).WherePasses(DB.ElementIntersectsSolidFilter(tung_solid))
            for tung_element in tat_ca_intersect_elements:
                if tung_element.Id in list_element_id_dau_vao:
                    result_element.append(tung_element)
        return result_element #Trả về dạng list các element
    except:
        return result_element