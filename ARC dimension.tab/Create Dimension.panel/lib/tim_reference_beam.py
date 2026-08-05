# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import Plane
import nances
if nances.AutodeskData():
    class ClassTimReference:
        def __init__(self, faces, center_plane, module_vectortransform):
            self.faces = faces           
            self.center_plane = center_plane            
            self.vectortransform = module_vectortransform

            self.ref_face_max = None
            self.ref_face_min = None
            self.max_value = None
            self.min_value = None

        def tim_reference_beam(self):
            center_plane_normal = self.center_plane.Normal
            list_distance = []
            list_outer_face = []
            for face in self.faces:
                try:
                    face_origin = face.Origin
                    face_normal = face.FaceNormal
                    face_to_plane = Plane.CreateByNormalAndOrigin(face_normal, face_origin)                    
                    check_pararel = self.vectortransform.are_planes_parallel(center_plane_normal, face_normal)
                    if check_pararel:
                        distance =  self.vectortransform.distance_between_parallel_planes(face_to_plane, self.center_plane)
                        list_distance.append(distance)
                        list_outer_face.append(face.Reference)
                except:
                    # import traceback
                    # print(traceback.format_exc())
                    pass
            if list_distance:    
                max_value = max(list_distance)
                max_index = list_distance.index(max_value)
                min_value = min(list_distance)
                min_index = list_distance.index(min_value)
                self.ref_face_max = list_outer_face[max_index]
                self.ref_face_min = list_outer_face[min_index]    
                self.max_value = max_value
                self.min_value = min_value                   
                return self
            else:
                self.ref_face_max = None
                self.ref_face_min = None
                self.max_value = None
                self.min_value = None