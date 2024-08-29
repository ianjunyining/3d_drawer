import turtle
from src.shape import *
from arts.art_base import ArtBase


class Walls(ArtBase):

    def __init__(self, transformation) -> None:
        super().__init__(transformation)
        self.num_blocks = 10
        self.side_len = 100

    def gen_centers_xy(self):
        centers = []
        for x in range(self.num_blocks):
            for y in range(self.num_blocks):
                centers.append([x * self.side_len, y * self.side_len, 0])
        return centers

    def gen_centers_xz(self):
        centers = []
        for x in range(self.num_blocks):
            for z in range(self.num_blocks):
                centers.append([x * self.side_len, 0, z * self.side_len])
        return centers

    def gen_centers_yz(self):
        centers = []
        for y in range(self.num_blocks):
            for z in range(self.num_blocks):
                centers.append([0, y * self.side_len, z * self.side_len])
        return centers
    
    def create_wall(self, centers, color):
        shapes = []
        for c in centers:
            pen = turtle.Turtle()
            pen.color(color)
            shapes.append(Cube(pen, self.transformation, self.side_len, c))
        return shapes

    def create_shapes(self):
        shapes = []
        shapes.extend(self.create_wall(self.gen_centers_xy(), "red"))
        shapes.extend(self.create_wall(self.gen_centers_xz(), "green"))
        shapes.extend(self.create_wall(self.gen_centers_yz(), "blue"))
        return shapes
    

    
