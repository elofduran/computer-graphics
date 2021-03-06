# CENG 487 Assignment3 by
# CENG 487 Assignment4 by
# Elif Duran
# StudentId: 230201002
# December 2019

from hcoordinates import Position, Vec3d
from operations.mat3d import Mat3d


class Operations:

    def __init__(self, position, rotation, translation):
        self.position = position
        self.rotation = rotation
        self.translation = translation
        self.last_matrix = Mat3d.identity_matrix()

    def apply_stack(self, matrix):
        self.last_matrix = self.last_matrix.mat_multiplication(matrix)

    def rotate_x(self, angle):
        self.rotation.x += angle
        self.apply_stack(Mat3d.rotate_x(angle))

    def rotate_y(self, angle):
        self.rotation.y += angle
        self.apply_stack(Mat3d.rotate_x(angle))

    def rotate_z(self, angle):
        self.rotation.z += angle
        self.apply_stack(Mat3d.rotate_x(angle))

    def translate(self, x, y, z):
        self.position.add(Position(x, y, z))
        self.apply_stack(Mat3d.translation_matrix(Vec3d(x, y, z)))

# can be added scale operation too
# this class applies matrix stack to the object at once
# before that I was multiply the object with the matrices
# now all the operations multiplied with the identity matrix at first

