import turtle
from src.shape import *
from arts.art_base import ArtBase
import math
import numpy as np


class Planet:
    
    def __init__(self, rotation_radius) -> None:
        self.ratation_radius = rotation_radius
        self.ratation_circle = None
        self.sphere = None
        self.make_random()

    def make_random(self):
        colors = ["red", "green", "blue", "black"]
        self.planet_radius = np.random.randint(50, 100)
        self.init_angle = np.random.randint(0, 360) * math.pi / 180
        self.rotation_speed = np.random.randint(2, 10) * math.pi / 180
        self.color = colors[np.random.randint(0, len(colors))]


class Solar(ArtBase):

    def __init__(self, transformation) -> None:
        super().__init__(transformation)
        self.sun_radius = 150
        self.num_planets = 7
        self.planet_gap = 300
        self.planets = []
        self.sun = []

    def make_planet(self, rotation_radius):
        planet = Planet(rotation_radius)
        circle_pen = turtle.Turtle()
        circle_pen.color(planet.color)
        planet.ratation_circle = Circle(circle_pen, self.transformation, planet.ratation_radius)
        sphere_pen = turtle.Turtle()
        sphere_pen.color(planet.color)
        planet.sphere = Sphere(
            sphere_pen, 
            self.transformation, 
            planet.planet_radius,
            [planet.ratation_radius * math.cos(planet.init_angle), planet.ratation_radius * math.sin(planet.init_angle), 0],
        )
        return planet

    def create_shapes(self):
        shapes = []
        pen = turtle.Turtle()
        pen.color("orange")
        self.sun = Sphere(pen, self.transformation, self.sun_radius)
        shapes.append(self.sun)
        for i in range(self.num_planets):
            planet = self.make_planet((i + 1) * self.planet_gap)
            self.planets.append(planet)
            shapes.append(planet.ratation_circle)
            shapes.append(planet.sphere)
        return shapes
    

    
