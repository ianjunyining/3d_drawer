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
        self.copy_delta = (100, 100, 100)
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
        return self.points2D
    
    def point_in_shape(self, point):
        return geo.distance_point_to_segment(self.points2D[0], self.points2D[1], point) <= 5
    
    def translate(self, delta):
        self.points3D = geo.translate_points_3D(self.points3D, delta)

    def rotate(self, delta, center):
        self.points3D = geo.rotate_3D(self.points3D, delta, center)

    def get_center(self):
        return geo.avg_points3D(self.points3D)
    
    def scale(self, s, center=None):
        s_center = center if center else self.get_center()
        self.point1 = geo.scale(s, s_center, self.point1)
        self.point2 = geo.scale(s, s_center, self.point2)
    
    def clone(self):
        return Line(self.clone_pen(), geo.translate(self.point1, self.copy_delta), geo.translate(self.point2, self.copy_delta))
    
    
class Cube(Shape):
    def __init__(self, pen: turtle.Turtle, transformation: trans.Transformation, s, center=[0, 0, 0]) -> None:
        super().__init__(pen, transformation)
        self.points2D = []
        self.points3D = [
            [0, 0, 0, 1],
            [s, 0, 0, 1],
            [s, s, 0, 1],
            [0, s, 0, 1],
            [0, 0, s, 1],
            [s, 0, s, 1],
            [s, s, s, 1],
            [0, s, s, 1],
        ]
        self.translate(geo.add_vec(center, (-s/2, -s/2, -s/2)))

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

    def rotate(self, delta, center=None):
        self.points3D = geo.rotate_3D(self.points3D, delta, center)

    def get_center(self):
        return geo.avg_points3D(self.points3D)
    
    def scale(self, s, center=None):
        s_center = center if center else self.get_center()
        self.point1 = geo.scale(s, s_center, self.point1)
        self.point2 = geo.scale(s, s_center, self.point2)
    
    def clone(self):
        cube = Cube(self.clone_pen(), self.transformation, 0)
        cube.points3D = geo.translate_points_3D(self.points3D, self.copy_delta)
        return cube
    

class Pyramid(Shape):
    def __init__(self, pen: turtle.Turtle, transformation: trans.Transformation, s, center=[0, 0, 0]) -> None:
        super().__init__(pen, transformation)
        self.points3D = [
            [0, 0, 0, 1],
            [s, 0, 0, 1],
            [s, s, 0, 1],
            [0, s, 0, 1],
            [s/2, s/2, s, 1],
        ]
        self.translate(geo.add_vec(center, (-s/2, -s/2, -s/2)))

    def project(self):
        self.points2D = self.transformation.project_3d_to_2d(self.points3D)

    def draw(self):
        self.clear()
        self.project()
        self._draw_ploygon(self.points2D[:4])
        for i in range(4):
            self._draw_line_segs([self.points2D[i], self.points2D[-1]])
        if self.selected:
            self.draw_selection_points()

    def get_selection_points(self):
        return  self.points2D
    
    def point_in_shape(self, point):
        min_x, max_x, min_y, max_y = geo.points_boundary(self.points2D)
        return geo.point_in_boundary(min_x, max_x, min_y, max_y, point)
    
    def translate(self, delta):
        self.points3D = geo.translate_points_3D(self.points3D, delta)

    def rotate(self, delta, center=None):
        self.points3D = geo.rotate_3D(self.points3D, delta, center)

    def get_center(self):
        return geo.avg_points3D(self.points3D)
    
    def scale(self, s, center=None):
        s_center = center if center else self.get_center()
        self.point1 = geo.scale(s, s_center, self.point1)
        self.point2 = geo.scale(s, s_center, self.point2)
    
    def clone(self):
        pyramid = Pyramid(self.clone_pen(), self.transformation, 0)
        pyramid.points3D = geo.translate_points_3D(self.points3D, self.copy_delta)
        return pyramid


class Circle(Shape):
    def __init__(self, pen: turtle.Turtle, transformation: trans.Transformation, r, center=[0, 0, 0]) -> None:
        super().__init__(pen, transformation)
        n = 72
        theta = 2 * math.pi / n
        self.points3D = []
        for i in range(n):
            self.points3D.append([r * math.cos(i * theta), r * math.sin(i * theta), 0, 1])
        self.translate(center)

    def project(self):
        self.points2D = self.transformation.project_3d_to_2d(self.points3D)

    def draw(self):
        self.clear()
        self.project()
        self._draw_ploygon(self.points2D)
        if self.selected:
            self.draw_selection_points()

    def get_selection_points(self):
        return  self.points2D
    
    def point_in_shape(self, point):
        min_x, max_x, min_y, max_y = geo.points_boundary(self.points2D)
        return geo.point_in_boundary(min_x, max_x, min_y, max_y, point)
    
    def translate(self, delta):
        self.points3D = geo.translate_points_3D(self.points3D, delta)

    def rotate(self, delta, center=None):
        self.points3D = geo.rotate_3D(self.points3D, delta, center)

    def get_center(self):
        return geo.avg_points3D(self.points3D)
    
    def scale(self, s, center=None):
        s_center = center if center else self.get_center()
        self.point1 = geo.scale(s, s_center, self.point1)
        self.point2 = geo.scale(s, s_center, self.point2)
    
    def clone(self):
        circle = Circle(self.clone_pen(), self.transformation, 0)
        circle.points3D = geo.translate_points_3D(self.points3D, self.copy_delta)
        return circle


class CombinedShape(Shape):
    def __init__(self, pen: turtle.Turtle, transformation: trans.Transformation, shapes) -> None:
        super().__init__(pen, transformation)
        self.shapes = shapes

    def draw(self):
        self.clear()
        for shape in self.shapes:
            shape.draw()
    
    def set_selected(self, selected):
        self.selected = selected
        for shape in self.shapes:
            shape.set_selected(selected)

    def clear(self):
        for shape in self.shapes:
            shape.clear()

    def get_selection_points(self):
        points = []
        for shape in self.shapes:
            points.extend(shape.get_selection_points())
        return points

    def get_center(self):
        centers = [shape.get_center() for shape in self.shapes]
        return geo.avg_points3D(centers)
    
    def translate(self, delta):
        for shape in self.shapes:
            shape.translate(delta)

    def rotate(self, delta, center=None):
        r_center = center if center else self.get_center()
        for shape in self.shapes:
            shape.rotate(delta, r_center)

    def point_in_shape(self, point):
        for shape in self.shapes:
            if shape.point_in_shape(point):
                return True
        return False
    
    def clone(self):
        shapes = []
        for shape in self.shapes:
            shapes.append(shape.clone())
        return CombinedShape(None, self.transformation, shapes)



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