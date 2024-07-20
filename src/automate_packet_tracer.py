import tkinter as tk
import re

def center_bottom_menu_position(event=None, obj=None, canvas=None):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    obj.place(x=canvas_width // 2, y=canvas_height - 20, anchor="s")
    root.title(f"Network Simulator")

class ElementGroup:
    def __init__(self, canvas, root, initial_x, initial_y, elements=None, connections=None):
        self.canvas = canvas
        self.root = root
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.connections = connections if connections else []
        if elements:
            self.elements = elements
        self.options_menu = None  # Initialize options_menu as None
        self.stored_data = {}  # Initialize stored_data as an empty dictionary
        self.input_fields = {"input_field_ip_address": "", "input_field_subnet_mask": ""}  # Initialize input fields

        for shape in self.elements:
            self.stored_data[shape] = {}

        # Import tkinter as tk within the class definition
        self.tk = tk  # Store tkinter as a class attribute

    def start_move(self, event):
        for shape in self.elements:
            self.elements[shape]['last_x'] = event.x
            self.elements[shape]['last_y'] = event.y

    def move(self, event):
        if all(['obj' in self.elements[shape] for shape in self.elements]) is False:
            raise ValueError("All elements must have an 'obj' key BEFORE initiating move")
        for shape in self.elements:
            dx = event.x - self.elements[shape]['last_x']
            dy = event.y - self.elements[shape]['last_y']
            self.canvas.move(self.elements[shape]['obj'], dx, dy)
            self.elements[shape]['x'] += dx
            self.elements[shape]['y'] += dy
            self.elements[shape]['last_x'] = event.x
            self.elements[shape]['last_y'] = event.y
        self.update_connections()

    def update_connections(self):
        for connection in self.connections:
            self.canvas.coords(
                connection['line'],
                connection['router1'].elements['oval']['x'] + 50,
                connection['router1'].elements['oval']['y'] + 50,
                connection['router2'].elements['oval']['x'] + 50,
                connection['router2'].elements['oval']['y'] + 50
            )
        self.redraw_elements()  # Redraw elements to ensure they are on top of connections

    def redraw_elements(self):
        for shape in self.elements:
            self.canvas.tag_raise(self.elements[shape]['obj'])

    def bind_events(self):
        if all(['obj' in self.elements[shape] for shape in self.elements]) is False:
            raise ValueError("All elements must have an 'obj' key BEFORE initiating bind_events")
        for shape in self.elements:
            self.canvas.tag_bind(self.elements[shape]['obj'], "<ButtonPress-1>", lambda event: self.start_move(event))
            self.canvas.tag_bind(self.elements[shape]['obj'], "<B1-Motion>", lambda event: self.move(event))
            self.canvas.tag_bind(self.elements[shape]['obj'], "<ButtonPress-2>", lambda event: create_input_fields(event, self.canvas, self.root, self))  # Pass self

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
                self.stored_data[shape]['text'] = current_shape['text']
                self.canvas.tag_bind(current_shape['obj'], "<Double-Button-1>", lambda event, shape=shape: self.__edit_text(shape))
            if 'oval' in shape:
                current_shape['obj'] = self.canvas.create_oval(
                    current_shape['x'],
                    current_shape['y'],
                    current_shape['x'] + current_shape['width'],
                    current_shape['y'] + current_shape['height'],
                    outline=current_shape['outline'],
                    fill=current_shape['fill']
                )

    def __edit_text(self, shape):
        if shape in self.elements and 'text' in self.elements[shape]:
            if 'entry' in self.elements[shape]:
                self.elements[shape]['entry'].destroy()  # Destroy the existing entry widget if it exists
            x = self.elements[shape]['x']
            y = self.elements[shape]['y']
            text = self.stored_data[shape]['text']
            font = self.elements[shape]['font']
            entry = self.tk.Entry(self.canvas, font=font)
            entry.insert(0, text)
            entry.place(x=x, y=y, anchor="center")
            entry.focus_set()
            entry.bind("<Return>", lambda event: self.__save_text(shape, entry))  # Bind the Return key event
            self.elements[shape]['entry'] = entry  # Store the new entry widget

    def __save_text(self, shape, entry):
        new_text = entry.get()
        self.stored_data[shape]['text'] = new_text
        self.elements[shape]['text'] = self.stored_data[shape]['text']
        self.canvas.itemconfig(self.elements[shape]['obj'], text=self.stored_data[shape]['text'])
        entry.destroy()  # Destroy the entry widget after saving
        print(self.stored_data)


def create_input_fields(event, canvas, root, element_group):
    inputs = {
        "input_field_ip_address": {
            "text": "IP Address",
            "font": ("Arial", 12),
            "fill": "black",
            "regex": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
            "value": element_group.input_fields["input_field_ip_address"]  # Get the saved value
        },
        "input_field_subnet_mask": {
            "text": "Subnet Mask",
            "font": ("Arial", 12),
            "fill": "black",
            "regex": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
            "value": element_group.input_fields["input_field_subnet_mask"]  # Get the saved value
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
        entry.insert(0, current_input["value"])  # Set the current value
        entry.pack()
        inputs[field]["entry"] = entry
    # create a button to save the input fields
    save_button = tk.Button(window, text="Save", command=lambda: save_input_fields(inputs, window, element_group))
    save_button.pack()


def save_input_fields(inputs, window, element_group):
    for field in inputs:
        value = inputs[field]["entry"].get()
        if not re.match(inputs[field]["regex"], value):
            print(f"{value} is not a valid {field}")
            return
        element_group.input_fields[field] = value  # Save the value in the element group
        print(f"{field}: {inputs[field]['entry'].get()}")
    # destroy the window
    window.destroy()


class Network:
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self.routers = []  # List to store ElementGroup instances
        self.selected_routers = []  # List to store selected routers for connection

    def create_router(self, initial_x, initial_y):
        shapes = {
            'oval': {
                'offset_x': 0,
                'offset_y': 0,
                'width': 100,
                'height': 100,
                'outline': "black",
                'fill': "gray",
            },
            'text_name': {
                'offset_x': 50,
                'offset_y': 50,
                'text': "Router",
                'font': ("Arial", 12),
                'fill': "black",
            },
            'text_hostname': {
                'offset_x': 50,
                'offset_y': 105,
                'text': "Hostname",
                'font': ("Arial", 10),
                'fill': "black",
            }
        }
        router = ElementGroup(self.canvas, self.root, initial_x, initial_y, shapes)
        router.create_elements()
        router.bind_events()
        self.routers.append(router)  # Add the router to the list

    def select_router(self, router):
        if router in self.selected_routers:
            self.selected_routers.remove(router)
        else:
            self.selected_routers.append(router)

        if len(self.selected_routers) == 2:
            self.create_connection(self.selected_routers[0], self.selected_routers[1])
            self.selected_routers = []

    def create_connection(self, router1, router2):
        line = self.canvas.create_line(
            router1.elements['oval']['x'] + 50,
            router1.elements['oval']['y'] + 50,
            router2.elements['oval']['x'] + 50,
            router2.elements['oval']['y'] + 50,
            fill="red"
        )
        connection = {
            'router1': router1,
            'router2': router2,
            'line': line
        }
        router1.connections.append(connection)
        router2.connections.append(connection)
        router1.redraw_elements()  # Redraw the routers to bring them on top of the connections
        router2.redraw_elements()

if __name__ == '__main__':
    root = tk.Tk()

    canvas = tk.Canvas(root, width=800, height=600)
    x, y = 100, 100

    canvas.pack(fill=tk.BOTH, expand=True)
    root.bind("<Configure>", lambda event: center_bottom_menu_position(button_frame, canvas))
    button_frame = tk.Frame(root)
    network = Network(canvas, root)  # Create a Network instance
    button = tk.Button(button_frame, text="Create Router", command=lambda: network.create_router(x, y))  # Use the Network instance
    connection_button = tk.Button(button_frame, text="New Connection", command=lambda: start_new_connection(network), bg="gray", fg="red")

    button.pack(side=tk.LEFT)
    connection_button.pack(side=tk.LEFT)

    root.bind("<Configure>", lambda event: center_bottom_menu_position(event, button_frame, canvas))

    def start_new_connection(network):
        for router in network.routers:
            for shape in router.elements:
                if 'obj' in router.elements[shape]:
                    canvas.tag_bind(router.elements[shape]['obj'], "<ButtonPress-1>", lambda event, router=router: network.select_router(router))

    root.mainloop()
