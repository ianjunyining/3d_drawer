import src.geometry as geo
import src.transformation as trans
import turtle, math
import numpy as np

class NotImplemented(Exception):
    pass

class Shape():
    def __init__(self, pen: turtle.Turtle, transformation: trans.Transformation) -> None:
        self.selected = False
        self.pen = pen
        self.sr = 5
        self.transformation = transformation
        self.copy_delta = (10, 0, 0)
        if pen:
            self.pen.hideturtle()

    def _type(self):
        return self.__class__.__name__
    
    def set_selected(self, selected):
        self.selected = selected

    def get_selected(self):
        return self.selected
    
    def draw(self):
        pass

    def _draw_ploygon(self, points, color=None):
        if color:
            old_color, _ = self.pen.color()
            self.pen.color(color)
        self.pen.penup()
        self.pen.goto(points[-1])
        self.pen.pendown()
        for pt in points:
            self.pen.goto(pt)
        self.pen.penup()
        if color:
            self.pen.color(old_color)

    def _draw_line_segs(self, points, color=None):
        if color:
            old_color, _ = self.pen.color()
            self.pen.color(color)
        self.pen.penup()
        self.pen.goto(points[0])
        self.pen.pendown()
        for pt in points[1:]:
            self.pen.goto(pt)
        self.pen.penup()
        if color:
            self.pen.color(old_color)

    def get_selection_points(self):
        raise NotImplemented(f"{self._type()}: get_selection_points() is not implemented")

    def draw_selection_points(self):
        for point in self.get_selection_points():
            self.pen.penup()
            self.pen.goto(point[0], point[1] - self.sr/2)
            self.pen.pendown()
            self.pen.circle(self.sr)
            self.pen.penup()

    def clear(self):
        self.pen.clear()

    def get_center(self):
        raise NotImplemented(f"{self._type()}: get_center() is not implemented")
        
    def point_in_shape(self, point):
        raise NotImplemented(f"{self._type()}: point_in_shape() is not implemented")
    
    # delta: (dx, dy)
    def translate(self, delta):
        raise NotImplemented(f"{self._type()}: translate() is not implemented")

    # rotate around center.
    # if center is None, rotate round the shape center
    def rotate(self, theta, center=None):
        raise NotImplemented(f"{self._type()}: rotate() is not implemented")

    def scale(self, s, center=None):
        raise NotImplemented(f"{self._type()}: scale() is not implemented")
    
    def clone_pen(self):
        pen = turtle.Turtle()
        pen.color(self.pen.color()[0])
        return pen

    def clone(self):
        return NotImplemented(f"{self._type()}: scale() is not implemented")
    
class Line(Shape):
    def __init__(self, pen: turtle.Turtle, transformation: trans.Transformation, point3d1, point3d2) -> None:
        super().__init__(pen, transformation)
        self.points3D = [point3d1, point3d2]
        self.points2D = []

    def draw(self):
        self.clear()
        self.points2D = self.transformation.project_3d_to_2d(self.points3D)
        self._draw_line_segs(self.points2D)
        self.pen.penup()
        if self.selected:
            self.draw_selection_points()

    def get_selection_points(self):
        return [self.point2d1, self.point2d2]
    
    def point_in_shape(self, point):
        return geo.distance_point_to_segment(self.point1, self.point2, point) <= 5
    
    def translate(self, delta):
        self.point1 = geo.translate(self.point1, delta)
        self.point2 = geo.translate(self.point2, delta)

    def rotate(self, theta, center=None):
        rotate_center = center if center else self.get_center()
        self.point1 = geo.rotate(self.point1, theta, rotate_center)
        self.point2 = geo.rotate(self.point2, theta, rotate_center)

    def get_center(self):
        center = (
            (self.point1[0] + self.point2[0]) / 2,
            (self.point1[1] + self.point2[1]) / 2,
        )
        return center
    
    def scale(self, s, center=None):
        s_center = center if center else self.get_center()
        self.point1 = geo.scale(s, s_center, self.point1)
        self.point2 = geo.scale(s, s_center, self.point2)
    
    def clone(self):
        return Line(self.clone_pen(), geo.translate(self.point1, self.copy_delta), geo.translate(self.point2, self.copy_delta))
    
    
class Cube(Shape):
    def __init__(self, pen: turtle.Turtle, transformation: trans.Transformation, s, center=[0, 0, 0]) -> None:
        super().__init__(pen, transformation)
        self.s = s
        self.center = center
        self.points2D = []
        self.points3D = [
            [self.center[0], self.center[1], self.center[2], 1],
            [self.s + self.center[0], self.center[1], self.center[2], 1],
            [self.s + self.center[0], self.s + self.center[1], self.center[2], 1],
            [self.center[0], self.s + self.center[1], self.center[2], 1],
            [self.center[0], self.center[1], self.s + self.center[2], 1],
            [self.s + self.center[0], self.center[1], self.s + self.center[2], 1],
            [self.s + self.center[0], self.s + self.center[1], self.s + self.center[2], 1],
            [self.center[0], self.s + self.center[1], self.s + self.center[2], 1],
        ]

    def project(self):
        self.points2D = self.transformation.project_3d_to_2d(self.points3D)

    def draw(self):
        self.clear()
        self.project()
        self._draw_ploygon(self.points2D[:4])
        self._draw_ploygon(self.points2D[4:])
        for i in range(4):
            self._draw_line_segs([self.points2D[i], self.points2D[i + 4]])
        if self.selected:
            self.draw_selection_points()

    def get_selection_points(self):
        return  self.points2D
    
    def point_in_shape(self, point):
        min_x, max_x, min_y, max_y = geo.points_boundary(self.points2D)
        return geo.point_in_boundary(min_x, max_x, min_y, max_y, point)
    
    def translate(self, delta):
        self.points3D = geo.translate_points_3D(self.points3D, delta)

    def rotate(self, theta, center=None):
        rotate_center = center if center else self.get_center()
        self.point1 = geo.rotate(self.point1, theta, rotate_center)
        self.point2 = geo.rotate(self.point2, theta, rotate_center)

    def get_center(self):
        center = (
            (self.point1[0] + self.point2[0]) / 2,
            (self.point1[1] + self.point2[1]) / 2,
        )
        return center
    
    def scale(self, s, center=None):
        s_center = center if center else self.get_center()
        self.point1 = geo.scale(s, s_center, self.point1)
        self.point2 = geo.scale(s, s_center, self.point2)
    
    def clone(self):
        return Line(self.clone_pen(), geo.translate(self.point1, self.copy_delta), geo.translate(self.point2, self.copy_delta))
    

class WorldCoord(Shape):
    def __init__(self, pen: turtle.Turtle, transformation: trans.Transformation, s) -> None:
        super().__init__(pen, transformation)
        self.s = s
        self.points2D = []
        self.points3D = [(0, 0, 0, 1), (s, 0, 0, 1), (0, s, 0, 1), (0, 0, s, 1)]

    def draw(self):
        self.clear()
        self.points2D = self.transformation.project_3d_to_2d(self.points3D)
        self._draw_line_segs([self.points2D[0], self.points2D[1]], 'red')
        self._draw_line_segs([self.points2D[0], self.points2D[2]], 'green')
        self._draw_line_segs([self.points2D[0], self.points2D[3]], 'blue')

    def point_in_shape(self, point):
        return False