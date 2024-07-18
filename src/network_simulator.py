import tkinter as tk
import re

def center_bottom_menu_position(event=None, obj=None, canvas=None):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    obj.place(x=canvas_width // 2, y=canvas_height - 20, anchor="s")
    root.title(f"Application Size: {canvas_width}x{canvas_height}")  # Update the window title with the size

class ElementGroup:
    def __init__(self, canvas, root, initial_x, initial_y, elements=None):
        self.canvas = canvas
        self.root = root
        self.initial_x = initial_x
        self.initial_y = initial_y
        if elements:
            self.elements = elements
        self.options_menu = None  # Initialize options_menu as None

        # Import tkinter as tk within the class definition
        self.tk = tk  # Store tkinter as a class attribute

    def start_move(self, event):
        for shape in self.elements:
            self.elements[shape]['last_x'] = event.x
            self.elements[shape]['last_y'] = event.y

    def move(self,event):
        if all(['obj' in self.elements[shape] for shape in self.elements]) is False:
            raise ValueError("All elements must have an 'obj' key BEFORE initiating move")
        for shape in self.elements:
            dx = event.x - self.elements[shape]['last_x']
            dy = event.y - self.elements[shape]['last_y']
            canvas.move(self.elements[shape]['obj'], dx, dy)
            self.elements[shape]['x'] += dx
            self.elements[shape]['y'] += dy
            self.elements[shape]['last_x'] = event.x
            self.elements[shape]['last_y'] = event.y

    def bind_events_move(self):
        if all(['obj' in self.elements[shape] for shape in self.elements]) is False:
            raise ValueError("All elements must have an 'obj' key BEFORE initiating bind_events_move")
        for shape in self.elements:
            self.canvas.tag_bind(self.elements[shape]['obj'], "<ButtonPress-1>", lambda event: self.start_move(event))
            self.canvas.tag_bind(self.elements[shape]['obj'], "<B1-Motion>", lambda event: self.move(event))
            self.canvas.tag_bind(self.elements[shape]['obj'], "<ButtonPress-2>", lambda event: create_input_fields(event,self.canvas, self.root))

    def create_elements(self):
        for shape in self.elements:
            current_shape = self.elements[shape]
            if 'text' in shape or 'oval' in shape:
                current_shape['x'] = self.initial_x + current_shape['offset_x']
                current_shape['y'] = self.initial_y + current_shape['offset_y']
                current_shape['last_x'] = current_shape['x']
                current_shape['last_y'] = current_shape['y']
            
            if 'text' in shape:
                current_shape['obj'] = self.canvas.create_text(
                    current_shape['x'],
                    current_shape['y'],
                    text=current_shape['text'],
                    font=current_shape['font'],
                    fill=current_shape['fill']
                )
                self.canvas.tag_bind(current_shape['obj'], "<Double-Button-1>", lambda event, shape=shape: self.edit_text(shape))
            if 'oval' in shape:
                current_shape['obj'] = self.canvas.create_oval(
                    current_shape['x'],
                    current_shape['y'],
                    current_shape['x'] + current_shape['width'],
                    current_shape['y'] + current_shape['height'],
                    outline=current_shape['outline'],
                    fill=current_shape['fill']
                )

    def edit_text(self, shape):
        if shape in self.elements and 'text' in self.elements[shape]:
            if 'entry' in self.elements[shape]:
                self.elements[shape]['entry'].destroy()  # Destroy the existing entry widget if it exists
            x = self.elements[shape]['x']
            y = self.elements[shape]['y']
            text = self.elements[shape]['text']
            font = self.elements[shape]['font']
            entry = self.tk.Entry(self.canvas, font=font)
            entry.insert(0, text)
            entry.place(x=x, y=y, anchor="center")
            entry.focus_set()
            entry.bind("<Return>", lambda event: self.save_text(shape, entry))  # Bind the Return key event
            self.elements[shape]['entry'] = entry  # Store the new entry widget

    def save_text(self, shape, entry):
        new_text = entry.get()
        self.elements[shape]['text'] = new_text
        self.canvas.itemconfig(self.elements[shape]['obj'], text=new_text)
        entry.destroy()  # Destroy the entry widget after saving


def create_input_fields(event,canvas, root):
    inputs = { 
        "input_field_ip_address": {
            "text": "IP Address",
            "font": ("Arial", 12),
            "fill": "black",
            "regex": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
        },
        "input_field_subnet_mask": {
            "text": "Subnet Mask",
            "font": ("Arial", 12),
            "fill": "black",
            "regex": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
        },
    }
    window = tk.Toplevel(root)
    window.geometry("200x200")
    window.title("Input Fields")
    window.bind("<Escape>", lambda event: window.destroy())  # Bind the Escape key to destroy the window
    for field in inputs:
        current_input = inputs[field]
        label = tk.Label(window, text=current_input["text"], font=current_input["font"], fg=current_input["fill"])
        label.pack()
        entry = tk.Entry(window, font=current_input["font"])
        entry.pack()
        inputs[field]["entry"] = entry
    # create a button to save the input fields
    save_button = tk.Button(window, text="Save", command=lambda: save_input_fields(inputs,window))
    save_button.pack()


def save_input_fields(inputs,window):
    for field in inputs:
        value = inputs[field]["entry"].get()
        if not re.match(inputs[field]["regex"],value):
            print(f"{value} is not a valid {field}")
            return
        print(f"{field}: {inputs[field]['entry'].get()}")
    # destroy the window
    window.destroy()





def create_router(canvas, root, initial_x, initial_y):
    shapes = {
        'oval':{
            'offset_x': 0,
            'offset_y': 0,
            'width': 100,
            'height': 100,
            'outline': "black",
            'fill': "white",
        },
        'text_name':{
            'offset_x': 50,
            'offset_y': 50,
            'text': "Router",
            'font': ("Arial", 12),
            'fill': "black",
        },
        'text_hostname':{
            'offset_x': 50,
            'offset_y': 105,
            'text': "Hostname",
            'font': ("Arial", 10),
            'fill': "black",
        }
    }
    router = ElementGroup(canvas, root, initial_x, initial_y, shapes)
    router.create_elements()
    router.bind_events_move()


if __name__ == '__main__':

  root = tk.Tk()

  canvas = tk.Canvas(root, width=800, height=600)
  x, y = 100, 100  

  canvas.pack(fill=tk.BOTH, expand=True)
  root.bind("<Configure>", lambda event: center_bottom_menu_position(button_frame, canvas))
  button_frame = tk.Frame(root)
  button = tk.Button(button_frame, text="Create Router", command=lambda: create_router(canvas, root, x, y))
  button_frame.pack(side=tk.BOTTOM, pady=10)

  button.pack()

  root.bind("<Configure>", lambda event: center_bottom_menu_position(event, button_frame, canvas))
  
  root.mainloop()