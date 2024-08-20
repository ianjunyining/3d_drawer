import turtle
from src.shape import *
import src.transformation as trans

class Canvas():
    def __init__(self) -> None:
        self.transformation = trans.Transformation(f=1000, r=(math.pi / 4, math.pi / 4, math.pi / 4), t=(0, 0, 5000))
        self.shapes = []

    def reset_3dview(self):
        self.transformation.reset()
        self.draw()

    def draw(self):
        for shape in self.shapes:
            shape.draw()
        
    def select_shapes(self, point, shift_pressed):
        for shape in self.shapes:
            selected_old = shape.get_selected()
            if selected_old and shift_pressed:
                continue
            selected_new = shape.point_in_shape(point)
            shape.set_selected(selected_new)
            if selected_old != selected_new:
                shape.draw()

    def delete_selected(self):
        old_shapes = self.shapes
        self.shapes = []
        for shape in old_shapes:
            if shape.get_selected():
                shape.clear()
            else:
                self.shapes.append(shape)

    def delete_all(self):  
        for shape in self.shapes:
            shape.clear()
        self.shapes = []

    def deselect_all(self):
        for shape in self.shapes:
            if shape.get_selected():
                shape.set_selected(False)
                shape.draw()

    # delta: (dx, dy)
    def translate_selected(self, delta):
        for shape in self.shapes:
            if shape.get_selected():
                shape.translate(delta)
                shape.draw()
    
    # if only one shape is selected, rotate around the center of the selected shape
    # otherwise, compute the center from the selection points of all selected shapes, 
    # and rotate all selected shapes around this center.
    def rotate_selected(self, theta):
        all_centers = [shape.get_center() for shape in self.shapes if shape.get_selected()]
        if len(all_centers) == 0:
            return
        center = geo.avg_points(all_centers)
        for shape in self.shapes:
            if shape.get_selected():
                shape.rotate(theta, center)
                shape.draw()

    def scale_selected(self, s):
        all_centers = [shape.get_center() for shape in self.shapes if shape.get_selected()]
        if len(all_centers) == 0:
            return
        center = geo.avg_points(all_centers)
        for shape in self.shapes:
            if shape.get_selected():
                shape.scale(s, center)
                shape.draw()
    
    def combine_selected(self):
        old_shapes = self.shapes
        self.shapes = []
        selected_shapes = []
        for shape in old_shapes:
            if shape.get_selected():
                selected_shapes.append(shape)
            else:
                self.shapes.append(shape)
        combined_shape = CombinedShape(turtle.Turtle(), selected_shapes)
        combined_shape.set_selected(True)
        self.shapes.append(combined_shape)

    def copy_selected(self):
        temp_shapes = []
        for shape in self.shapes:
            if shape.get_selected():
                clone = shape.clone()
                print(clone.get_selected())
                clone.set_selected(True)
                shape.set_selected(False)
                temp_shapes.append(clone)
                clone.draw()
                shape.draw()
        self.shapes.extend(temp_shapes)

    def create_customized_arts(self, name):
        # self.delete_all()

        arts_map = {
            "fractal_triangle": FractalTriangle,
            "cube": Cube,
        }

        if name in arts_map:
            art_class = arts_map[name]
            self.shapes.append(art_class().create_combined_shape())
        else:
            raise f"Undefined customized art: {name}"
        
        self.draw()


