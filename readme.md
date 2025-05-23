# Mouse Automation Tool

This is a versatile Python-based mouse automation tool with a user-friendly graphical interface built using `tkinter`. It allows you to define multiple screen coordinates, and then automates mouse movements and clicks at those specified locations, with customizable timings.

---

## Features

* **Dynamic Coordinate Input:** Easily add and manage multiple mouse click locations directly from the GUI.
* **Real-time Mouse Position Display:** See your current mouse X and Y coordinates to help you pinpoint exact click locations.
* **Customizable Cycle Wait Time:** Set the delay (in seconds) that occurs after the tool completes clicking all defined locations before starting the cycle again.
* **Customizable Click Wait Time:** Define the delay (in seconds) between individual clicks at different locations within a single cycle.
* **Threaded Operation:** The clicking actions run in a separate thread, keeping the GUI responsive.
* **Multiple Stop Options:**
    * Click the **"Stop Script"** button in the GUI.
    * Press the **'q'** key on your keyboard.
    * Move your mouse to any of the four corners of the screen (PyAutoGUI's built-in fail-safe).

---

## Try the App (Pre-compiled Executable for Windows)

For users who want to try the application immediately without installing Python or setting up the development environment, a pre-compiled executable is available.

You can find the `mouse_clicker.exe` file directly in this Git repository.

### How to Use the Executable:

1.  **Download/Clone:** Clone or download this Git repository.
2.  **Locate:** Find the `mouse_clicker.exe` file within the repository.
3.  **Run:** Double-click `mouse_clicker.exe` to start the application.
---

---
## How to Use the App

* **Current Mouse Position:** The top label continuously displays your mouse's current **X** and **Y coordinates**. Use this to find the precise coordinates you want the tool to click.
* **Number of Locations:**
    * Enter the desired number of click locations (between 1 and 10) in the "Number of Locations" field.
    * Click the **"Set"** button. This will dynamically generate the corresponding number of input fields for coordinates.
* **Enter Coordinates (x, y):** For each "Location" field, enter the **X and Y coordinates separated by a comma** (e.g., `100, 200`).
* **Wait Time Between Cycles (seconds):** Enter the amount of time (in seconds, can be a decimal) you want the script to wait after it has clicked all the defined locations once, before starting the sequence again.
* **Wait Time Between Clicks (seconds):** Enter the amount of time (in seconds, can be a decimal) you want the script to wait after performing a click at one location before moving to the next location in the sequence.
* **Start Script:** Click the **"Start Script"** button to begin the automation.
* **Stop Script:** To halt the automation, click the **"Stop Script"** button, press the **'q'** key on your keyboard, or move your mouse to any of the screen corners (PyAutoGUI's fail-safe).

---

## Prerequisites

Before running the script (if you choose not to use the executable), ensure you have Python installed (Python 3.x is recommended). Then, install the necessary libraries using pip:

```bash
pip install pyautogui keyboard tkinter
```
