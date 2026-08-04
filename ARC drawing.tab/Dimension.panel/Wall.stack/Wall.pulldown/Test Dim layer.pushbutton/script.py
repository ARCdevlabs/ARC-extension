# -*- coding: utf-8 -*-
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
import traceback
import math

import nances as module
from nances import vectortransform,geometry,selection
import tim_reference_beam

if module.AutodeskData():
    uidoc = __revit__.ActiveUIDocument
    #Get Document 
    doc = uidoc.Document
    Currentview = doc.ActiveView
    Curve = []

    def create_plane_from_point_and_normal(point, normal):
        plane = Plane(normal, point)
        return plane

    def are_planes_parallel(normal1, normal2):
        tolerance=0.0000001
        cross_product = normal1.CrossProduct(normal2)
        return cross_product.GetLength() < tolerance

    def distance_between_planes(normal1, point_on_plane1, normal2):
        vector_between_planes = point_on_plane1 - (point_on_plane1.DotProduct(normal2) - normal2.DotProduct(normal1)) / normal1.DotProduct(normal2) * normal1
        distance = vector_between_planes.GetLength()
        return distance
    def get_point_at_center_line(wall):
        wall_location = wall.Location
        wall_location_curve = wall_location.Curve
        start_point = wall_location_curve.GetEndPoint(0)
        return start_point
    def get_center_plane (wall):
        wall_location = wall.Location
        wall_location_curve = wall_location.Curve
        start_point = wall_location_curve.GetEndPoint(0)
        endpoint = wall_location_curve.GetEndPoint(1)
        mid_point = wall_location_curve.Evaluate(0.5, True)
        offset_mid_point = XYZ(start_point.X, start_point.Y, mid_point.Z +10000)
        point1 = start_point
        point2 = endpoint
        point3 =offset_mid_point
        vector1 = point2 - point1
        vector2 = point3 - point1
        normal_vector = vector1.CrossProduct(vector2).Normalize()
        plane = Plane.CreateByNormalAndOrigin(normal_vector, mid_point)
        return plane

    def get_rotate_90_location_wall_center (wall):
        from Autodesk.Revit.DB import Line
        wall_location = wall.Location
        wall_location_curve = wall_location.Curve
        mid_point = wall_location_curve.Evaluate(0.5, True)
        Z_point = XYZ(mid_point.X, mid_point.Y, mid_point.Z + 10)
        Z_axis = Line.CreateBound(mid_point, Z_point)
        curve_of_location_curve = Line.CreateBound(wall_location_curve.GetEndPoint(0),wall_location_curve.GetEndPoint(1))
        detail_curve_of_location_curve = doc.Create.NewDetailCurve(Currentview,curve_of_location_curve)
        locate_detail_curve_of_location_curve = detail_curve_of_location_curve.Location
        retate_locate_detail_curve_of_location_curve = locate_detail_curve_of_location_curve.Rotate(Z_axis, 2 * math.pi / 4)
        return detail_curve_of_location_curve
            
    def get_geometry(element):
        option = Options()
        option.ComputeReferences = True
        geo_ref =  element.get_Geometry(option)
        return geo_ref

    def get_face(geometry):
        for solid in geometry:
            face = solid.Faces
        return face

    def distance_to_plane(point, plane):
        distance = plane.Normal.DotProduct(point - plane.Origin)
        return distance
    def distance_between_parallel_planes(plane1, plane2):
        point_on_plane = XYZ(0, 0, 0)
        distance1 = abs(distance_to_plane(point_on_plane, plane1))
        distance2 = abs(distance_to_plane(point_on_plane, plane2))
        distance = (distance1 - distance2)
        return distance

    def WallDimension(doc, uidoc, elements, type, fm, pickedPoint, schema):

        lstDims = []
        list_walls = []
        list2_walls = []

        # ============================================================
        # Phân loại Wall:
        # - Wall có CompoundStructure và LayerCount > 1
        # - Wall còn lại
        # ============================================================

        for element in elements:

            wall = element if isinstance(element, Wall) else None

            if wall is not None:

                wallType = wall.WallType
                compoundStructure = wallType.GetCompoundStructure()

                if compoundStructure is not None and compoundStructure.LayerCount > 1:
                    list_walls.append(wall)
                else:
                    list2_walls.append(wall)


        # ============================================================
        # Xử lý các Wall có nhiều layer
        # ============================================================

        for wall in list_walls:

            # Exterior
            reference = None

            closestWallExterior = GetClosestWallReference(
                wall.Document,
                wall,
                ShellLayerType.Exterior
            )

            # Interior
            reference2 = None

            closestWallInterior = GetClosestWallReference(
                wall.Document,
                wall,
                ShellLayerType.Interior
            )


            # Nếu tìm được Wall exterior gần nhất
            if closestWallExterior is not None:

                list2_walls[:] = [
                    w for w in list2_walls
                    if w.Id != closestWallExterior.Id
                ]


            # Nếu tìm được Wall interior gần nhất
            if closestWallInterior is not None:

                list2_walls[:] = [
                    w for w in list2_walls
                    if w.Id != closestWallInterior.Id
                ]


            # Gọi CallAction
            CallAction(
                wall,
                doc,
                type,
                fm,
                lstDims,
                pickedPoint,
                schema,
                True
            )


        # ============================================================
        # Xử lý các Wall còn lại
        # ============================================================

        for wall in list2_walls:

            # Exterior
            closestWallReference = GetClosestWallReference(
                wall.Document,
                wall,
                ShellLayerType.Exterior
            )

            # Interior
            closestWallReference2 = GetClosestWallReference(
                wall.Document,
                wall,
                ShellLayerType.Interior
            )


            # Chỉ CallAction khi KHÔNG tìm được
            # cả Exterior lẫn Interior
            if (
                closestWallReference is None
                and closestWallReference2 is None
            ):

                CallAction(
                    wall,
                    doc,
                    type,
                    fm,
                    lstDims,
                    pickedPoint,
                    schema,
                    False
                )

    def GetClosestWallReference(doc, wall, shellLayerType):
        """
        Tìm Wall gần nhất và Reference của mặt Exterior/Interior gần Wall đầu vào nhất.

        Parameters
        ----------
        doc : Document
            Revit Document
        wall : Wall
            Wall cần tìm Wall gần nhất
        shellLayerType : ShellLayerType
            DB.ShellLayerType.Exterior hoặc DB.ShellLayerType.Interior

        Returns
        -------
        tuple
            (Wall, Reference)

            Nếu không tìm được:
            (None, None)
        """

        # ============================================================
        # 1. Lấy side face của Wall đầu vào
        # ============================================================

        sideFaces = DB.HostObjectUtils.GetSideFaces(
            wall,
            shellLayerType
        )

        if sideFaces is None or sideFaces.Count == 0:
            return None, None

        # Reference đầu tiên
        wallRef = sideFaces[0]

        # Lấy Face
        element = doc.GetElement(wallRef)

        face = element.GetGeometryObjectFromReference(wallRef)

        if face is None:
            return None, None

        # ============================================================
        # 2. Lấy điểm giữa của Face
        # ============================================================

        bbox = face.GetBoundingBox()

        center_uv = (bbox.Min + bbox.Max) / 2.0

        xyz = face.Evaluate(center_uv)

        # ============================================================
        # 3. Lấy tất cả Wall khác
        # ============================================================

        walls = DB.FilteredElementCollector(doc) \
            .OfClass(DB.Wall) \
            .WhereElementIsNotElementType() \
            .ToElements()

        # ============================================================
        # 4. Các biến dùng để tìm Wall gần nhất
        # ============================================================

        closestWall = None
        closestReference = None

        minDistance = float("inf")

        # 0.2 feet
        maxDistance = 0.2

        # Orientation của Wall hiện tại
        wallOrientation = wall.Orientation

        # ============================================================
        # 5. Duyệt tất cả Wall
        # ============================================================

        for wall2 in walls:

            # Bỏ qua chính Wall hiện tại
            if wall2.Id == wall.Id:
                continue

            # ========================================================
            # 6. Kiểm tra 2 Wall có song song không
            # ========================================================

            wall2Orientation = wall2.Orientation

            cross = wallOrientation.CrossProduct(
                wall2Orientation
            )

            # Nếu cross product gần 0 => song song
            if cross.GetLength() >= 0.001:
                continue

            # ========================================================
            # 7. Lấy mặt Exterior của Wall2
            # ========================================================

            sideFaces2 = DB.HostObjectUtils.GetSideFaces(
                wall2,
                DB.ShellLayerType.Exterior
            )

            if sideFaces2 is None or sideFaces2.Count == 0:
                continue

            exteriorReference = sideFaces2[0]

            element2 = doc.GetElement(exteriorReference)

            face2 = element2.GetGeometryObjectFromReference(
                exteriorReference
            )

            if face2 is None:
                continue

            # Lấy điểm giữa mặt Exterior
            bbox2 = face2.GetBoundingBox()

            center_uv2 = (bbox2.Min + bbox2.Max) / 2.0

            source = face2.Evaluate(center_uv2)

            # ========================================================
            # 8. Lấy mặt Interior của Wall2
            # ========================================================

            sideFaces3 = DB.HostObjectUtils.GetSideFaces(
                wall2,
                DB.ShellLayerType.Interior
            )

            if sideFaces3 is None or sideFaces3.Count == 0:
                continue

            interiorReference = sideFaces3[0]

            element3 = doc.GetElement(interiorReference)

            face3 = element3.GetGeometryObjectFromReference(
                interiorReference
            )

            if face3 is None:
                continue

            # Lấy điểm giữa mặt Interior
            bbox3 = face3.GetBoundingBox()

            center_uv3 = (bbox3.Min + bbox3.Max) / 2.0

            source2 = face3.Evaluate(center_uv3)

            # ========================================================
            # 9. Tính khoảng cách
            # ========================================================

            distanceExterior = xyz.DistanceTo(source)

            distanceInterior = xyz.DistanceTo(source2)

            minWallDistance = min(
                distanceExterior,
                distanceInterior
            )

            # ========================================================
            # 10. Kiểm tra Wall này có gần nhất không
            # ========================================================

            if (
                minWallDistance < minDistance
                and minWallDistance <= maxDistance
            ):

                minDistance = minWallDistance

                closestWall = wall2

                # ====================================================
                # Nếu Exterior xa hơn Interior
                # => chọn Interior
                #
                # Ngược lại chọn Exterior
                # ====================================================

                if distanceExterior > distanceInterior:
                    closestReference = exteriorReference
                else:
                    closestReference = interiorReference

        # ============================================================
        # 11. Trả kết quả
        # ============================================================

        return closestWall, closestReference

    def GetClosestWallReference_sua_lai(idoc, wall, shellLayerType):
        """
        Tìm Wall gần nhất và Reference của mặt Exterior/Interior gần Wall đầu vào nhất.

        Parameters
        ----------
        doc : Document
            Revit Document
        wall : Wall
            Wall cần tìm Wall gần nhất
        shellLayerType : ShellLayerType
            DB.ShellLayerType.Exterior hoặc DB.ShellLayerType.Interior

        Returns
        -------
        tuple
            (Wall, Reference)

            Nếu không tìm được:
            (None, None)
        """


        sideFaces = DB.HostObjectUtils.GetSideFaces(
            wall,
            shellLayerType
        )
        
        if sideFaces is None or sideFaces.Count == 0:
            return None, None

        # Reference đầu tiên
        wallRef = sideFaces[0]

        # Lấy Face
        element = idoc.GetElement(wallRef)

        face = element.GetGeometryObjectFromReference(wallRef)
        return wallRef

    from Autodesk.Revit.DB import (
        HostObjectUtils,
        ShellLayerType,
        ReferenceArray,
        Line,
        XYZ,
        UV,
        Face,
        LocationCurve,
        Reference,
        SubTransaction,
        FilteredElementCollector
    )


    def get_wall_references(
            wall,
            check_type,
            wall_type,
            grid=None,
            ext_ref=None,
            int_ref=None):

        reference_array = ReferenceArray()
        reference_list = []

        unique_id = wall.UniqueId

        interior_reference = None
        exterior_reference = None

        distance_interior = 0.0
        distance_exterior = 0.0

        # ============================================================
        # INTERIOR
        # ============================================================

        interior_faces = HostObjectUtils.GetSideFaces(
            wall,
            ShellLayerType.Interior
        )

        for reference in interior_faces:

            if reference is not None and not check_type:

                interior_reference = reference

                if grid is not None and wall_type == "WallThree":

                    curve = grid.Curve
                    source = curve.Evaluate(0.5, True)

                    geometry_object = wall.GetGeometryObjectFromReference(
                        reference
                    )

                    face = geometry_object

                    if face is not None:

                        bounding_box = face.GetBoundingBox()

                        uv = (bounding_box.Min + bounding_box.Max) * 0.5

                        point = face.Evaluate(uv)

                        distance_interior = point.DistanceTo(source)

                else:

                    if int_ref is not None:

                        reference_list.append(int_ref)
                        reference_array.Append(int_ref)

                    else:

                        reference_list.append(reference)
                        reference_array.Append(reference)

            else:

                if wall_type != "WallOne" and wall_type != "WallThree":

                    interior_reference = reference

                    reference_array.Append(reference)
                    reference_list.append(reference)

        # ============================================================
        # EXTERIOR
        # ============================================================

        exterior_faces = HostObjectUtils.GetSideFaces(
            wall,
            ShellLayerType.Exterior
        )

        for reference in exterior_faces:

            if reference is not None and not check_type:

                exterior_reference = reference

                if grid is not None and wall_type == "WallThree":

                    curve = grid.Curve
                    source = curve.Evaluate(0.5, True)

                    element = wall.Document.GetElement(
                        reference.ElementId
                    )

                    face = element.GetGeometryObjectFromReference(
                        reference
                    )

                    if face is not None:

                        bounding_box = face.GetBoundingBox()

                        uv = (bounding_box.Min + bounding_box.Max) * 0.5

                        point = face.Evaluate(uv)

                        distance_exterior = point.DistanceTo(source)

                else:

                    if ext_ref is not None:

                        reference_array.Append(ext_ref)
                        reference_list.append(ext_ref)

                    else:

                        reference_array.Append(reference)
                        reference_list.append(reference)

            else:

                if wall_type != "WallOne" and wall_type != "WallThree":

                    exterior_reference = reference

                    reference_array.Append(reference)
                    reference_list.append(reference)

        # ============================================================
        # CHỌN INTERIOR / EXTERIOR GẦN GRID HƠN
        # ============================================================

        if distance_interior > distance_exterior:

            if int_ref is not None:

                reference_array.Append(int_ref)
                reference_list.append(int_ref)

            else:

                reference_array.Append(interior_reference)
                reference_list.append(interior_reference)

        if distance_interior < distance_exterior:

            if ext_ref is not None:

                reference_array.Append(ext_ref)
                reference_list.append(ext_ref)

            else:

                reference_array.Append(exterior_reference)
                reference_list.append(exterior_reference)

        # ============================================================
        # CHECK TYPE
        # ============================================================

        if check_type:

            compound_structure = wall.WallType.GetCompoundStructure()

            core_width = 0.0
            exterior_width = 0.0
            interior_width = 0.0

            if compound_structure is not None:

                first_core_layer = (
                    compound_structure.GetFirstCoreLayerIndex()
                )

                last_core_layer = (
                    compound_structure.GetLastCoreLayerIndex()
                )

                # Core layers
                for i in range(
                        first_core_layer,
                        last_core_layer + 1):

                    core_width += (
                        compound_structure.GetLayerWidth(i)
                    )

                # Các layer phía trước core
                for i in range(first_core_layer):

                    interior_width += (
                        compound_structure.GetLayerWidth(i)
                    )

                # Các layer phía sau core
                for i in range(
                        last_core_layer + 1,
                        compound_structure.LayerCount):

                    exterior_width += (
                        compound_structure.GetLayerWidth(i)
                    )

            layer_count = (
                wall.WallType
                .GetCompoundStructure()
                .LayerCount
            )

            # ========================================================
            # WallOne / WallThree
            # ========================================================

            if wall_type == "WallOne" or wall_type == "WallThree":

                if layer_count >= 2:

                    reference_array_2 = ReferenceArray()

                    location_curve = wall.Location

                    wall_curve = location_curve.Curve

                    # Đây là phần thay thế GeoVector.GetPerpendicular()
                    if isinstance(wall_curve, Line):

                        direction = wall_curve.Direction

                        perpendicular = XYZ(
                            -direction.Y,
                            direction.X,
                            0
                        ).Normalize()

                        middle_point = wall_curve.Evaluate(
                            0.5,
                            True
                        )

                        line = Line.CreateUnbound(
                            middle_point,
                            perpendicular
                        )

                    dimension_list = []

                    sub_transaction = SubTransaction(
                        wall.Document
                    )

                    found_reference = False

                    for l in range(2, 6):

                        stable_representation = (
                            unique_id +
                            ":-9999:" +
                            str(l)
                        )

                        reference3 = (
                            Reference.ParseFromStableRepresentation(
                                wall.Document,
                                stable_representation
                            )
                        )

                        if reference3 is None:
                            continue

                        reference_array_2.Append(reference3)

                        for m in range(l + 1, 6):

                            stable_representation_2 = (
                                unique_id +
                                ":-9999:" +
                                str(m)
                            )

                            reference4 = (
                                Reference.ParseFromStableRepresentation(
                                    wall.Document,
                                    stable_representation_2
                                )
                            )

                            found_reference = False

                            if reference4 is None:
                                continue

                            reference_array_2.Append(reference4)

                            try:

                                sub_transaction.Start()

                                dimension = (
                                    wall.Document.Create.NewDimension(
                                        wall.Document.ActiveView,
                                        line,
                                        reference_array_2
                                    )
                                )

                                dimension_list.append(dimension)

                                wall.Document.Regenerate()

                                if (
                                    dimension is not None
                                    and abs(
                                        dimension.Value.Value
                                        - core_width
                                    ) > 0.001
                                ):

                                    found_reference = True

                                    sub_transaction.Commit()

                                    break

                                sub_transaction.Commit()

                            except:

                                if sub_transaction.HasStarted:
                                    sub_transaction.RollBack()

                            reference_array_2 = ReferenceArray()
                            reference_array_2.Append(reference3)

                        if found_reference:
                            break

                    if found_reference:

                        for reference in reference_array_2:
                            reference_array.Append(reference)

                        sub_transaction.Start()

                        for dimension in dimension_list:

                            if dimension is not None:

                                wall.Document.Delete(
                                    dimension.Id
                                )

                        sub_transaction.Commit()

            # ========================================================
            # WallTwo
            # ========================================================

            elif wall_type == "WallTwo":

                if layer_count > 1:

                    location_curve = wall.Location
                    wall_curve = location_curve.Curve

                    direction = wall_curve.Direction

                    perpendicular = XYZ(
                        -direction.Y,
                        direction.X,
                        0
                    ).Normalize()

                    middle_point = wall_curve.Evaluate(
                        0.5,
                        True
                    )

                    line = Line.CreateUnbound(
                        middle_point,
                        perpendicular
                    )

                    dimension_list = []

                    found_reference = False

                    reference_array_3 = ReferenceArray()
                    reference_array_4 = ReferenceArray()

                    for ref in reference_list:

                        reference_array_4.Append(ref)

                    for n in range(2, 5):

                        stable_representation = (
                            unique_id +
                            ":-9999:" +
                            str(n)
                        )

                        reference5 = (
                            Reference.ParseFromStableRepresentation(
                                wall.Document,
                                stable_representation
                            )
                        )

                        if reference5 is None:
                            continue

                        dimension_failed = False

                        reference_array.Append(reference5)
                        reference_list.append(reference5)

                        sub_transaction = SubTransaction(
                            wall.Document
                        )

                        try:

                            sub_transaction.Start()

                            dimension = (
                                wall.Document.Create.NewDimension(
                                    wall.Document.ActiveView,
                                    line,
                                    reference_array
                                )
                            )

                            if dimension is not None:

                                invalid_dimension = False

                                if dimension.Segments.Size > 0:

                                    for segment in dimension.Segments:

                                        value = segment.Value.Value

                                        if value <= 0:

                                            dimension_failed = True
                                            raise Exception(
                                                "Invalid dimension"
                                            )

                                        if (
                                            (
                                                abs(value - interior_width)
                                                > 0.001
                                                and abs(interior_width)
                                                < 0.001
                                            )
                                            or
                                            (
                                                abs(value - exterior_width)
                                                > 0.001
                                                and abs(exterior_width)
                                                < 0.001
                                            )
                                        ):

                                            invalid_dimension = True

                                else:

                                    value = dimension.Value.Value

                                    if (
                                        (
                                            abs(value - interior_width)
                                            > 0.001
                                            and abs(interior_width)
                                            < 0.001
                                        )
                                        or
                                        (
                                            abs(value - exterior_width)
                                            > 0.001
                                            and abs(exterior_width)
                                            < 0.001
                                        )
                                    ):

                                        invalid_dimension = True

                                if invalid_dimension:

                                    reference_list.remove(
                                        reference5
                                    )

                                    reference_array = ReferenceArray()

                                    for ref in reference_list:
                                        reference_array.Append(ref)

                                    reference_array_3.Append(
                                        reference5
                                    )

                                    found_reference = True

                                    if sub_transaction.HasStarted:
                                        sub_transaction.RollBack()

                                else:

                                    dimension_failed = True

                                    if sub_transaction.HasStarted:
                                        sub_transaction.RollBack()

                        except:

                            if sub_transaction.HasStarted:
                                sub_transaction.RollBack()

                            dimension_failed = True

                        if dimension_failed:

                            if reference5 in reference_list:
                                reference_list.remove(
                                    reference5
                                )

                            reference_array = ReferenceArray()

                            for ref in reference_list:
                                reference_array.Append(ref)

                    if found_reference:

                        reference_array = ReferenceArray()

                        for ref in reference_array_3:

                            reference_list.append(ref)

                    reference_array = ReferenceArray()

                    for ref in reference_list:
                        reference_array.Append(ref)

            # ========================================================
            # Các Wall type còn lại
            # ========================================================

            else:

                for i in range(2, layer_count + 1):

                    stable_representation = (
                        unique_id +
                        ":-9999:" +
                        str(i)
                    )

                    reference6 = (
                        Reference.ParseFromStableRepresentation(
                            wall.Document,
                            stable_representation
                        )
                    )

                    if reference6 is not None:
                        reference_array.Append(reference6)

        return reference_array














    def get_wall_references_lam_lai(wall,check_type):

        reference_array = ReferenceArray()
        reference_list = []

        unique_id = wall.UniqueId

        if check_type:

            compound_structure = wall.WallType.GetCompoundStructure()

            core_width = 0.0
            exterior_width = 0.0
            interior_width = 0.0

            if compound_structure is not None:

                first_core_layer = (
                    compound_structure.GetFirstCoreLayerIndex()
                )

                last_core_layer = (
                    compound_structure.GetLastCoreLayerIndex()
                )

                # Core layers
                for i in range(
                        first_core_layer,
                        last_core_layer + 1):

                    core_width += (
                        compound_structure.GetLayerWidth(i)
                    )

                # Các layer phía trước core
                for i in range(first_core_layer):

                    interior_width += (
                        compound_structure.GetLayerWidth(i)
                    )

                # Các layer phía sau core
                for i in range(
                        last_core_layer + 1,
                        compound_structure.LayerCount):

                    exterior_width += (
                        compound_structure.GetLayerWidth(i)
                    )

        layer_count = (wall.WallType.GetCompoundStructure().LayerCount)

        if layer_count > 1:

            location_curve = wall.Location
            wall_curve = location_curve.Curve

            direction = wall_curve.Direction

            perpendicular = XYZ(-direction.Y,direction.X,0).Normalize()

            middle_point = wall_curve.Evaluate(0.5,True)

            line = Line.CreateUnbound(middle_point,perpendicular)

            dimension_list = []

            found_reference = False

            reference_array_3 = ReferenceArray()
            reference_array_4 = ReferenceArray()

            # for ref in reference_list:

            #     reference_array_4.Append(ref)

            for n in range(2, 5):

                stable_representation = (unique_id +":-9999:" +str(n))

                reference5 = (Reference.ParseFromStableRepresentation(wall.Document,stable_representation))

                if reference5 is None:
                    continue

                dimension_failed = False

                reference_array.Append(reference5)
                reference_list.append(reference5)
                try:
                    sub_transaction = SubTransaction(wall.Document)

                    sub_transaction.Start()

                    dimension = (
                        wall.Document.Create.NewDimension(
                            wall.Document.ActiveView,
                            line,
                            reference_array
                        )
                    )
                    if dimension is not None:

                        invalid_dimension = False

                        if dimension.Segments.Size > 0:

                            for segment in dimension.Segments:

                                value = segment.Value.Value

                                if value <= 0:

                                    dimension_failed = True
                                    raise Exception(
                                        "Invalid dimension"
                                    )

                                if (
                                    (
                                        abs(value - interior_width)
                                        > 0.001
                                        and abs(interior_width)
                                        < 0.001
                                    )
                                    or
                                    (
                                        abs(value - exterior_width)
                                        > 0.001
                                        and abs(exterior_width)
                                        < 0.001
                                    )
                                ):

                                    invalid_dimension = True

                        else:

                            value = dimension.Value.Value

                            if (
                                (
                                    abs(value - interior_width)
                                    > 0.001
                                    and abs(interior_width)
                                    < 0.001
                                )
                                or
                                (
                                    abs(value - exterior_width)
                                    > 0.001
                                    and abs(exterior_width)
                                    < 0.001
                                )
                            ):

                                invalid_dimension = True

                        if invalid_dimension:

                            reference_list.remove(
                                reference5
                            )

                            reference_array = ReferenceArray()

                            for ref in reference_list:
                                reference_array.Append(ref)

                            reference_array_3.Append(
                                reference5
                            )

                            found_reference = True

                            if sub_transaction.HasStarted:
                                sub_transaction.RollBack()

                        else:

                            dimension_failed = True

                            if sub_transaction.HasStarted:
                                sub_transaction.RollBack()

                except:

                    if sub_transaction.HasStarted:
                        sub_transaction.RollBack()

                    dimension_failed = True

                if dimension_failed:

                    if reference5 in reference_list:
                        reference_list.remove(
                            reference5
                        )

                    reference_array = ReferenceArray()

                    for ref in reference_list:
                        reference_array.Append(ref)


            if found_reference:

                reference_array = ReferenceArray()

                for ref in reference_array_3:

                    reference_list.append(ref)

            reference_array = ReferenceArray()

            for ref in reference_list:
                reference_array.Append(ref)

    # ========================================================
    # Các Wall type còn lại
    # ========================================================

        else:

            for i in range(2, layer_count + 1):

                stable_representation = (
                    unique_id +
                    ":-9999:" +
                    str(i)
                )

                reference6 = (
                    Reference.ParseFromStableRepresentation(
                        wall.Document,
                        stable_representation
                    )
                )

                if reference6 is not None:
                    reference_array.Append(reference6)

        return reference_array


    def get_wall_reference_by_magic(uid,index):
        format = "{0}:{1}:{2}"
        nine = -9999
        refString = str.Format(format,uid,nine,index)
        return refString
    
    Ele = module.get_elements(uidoc,doc, "Select Walls", noti = False)
    # for tung_wall in Ele:
    #     t = Transaction(doc,"Dimension wall (face to face)")
    #     t.Start()
    # #     get_wall_reference = GetClosestWallReference_sua_lai(doc, tung_wall, ShellLayerType.Exterior)
    #     # print get_wall_reference, dir(get_wall_reference)
    #     # for tung_ref in get_wall_reference:
    #     #     print tung_ref
    #     test_ham= get_wall_references_lam_lai(tung_wall,check_type = True)
    #     print test_ham
    #     t.Commit()

    # trans_group = TransactionGroup(doc, 'Dim Thickness of Wall')
    # trans_group.Start()
    if Ele:
        list_new_dim = []

        for wall in Ele:

            t = Transaction(doc,"Dimension wall (face to face)")
            t.Start()
            # try:
            geo = (get_geometry(wall))
            faces = get_face(geo)
            center_plane = get_center_plane(wall)
            center_plane_normal = center_plane.Normal
            list_distance = []
            list_outer_face = []
            call_class_tim_reference = tim_reference_beam.ClassTimReference(faces,center_plane, vectortransform)                
            result = call_class_tim_reference.tim_reference_beam()
            ref_face_min = result.ref_face_min
            ref_face_max = result.ref_face_max
            max_value = result.max_value

            detail_line = get_rotate_90_location_wall_center (wall)
            line = detail_line.Location.Curve
            wall_reference = ReferenceArray()
            unique_id = wall.UniqueId
            string_face_3 = get_wall_reference_by_magic(unique_id,4)
            ref_3 = Reference.ParseFromStableRepresentation(doc,string_face_3)
            wall_reference.Append(ref_3)

            get_wall_reference_exterior = GetClosestWallReference_sua_lai(doc, wall, ShellLayerType.Exterior)
            get_wall_reference_interior = GetClosestWallReference_sua_lai(doc, wall, ShellLayerType.Interior)
            wall_reference.Append(get_wall_reference_exterior)
            wall_reference.Append(get_wall_reference_interior)
            test_ham= get_wall_references_lam_lai(wall,check_type = True)
            print dir(test_ham)
            # wall_reference.Append(ref_face_min)
            # wall_reference.Append(ref_face_max)
            # dim = doc.Create.NewDimension(Currentview, line, test_ham)
            # print dim
            # list_new_dim.append(dim)
            # delete_detail_curve = doc.Delete(detail_line.Id)
            t.Commit()
            # except:
            #     t.RollBack()
            #     pass
    # trans_group.Assimilate()