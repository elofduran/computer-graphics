# CENG 487 Assignment4 by
# Elif Duran
# StudentId: 230201002
# December 2019


import random
from functools import reduce
from OpenGL.GL import *


# Reference: https://rosettacode.org/wiki/Catmull%E2%80%93Clark_subdivision_surface#Python
from hcoordinates import HCoordinates, Vec3d
from operations.mat3d import Mat3d


class Object:

    def __init__(self, name, vertices, faces):
        self.name = name
        self.vertices = vertices
        self.faces = faces
        self.colors = []
        self.operation = Mat3d()
        self.wireOnShaded = False
        self.wireWidth = 2
        self.wireOnShadedColor = HCoordinates(1.0, 1.0, 1.0, 1.0)

    def apply_operation(self, mat3d):
        for i, vertex in enumerate(self.vertices):
            self.vertices[i] = mat3d.multiply_vec(vertex)

    def draw(self, camera):
        index = 0
        for face in self.faces:

            if self.wireOnShaded:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                glLineWidth(self.wireWidth)

                glBegin(GL_POLYGON)
                glColor3f(self.wireOnShadedColor[0], self.wireOnShadedColor[1], self.wireOnShadedColor[2])
                for vertex in range(len(face)):
                    glVertex3f(self.vertices[vertex].x, self.vertices[vertex].y, self.vertices[vertex].z)
                glEnd()

                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            else:
                glBegin(GL_POLYGON)
                if len(self.colors) > 0:
                    glColor3f(self.colors[index].x, self.colors[index].y, self.colors[index].z)
                else:
                    glColor3f(1.0, 2.6, 0.0)

                for vertex in face:
                    glVertex3f(self.vertices[vertex].x, self.vertices[vertex].y, self.vertices[vertex].z)
                glEnd()

            index += 1

            glLineWidth(2.5)
            glBegin(GL_LINE_LOOP)
            glColor3f(.3, .3, .3)
            for vertex in face:
                glVertex3f(self.vertices[vertex].x, self.vertices[vertex].y, self.vertices[vertex].z)
            glEnd()


    def subdivide(self):
        """
        self.vertices = [ Point3f(1.0, 1.0, 1.0), ...]
        self.faces = [ [0, 2, 3, 1], ...]

        references:
        - https://en.wikipedia.org/wiki/Catmull%E2%80%93Clark_subdivision_surface
        - http://www.rorydriscoll.com/2008/08/01/catmull-clark-subdivision-the-basics/
        - https://rosettacode.org/wiki/Catmull%E2%80%93Clark_subdivision_surface
        - https://www.algosome.com/articles/catmull-clark-subdivision-algorithm.html
        """
        vertices = self.vertices.copy()
        faces = self.faces.copy()

        # 1. face points
        facePoints = [reduce(lambda v1, v2: v1.add(v2), map(lambda idx: self.vertices[idx], face)) * (1.0 / len(face)) for
                      face in faces]

        # 2. find edges
        edges = []

        # get edges from each face
        for faceIndex in range(len(faces)):
            face = faces[faceIndex]
            faceLength = len(face)

            for pointNumIndex in range(faceLength):
                # if not last point then edge is curr point and next point, else edge is curr point and first point
                pointNum1 = face[pointNumIndex]
                pointNum2 = face[pointNumIndex + 1 if (pointNumIndex < faceLength - 1) else 0]

                # order points in edge by lowest point number
                if pointNum1 > pointNum2:
                    pointNum1, pointNum2 = pointNum2, pointNum1

                edges.append([pointNum1, pointNum2, faceIndex])

        # sort edges by pointNum1, pointNum2, faceIndex
        edges = sorted(edges)

        # merge edges with 2 adjacent faces
        # [pointNum1, pointNum2, faceIndex1, faceIndex2]
        mergedEdges = []

        i = int(len(edges) / 2)
        for edgeIndex in range(i):
            edge1 = edges[2 * edgeIndex]
            edge2 = edges[2 * edgeIndex + 1]
            mergedEdges.append([edge1[0], edge1[1], edge1[2], edge2[2]])

        # add edge centers
        # [pointNum1, pointNum2, faceIndex1, faceIndex2, centerPoint]
        edgesCenters = []

        for mergedEdge in mergedEdges:
            point1 = vertices[mergedEdge[0]]
            point2 = vertices[mergedEdge[1]]
            centerPoint = (point1.add(point2)) * 0.5
            edgesCenters.append(mergedEdge + [centerPoint])

        # 3. edge points
        edgePoints = []

        for edgeFace in edgesCenters:
            # get center of edge
            centerEdgePoint = edgeFace[4]
            # get center of two facepoints
            facePoint1 = facePoints[edgeFace[2]]
            facePoint2 = facePoints[edgeFace[3]]
            centerFacePoint = (facePoint1.add(facePoint2)) * 0.5
            # get average between center of edge and center of facepoints
            edgePoint = (centerEdgePoint.add(centerFacePoint)) * 0.5
            edgePoints.append(edgePoint)

        # 4. new vertices

        # 4.1 average face points
        # the average of the face points of the faces the point belongs to (avg_face_points)
        tempPoints = []  # [[Point3f(0.0, 0.0, 0.0), 0], ...]
        averageFacePoints = []  # [Point3f(0.0, 0.0, 0.0), ...]
        for pointIndex in range(len(vertices)):
            tempPoints.append([HCoordinates(0.0, 0.0, 0.0, 0.0), 0])

        # loop through faces updating tempPoints
        for faceIndex in range(len(faces)):
            for pointIndex in faces[faceIndex]:
                tempPoints[pointIndex][0] = tempPoints[pointIndex][0].add(facePoints[faceIndex])
                tempPoints[pointIndex][1] += 1

        # divide to create avg_face_points
        for tempPoint in tempPoints:
            averageFacePoints.append(tempPoint[0] * (1.0 / tempPoint[1]))

        # 4.2 average mid edges
        # the average of the centers of edges the point belongs to (avg_mid_edges)
        tempPoints = []  # [[Point3f(0.0, 0.0, 0.0), 0], ...]
        averageMidEdges = []  # [Point3f(0.0, 0.0, 0.0), ...]
        for pointIndex in range(len(vertices)):
            tempPoints.append([HCoordinates(0.0, 0.0, 0.0, 0.0), 0])

        # go through edgesCenters using center updating each point
        for edge in edgesCenters:
            for pointIndex in [edge[0], edge[1]]:
                tempPoints[pointIndex][0] = tempPoints[pointIndex][0].add(edge[4])
                tempPoints[pointIndex][1] += 1

        # divide out number of points to get average
        for tempPoint in tempPoints:
            averageMidEdges.append(tempPoint[0] * (1.0 / tempPoint[1]))

        # 4.3 point faces
        # how many faces a point belongs to
        pointsFaces = []

        for pointIndex in range(len(vertices)):
            pointsFaces.append(0)

        # loop through faces updating pointsFaces
        for faceIndex in range(len(faces)):
            for pointIndex in faces[faceIndex]:
                pointsFaces[pointIndex] += 1

        # 4.4 new vertices with barycenter
        """
        m1 = (n - 3) / n
        m2 = 1 / n
        m3 = 2 / n
        newCoords = (m1 * oldCoords) + (m2 * averageFacePoints) + (m3 * averageMidEdges)
        """
        newVertices = []

        for pointIndex in range(len(vertices)):
            n = pointsFaces[pointIndex]
            m1 = (n - 3.0) / n
            m2 = 1.0 / n
            m3 = 2.0 / n
            newCoords1 = (vertices[pointIndex].scale(m1)).add((averageFacePoints[pointIndex].scale(m2)))
            newCoords = newCoords1.add(averageMidEdges[pointIndex].scale(m3))
            newVertices.append(newCoords)

        # 4.5 add face points to newVertices
        facePointIndices = []
        edgePointIndices = dict()
        nextPointIndex = len(newVertices)

        # point num after next append to newVertices
        for facePoint in facePoints:
            newVertices.append(facePoint)
            facePointIndices.append(nextPointIndex)
            nextPointIndex += 1

        # add edge points to newPoints
        for edgeIndex in range(len(edgesCenters)):
            pointIndex1 = edgesCenters[edgeIndex][0]
            pointIndex2 = edgesCenters[edgeIndex][1]
            edgePoint = edgePoints[edgeIndex]
            newVertices.append(edgePoint)
            edgePointIndices[(pointIndex1, pointIndex2)] = nextPointIndex
            nextPointIndex += 1

        # 5. new faces
        # newVertices now has the points to output. Need new faces
        newFaces = []

        for oldFaceIndex in range(len(faces)):
            oldFace = faces[oldFaceIndex]
            # 4 point face
            if len(oldFace) == 4:
                # old vertices
                a = oldFace[0]
                b = oldFace[1]
                c = oldFace[2]
                d = oldFace[3]
                # create face point and edges
                facePoint_abcd = facePointIndices[oldFaceIndex]
                edge_point_ab = edgePointIndices[self.sortIndices((a, b))]
                edge_point_da = edgePointIndices[self.sortIndices((d, a))]
                edge_point_bc = edgePointIndices[self.sortIndices((b, c))]
                edge_point_cd = edgePointIndices[self.sortIndices((c, d))]
                # add new faces
                newFaces.append((a, edge_point_ab, facePoint_abcd, edge_point_da))
                newFaces.append((b, edge_point_bc, facePoint_abcd, edge_point_ab))
                newFaces.append((c, edge_point_cd, facePoint_abcd, edge_point_bc))
                newFaces.append((d, edge_point_da, facePoint_abcd, edge_point_cd))
            else:
                raise Exception("face is broken!")

        # 6. assign new shape
        self.vertices = newVertices
        self.faces = newFaces
        self.colors = []
        for i in range(0, len(newFaces) + 1):
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)
            self.colors.append(HCoordinates(r, g, b, 1.0))

    def sortIndices(self, indices):
        return indices if indices[0] < indices[1] else (indices[1], indices[0])

