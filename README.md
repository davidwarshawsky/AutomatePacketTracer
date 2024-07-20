# Network Simulator

This project is a network simulator built with Python's Tkinter library. It allows you to create and manage network elements such as routers, and visually connect them to simulate a network.

## Features

- Create network elements (routers)
- Move network elements within the canvas
- Connect network elements with visual lines
- Edit properties of network elements
- Save and load configurations

## Getting Started

### Prerequisites

- Python 3.x

### Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/network-simulator.git
cd network-simulator
```

## Code Overview

### Main Components

- **ElementGroup**: Class to manage individual network elements.
- **Network**: Class to manage the overall network, including routers and connections.

### Key Functions
- **center_bottom_menu_position**: Centers and positions the menu at the bottom of the canvas.
- **start_move**: Initializes the movement of network elements.
- **move**: Handles the movement of network elements.
- **update_connections**: Updates the positions of connections between elements.
- **bind_events**: Binds events to network elements.
- **create_elements**: Creates network elements on the canvas.
- **__edit_text**: Allows editing of text properties of elements.
- **__save_text**: Saves edited text properties of elements.
- **create_input_fields**: Creates input fields for element properties.
- **save_input_fields**: Saves input fields for element properties.
- **create_router**: Creates a new router element.
- **select_router**: Selects a router for connection.
- **create_connection**: Creates a connection between two routers.


### Future Updates:
- Ability to export commands
- Create RIP class to allow for the option rather than automatic configuration
- Create OSPF class to allow for OSPF configuration
- Create ability to save router as a csv file to be read in later.
- N for new router
- A to add an interface for the current router
- S to save only the currently selected router script.
- QQ to quit the application
- R for a reminder of options as a menu popup

Go to this link and press run to use it: https://replit.com/@DavidWarshawsky/AutoPacket-Tracer#main.py
Make fullscreen and then you can play around with it. 
