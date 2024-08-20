from src.canvas import Canvas
from src.shape import *
from src.button import Button
import turtle, enum, math

class Action(enum.Enum):
    View = 1
    SELECT = 2
    LINE = 3
    CUBE = 4


class Color(enum.Enum):
    BLACK = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4


class State(enum.Enum):
    START = 1
    END = 2


class Drawer():
    def __init__(self, screen):
        self.screen = screen
        self.shift_pressed = False
        self.w = screen.window_width()
        self.h = screen.window_height()
        self.hw = self.w / 2 
        self.hh = self.h / 2 
        self.gap = 5
        self.btn_sz = (60, -30)
        self.magnitude = 10

        self.create_buttons()

        self.canvas = Canvas()
        self.action = Action.SELECT
        self.color = Color.BLUE
        self.state = State.END
        self.temp_line = None
        self.temp_cube = None

        # pen = turtle.Turtle()
        # pen.color(self.get_color_str(self.color))
        # self.temp_line = Line(pen, self.canvas.transformation, (0, 0, 0, 1), (100, 100, 10, 1))
        # self.temp_line.draw()
        # self.canvas.shapes.append(self.temp_line)

        # pen = turtle.Turtle()
        # pen.color(self.get_color_str(self.color))
        # self.temp_line = Line(pen, self.canvas.transformation, (0, 0, 0, 1), (-100, 100, 10, 1))
        # self.temp_line.draw()
        # self.canvas.shapes.append(self.temp_line)
        # c = [
        #     (0, 0, 0),
        #     (0, 0, 500),
        #     (0, 500, 0),
        #     (0, 500, 500),
        #     (500, 0, 0),
        #     (500, 0, 500),
        #     (500, 500, 0),
        #     (500, 500, 500),
        # ]
        # for i in range(8):
        #     pen = turtle.Turtle()
        #     pen.color(self.get_color_str(self.color))
        #     self.temp_line = Cube(pen, self.canvas.transformation, 500, c[i])
        #     self.canvas.shapes.append(self.temp_line)
        #     self.canvas.draw()

        pen = turtle.Turtle()
        pen.color(self.get_color_str(self.color))
        self.temp_cube = Cube(pen, self.canvas.transformation, 500, [200, 200, 200])
        self.canvas.shapes.append(self.temp_cube)
        self.canvas.draw()

        pen = turtle.Turtle()
        pen.color(self.get_color_str(self.color))
        self.temp_world_coord = WorldCoord(pen, self.canvas.transformation, 300)
        self.canvas.shapes.append(self.temp_world_coord)

        self.canvas.draw()


    def get_color_str(self, color: Color):
        color_map = {
            Color.BLACK : "black",
            Color.RED : "red",
            Color.BLUE : "blue",
            Color.GREEN : "green",
            Color.YELLOW : "yellow",
        }
        return color_map[color]
    
    def create_buttons(self):
        btn_gap = self.btn_sz[0] + self.gap
        btn_st_y = self.hh - self.gap
        btn_st_x = -self.hw + self.gap
        self.action_buttons = {
            Action.SELECT: Button(turtle.Turtle(), (btn_st_x, btn_st_y), self.btn_sz, "Select"),
            Action.View: Button(turtle.Turtle(), (btn_st_x + btn_gap * 1, btn_st_y), self.btn_sz, "3D view"),
            Action.LINE: Button(turtle.Turtle(), (btn_st_x + btn_gap * 2, btn_st_y), self.btn_sz, "Line"),
            Action.CUBE: Button(turtle.Turtle(), (btn_st_x + btn_gap * 3, btn_st_y), self.btn_sz, "Cube"),
        }
        self.action_buttons[Action.SELECT].selected = True
        for _, btn in self.action_buttons.items():
            btn.draw()

        # btn_st_x += len(self.action_buttons.items()) * btn_gap + 20
        btn_st_y += self.btn_sz[1] - self.gap
        self.color_buttons = {
            Color.BLUE: Button(turtle.Turtle(), (btn_st_x + btn_gap * 0, btn_st_y), self.btn_sz, "Blue"),
            Color.RED: Button(turtle.Turtle(), (btn_st_x + btn_gap * 1, btn_st_y), self.btn_sz, "Red"),
            Color.GREEN: Button(turtle.Turtle(), (btn_st_x + btn_gap * 2, btn_st_y), self.btn_sz, "Green"),
            Color.YELLOW: Button(turtle.Turtle(), (btn_st_x + btn_gap * 3, btn_st_y), self.btn_sz, "Yellow"),
            Color.BLACK: Button(turtle.Turtle(), (btn_st_x + btn_gap * 4, btn_st_y), self.btn_sz, "Black"),
        }
        self.color_buttons[Color.BLUE].selected = True

        for _, btn in self.color_buttons.items():
            btn.draw()

    def on_window_resize(self, w, h):
        delta = (-(w - self.w) / 2, (h - self.h) / 2)
        self.w = w
        self.h = h

        for _, btn in self.action_buttons.items():
            btn.move(delta)

        for _, btn in self.color_buttons.items():
            btn.move(delta)

    def click_on_action_button(self, x, y):
        old_act = self.action
        new_act = None
        for act, btn in self.action_buttons.items():
            if btn.inbox((x, y)):
                new_act = act
                break
        if new_act and new_act != old_act:
            self.action = new_act
            self.action_buttons[old_act].set_selection(False)
            self.action_buttons[new_act].set_selection(True)
        return new_act     

    def click_on_color_button(self, x, y):
        old_color = self.color
        new_color = None
        for color, btn in self.color_buttons.items():
            if btn.inbox((x, y)):
                new_color = color
                break
        if new_color and new_color != old_color:
            self.color = new_color
            self.color_buttons[old_color].set_selection(False)
            self.color_buttons[new_color].set_selection(True)
        return new_color     

    def make_line(self, x, y):
        if self.action != Action.LINE:
            return
        points3D = self.canvas.transformation.project_2d_to_3d([(x, y)])
        if self.state == State.END:
            self.state = State.START
            pen = turtle.Turtle()
            pen.color(self.get_color_str(self.color))
            self.temp_line = Line(pen, self.canvas.transformation, points3D[0], points3D[0])
            self.temp_line.draw()
        elif self.state == State.START:
            self.state = State.END
            self.temp_line.points3D[1] = points3D[0]
            self.temp_line.draw()
            self.canvas.shapes.append(self.temp_line)

    def make_cube(self, x, y):
        if self.action != Action.CUBE:
            return
        points3D = self.canvas.transformation.project_2d_to_3d([(x, y)])
        if self.state == State.END:
            self.state = State.START
            pen = turtle.Turtle()
            pen.color(self.get_color_str(self.color))
            self.temp_cube = Cube(pen, self.canvas.transformation, 0, points3D[0])
            self.temp_cube.draw()
        elif self.state == State.START:
            self.state = State.END    
            self.temp_cube.s = geo.distance_3d(
                self.temp_cube.center, 
                points3D[0],
            )
            self.temp_cube.draw()
            self.canvas.shapes.append(self.temp_cube)

    def make_polygon(self, x, y):
        if self.action != Action.POLYGON:
            return
        if self.state == State.END:
            self.state = State.START
            pen = turtle.Turtle()
            pen.color(self.get_color_str(self.color))
            self.temp_polygon = Polygon(pen, [(x, y)])
            self.temp_polygon.draw()
        elif self.state == State.START:
            self.temp_polygon.points.append((x, y))
            self.temp_polygon.draw()
            if self.shift_pressed:
                self.state = State.END
                self.canvas.shapes.append(self.temp_polygon)


    def make_regular_polygon(self, x, y):
        if self.action != Action.RPOLYGON:
            return
        if self.state == State.END:
            self.state = State.START
            pen = turtle.Turtle()
            pen.color(self.get_color_str(self.color))
            self.temp_rpolygon = RegularPolygon(pen, (x, y), 0, 0)
        elif self.state == State.START:
            self.state = State.END
            sides = self.screen.textinput("Enter sides", "How many sides?")
            self.screen.listen()
            if sides:
                self.temp_rpolygon.r = geo.distance(self.temp_rpolygon.center, (x, y)) 
                self.temp_rpolygon.num_sides = int(sides)
                self.temp_rpolygon.draw()
                self.canvas.shapes.append(self.temp_rpolygon)

    def onclick(self, x, y):
        if self.click_on_action_button(x, y):
            pass
        elif self.click_on_color_button(x, y):
            # don't draw
            pass
        elif self.action == Action.SELECT:
            self.canvas.select_shapes((x, y), self.shift_pressed)
        elif self.action == Action.LINE:
            self.make_line(x, y)
        elif self.action == Action.CUBE:
            self.make_cube(x, y)
        

    def onkeygroup(self):
        self.canvas.combine_selected()

    def onkeycopy(self):
        self.canvas.copy_selected()
        
    def onkey_3dview_translate(self, key_pressed, magnitude=1):
        if self.action != Action.View:
            return
        delta = magnitude * 10
        key_translation = {
            "j" : (self.canvas.transformation.inc_x, -delta),
            "l" : (self.canvas.transformation.inc_x, delta),
            "u" : (self.canvas.transformation.inc_y, -delta),
            "o" : (self.canvas.transformation.inc_y, delta),
            "i" : (self.canvas.transformation.inc_z, -delta),
            "k" : (self.canvas.transformation.inc_z, delta),
        }
        
        if key_pressed in key_translation.keys():
            func, v = key_translation[key_pressed]
            func(v)
            self.canvas.draw()

    def onkey_3dview_rotate(self, key_pressed, magnitude=1):
        if self.action != Action.View:
            return
        delta = math.pi / 180 * magnitude
        
        key_rotate = {
            "a" : (self.canvas.transformation.inc_yaw, -delta),
            "d" : (self.canvas.transformation.inc_yaw, delta),
            "q" : (self.canvas.transformation.inc_pitch, -delta),
            "e" : (self.canvas.transformation.inc_pitch, delta),
            "w" : (self.canvas.transformation.inc_roll, -delta),
            "s" : (self.canvas.transformation.inc_roll, delta),      
        }
        if key_pressed in key_rotate.keys():
            func, v = key_rotate[key_pressed]
            func(v)
            self.canvas.draw()

    def onkey_a(self):
        self.onkey_3dview_rotate("a")

    def onkey_d(self):
        self.onkey_3dview_rotate("d")

    def onkey_q(self):
        self.onkey_3dview_rotate("q")

    def onkey_e(self):
        self.onkey_3dview_rotate("e")
    
    def onkey_w(self):
        self.onkey_3dview_rotate("w")

    def onkey_s(self):
        self.onkey_3dview_rotate("s")

    def onkey_A(self):
        self.onkey_3dview_rotate("a", 10)

    def onkey_D(self):
        self.onkey_3dview_rotate("d", 10)

    def onkey_Q(self):
        self.onkey_3dview_rotate("q", 10)

    def onkey_E(self):
        self.onkey_3dview_rotate("e", 10)
    
    def onkey_W(self):
        self.onkey_3dview_rotate("w", 10)

    def onkey_S(self):
        self.onkey_3dview_rotate("s", 10)

    # ------------------ translation ------------------
    def onkey_j(self):
        self.onkey_3dview_translate("j")

    def onkey_l(self):
        self.onkey_3dview_translate("l")

    def onkey_u(self):
        self.onkey_3dview_translate("u")

    def onkey_o(self):
        self.onkey_3dview_translate("o")
    
    def onkey_i(self):
        self.onkey_3dview_translate("i")

    def onkey_k(self):
        self.onkey_3dview_translate("k")

    def onkey_J(self):
        self.onkey_3dview_translate("j", 10)

    def onkey_L(self):
        self.onkey_3dview_translate("l", 10)

    def onkey_U(self):
        self.onkey_3dview_translate("u", 10)

    def onkey_O(self):
        self.onkey_3dview_translate("o", 10)
    
    def onkey_I(self):
        self.onkey_3dview_translate("i", 10)

    def onkey_K(self):
        self.onkey_3dview_translate("k", 10)

