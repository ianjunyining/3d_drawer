from pynput import keyboard
import threading

from functools import partial
import turtle
from src.drawer import Drawer

########################## Setup pynput ####################################################
# Flag to control the pynput listener thread
stop_pynput_listener = threading.Event()

def on_shift_press(key):
    try:
        if key == keyboard.Key.shift:
            drawer.shift_pressed = True
        # if drawer.shift_pressed:
        #     print(f"Shift + {key.name} key pressed")
    except AttributeError:
        pass

def on_shift_release(key):
    try:
        if key == keyboard.Key.shift:
            drawer.shift_pressed = False
#        if drawer.shift_pressed:
#            print(f"Shift + {key.name} key released")
    except AttributeError:
        pass
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def start_pynput_listener():
    with keyboard.Listener(on_press=on_shift_press, on_release=on_shift_release) as listener:
        while not stop_pynput_listener.is_set():
            listener.join(0.1)  # Check periodically if the stop event is set

def close_pynput():
    stop_pynput_listener.set()  # Signal the listener thread to stop
    pynput_listener_thread.join()  # Wait for the listener thread to finish
    turtle.bye()  # Close the Turtle GUI
    print("Program terminated.")
    exit()  # Ensure the entire program exits

# Set up the close event handler
def on_close():
    close_pynput()

# Run the pynput listener in a separate thread to allow the main program to continue running
pynput_listener_thread = threading.Thread(target=start_pynput_listener)
pynput_listener_thread.start()

########################## Setup window resize ####################################################
turtle.hideturtle()
turtle.speed(0)

screen = turtle.Screen()
screen.tracer(0)
drawer = Drawer(screen)

# Store the initial window size
initial_width = screen.window_width()
initial_height = screen.window_height()

#def on_resize(new_width, new_height):
#    print(f"Window resized to: {new_width}x{new_height}")

def check_resize():
    global initial_width, initial_height
    current_width = screen.window_width()
    current_height = screen.window_height()
    
    if current_width != initial_width or current_height != initial_height:
        drawer.on_window_resize(current_width, current_height)
        initial_width = current_width
        initial_height = current_height
    
    # Continue checking for resize events
    screen.ontimer(check_resize, 100)

# Start checking for resize events
check_resize()

########################## Setup drawer and onkey functions ####################################################

screen.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", on_close)

screen.onclick(drawer.onclick)
screen.onkeypress(drawer.onkey_a, "a")
screen.onkeypress(drawer.onkey_d, "d")
screen.onkeypress(drawer.onkey_q, "q")
screen.onkeypress(drawer.onkey_e, "e")
screen.onkeypress(drawer.onkey_w, "w")
screen.onkeypress(drawer.onkey_s, "s")
screen.onkeypress(drawer.onkey_A, "A")
screen.onkeypress(drawer.onkey_D, "D")
screen.onkeypress(drawer.onkey_Q, "Q")
screen.onkeypress(drawer.onkey_E, "E")
screen.onkeypress(drawer.onkey_W, "W")
screen.onkeypress(drawer.onkey_S, "S")

# ------------------------- translation ----
screen.onkeypress(drawer.onkey_j, "j")
screen.onkeypress(drawer.onkey_l, "l")
screen.onkeypress(drawer.onkey_u, "u")
screen.onkeypress(drawer.onkey_o, "o")
screen.onkeypress(drawer.onkey_i, "i")
screen.onkeypress(drawer.onkey_k, "k")
screen.onkeypress(drawer.onkey_J, "J")
screen.onkeypress(drawer.onkey_L, "L")
screen.onkeypress(drawer.onkey_U, "U")
screen.onkeypress(drawer.onkey_O, "O")
screen.onkeypress(drawer.onkey_I, "I")
screen.onkeypress(drawer.onkey_K, "K")
screen.onkeypress(drawer.onkeycopy, "c")
screen.onkeypress(drawer.onkeydelete, "BackSpace")

screen.listen()
screen.mainloop()
