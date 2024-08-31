from src.shape import *


class ArtBase:
    def __init__(self, transformation) -> None:
        self.transformation = transformation

    def create_shapes(self):
        pass

    def create_combined_shape(self):
        return CombinedShape(None, self.transformation, self.create_shapes())
    