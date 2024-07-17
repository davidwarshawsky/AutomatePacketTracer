import tkinter as tk

router = None  # Global variable to store the router

def start_move(event):
    global last_x, last_y
    last_x = event.x
    last_y = event.y

def stop_move(event):
    pass

def show_hostname_entry(event):
    if router['entry'] is None:
        router['entry'] = tk.Entry(root)
        router['entry'].insert(0, router['hostname'])
        router['entry'].place(x=router['x'] + 25, y=router['y'] + 60, anchor="center")
        router['entry'].focus_set()
        router['entry'].bind("<Return>", lambda event: update_hostname())
        router['entry'].bind("<FocusOut>", lambda event: update_hostname())

def create_router():
    global router
    if router is not None:
        return  # Return early if a router already exists

    x, y = 100, 100  # Initial position for demonstration
    router = {
        'oval': canvas.create_oval(x, y, x + 100, y + 100, outline="black", fill="white"),
        'text': canvas.create_text(x + 50, y + 50, text="Router", font=("Arial", 12), fill="black"),
        'entry': None,
        'hostname': 'Router',
        'x': x,
        'y': y
    }
    canvas.tag_bind(router['oval'], "<ButtonPress-1>", start_move)
    canvas.tag_bind(router['oval'], "<B1-Motion>", move_router)
    canvas.tag_bind(router['oval'], "<ButtonRelease-1>", stop_move)
    canvas.tag_bind(router['oval'], "<Double-Button-1>", show_hostname_entry)

def move_router(event):
    global last_x, last_y
    dx = event.x - last_x
    dy = event.y - last_y
    canvas.move(router['oval'], dx, dy)
    canvas.move(router['text'], dx, dy)
    last_x = event.x
    last_y = event.y

def adjust_button_position(event):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    button_frame.place(x=canvas_width // 2, y=canvas_height - 20, anchor="s")
    root.title(f"Application Size: {canvas_width}x{canvas_height}")  # Update the window title with the size

def update_hostname():
    new_hostname = router['entry'].get()
    canvas.itemconfig(router['text'], text=new_hostname)
    router['hostname'] = new_hostname
    router['entry'].destroy()
    router['entry'] = None

root = tk.Tk()

root.bind("<Configure>", adjust_button_position)

root.geometry("800x600")  # Set the initial size of the application

canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill=tk.BOTH, expand=True)

button_frame = tk.Frame(root)
button_frame.place(x=400, y=580, anchor="s")

button = tk.Button(button_frame, text="Create Router", command=create_router)
button.pack()

root.mainloop()
