# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import Plane
import nances
if nances.AutodeskData():
    class ClassTimReference:
        def __init__(self, faces, X_vector, Y_vector, X_plane, Y_plane, module_vectortransform):
            self.faces = faces
            self.X_vector = X_vector
            self.Y_vector = Y_vector
            self.X_plane = X_plane
            self.Y_plane = Y_plane
            self.vectortransform = module_vectortransform

            self.ref_face_max = None
            self.ref_face_min = None
            self.ref_face_max_X = None
            self.ref_face_min_X = None
            self.max_value_X = None
            self.max_value_Y = None

        def tim_reference_column (self):
            list_distance_Y = []
            list_distance_X = []
            list_outer_face_Y = []
            list_outer_face_X = []
            for face in self.faces:
                try:
                    face_origin = face.Origin
                    face_normal = face.FaceNormal
                    face_to_plane = Plane.CreateByNormalAndOrigin(face_normal, face_origin)                                               
                    check_pararel_Y = self.vectortransform.are_planes_parallel(self.Y_vector,face_normal)
                    if check_pararel_Y == False:
                        check_pararel_X = self.vectortransform.are_planes_parallel(self.X_vector,face_normal)

                    if check_pararel_Y == True: 
                        distance_Y =  self.vectortransform.distance_between_parallel_planes(face_to_plane, self.X_plane)
                        list_distance_Y.append(distance_Y)
                        list_outer_face_Y.append(face.Reference)

                    else:
                        if check_pararel_X == True:
                            distance_X =  self.vectortransform.distance_between_parallel_planes(face_to_plane, self.Y_plane)
                            list_distance_X.append(distance_X)
                            list_outer_face_X.append(face.Reference)
                except:
                    pass
            try:
                max_value_Y = max(list_distance_Y)
                max_index = list_distance_Y.index(max_value_Y)
                min_value = min(list_distance_Y)
                min_index = list_distance_Y.index(min_value)
                self.ref_face_max = list_outer_face_Y[max_index]
                self.ref_face_min = list_outer_face_Y[min_index]
                self.max_value_Y = max_value_Y
            except:
                pass
            try:
                max_value_X = max(list_distance_X)
                max_index_X = list_distance_X.index(max_value_X)
                min_value_X = min(list_distance_X)
                min_index_X = list_distance_X.index(min_value_X)
                self.ref_face_max_X = list_outer_face_X[max_index_X]
                self.ref_face_min_X = list_outer_face_X[min_index_X]
                self.max_value_X = max_value_X
            except:
                pass
            return self
