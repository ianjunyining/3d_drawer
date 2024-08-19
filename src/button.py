import turtle

class Button:
    def __init__(self, pen: turtle.Turtle, top_left, sz, txt):
        self.pen = pen
        self.pen.hideturtle()
        self.top_left = top_left
        self.sz = sz
        self.txt = txt
        self.selected = False
        self.clr_selected = "Blue"
        self.clr_unselected = "Gray"
    
    def draw(self):
        self.pen.clear()
        self.pen.color(self.clr_selected if self.selected else self.clr_unselected)
        x0, y0 = self.top_left
        dx, dy = self.sz
        self.pen.penup()
        self.pen.goto(x0, y0)
        self.pen.pendown()
        self.pen.goto(x0 + dx, y0)
        self.pen.goto(x0 + dx, y0 + dy)
        self.pen.goto(x0, y0 + dy)
        self.pen.goto(x0, y0)
        self.pen.penup()
        self.pen.goto(x0 + dx / 5, y0 + dy - dy / 3)
        self.pen.write(self.txt, font=("Arial", 12))

    def move(self, delta):
        x0, y0 = self.top_left
        self.top_left = (x0 + delta[0], y0 + delta[1])
        self.draw()
        
    def set_selection(self, selected: bool):
        if self.selected != selected:
            self.selected = selected
            self.draw()

    def inbox(self, pt):
        return pt[0] > self.top_left[0] \
            and pt[0] < self.top_left[0] + self.sz[0] \
                and pt[1] < self.top_left[1] \
                    and pt[1] > self.top_left[1] + self.sz[1]