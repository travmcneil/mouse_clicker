import pyautogui
import time
import keyboard
import threading
import tkinter as tk
from tkinter import ttk # For potentially more advanced widgets later, but currently not strictly necessary

# --- Global Variables ---
locations = [] # This will now be dynamically populated
cycle_wait_time = 13 # Default timing in seconds between full cycles of locations
click_wait_time = 0.2 # Default timing in seconds between individual clicks

stop_flag = False
mouse_thread = None
key_listener_thread = None
mouse_pos_label = None

# Variables for dynamic coordinate entries
coordinate_entry_frames = [] # To hold references to frames containing entries
coordinate_entries = [] # To hold references to the actual entry widgets

# GUI widget references (will be assigned in create_gui)
timing_entry = None # For cycle_wait_time
click_timing_entry = None # For click_wait_time
coordinate_input_frame = None # Frame to hold dynamic coordinate entries

# --- Core Logic Functions ---

def check_keypress():
    """Monitors for 'q' keypress in a separate thread."""
    global stop_flag
    print("Key listener started. Press 'q' to stop script.")
    try:
        keyboard.wait('q')
        if not stop_flag:
            print("Stopping script due to 'q' keypress.")
            stop_script_internal()
    except Exception as e:
        print(f"Key listener error: {e}")
    finally:
        print("Key listener thread finished.")


def mouse_actions_thread():
    """Moves mouse, clicks, waits, repeats, and stops when stop_flag is True."""
    global stop_flag, cycle_wait_time, click_wait_time # Ensure these are accessible
    stop_flag = False # Reset stop flag when starting
    try:
        while not stop_flag:
            for x, y in locations:
                pyautogui.moveTo(x, y, duration=0.2)
                pyautogui.click()
                time.sleep(click_wait_time) # Use the new variable here

            if stop_flag:
                break
            time.sleep(cycle_wait_time) # Use the renamed variable here

    except pyautogui.FailSafeException:
        print("PyAutoGUI Fail-safe triggered. Program terminated.")
    except Exception as e:
        print(f"An error occurred in mouse actions: {e}")
    finally:
        if not stop_flag:
            stop_script_internal()
        print("Mouse actions thread finished.")


def update_locations_from_gui():
    """Updates the global locations list from GUI entry fields."""
    global locations, coordinate_entries
    new_locations = []
    for entry in coordinate_entries:
        try:
            x_str, y_str = entry.get().split(',')
            x = int(x_str.strip())
            y = int(y_str.strip())
            new_locations.append((x, y))
        except ValueError:
            print("Input Error: Please ensure all coordinate fields contain 'x, y' (e.g., '100, 200').")
            return False
    locations = new_locations
    return True

def update_mouse_position():
    """Updates the mouse position label in the GUI."""
    if mouse_pos_label:
        x, y = pyautogui.position()
        mouse_pos_label.config(text=f"Current Mouse Position: X={x}, Y={y}")
    mouse_pos_label.after(100, update_mouse_position)

def start_script():
    """Starts the mouse actions and key listener in separate threads."""
    global mouse_thread, key_listener_thread, cycle_wait_time, click_wait_time, stop_flag, timing_entry, click_timing_entry

    if mouse_thread and mouse_thread.is_alive():
        print("Info: Script is already running.")
        return

    if not update_locations_from_gui():
        return

    # Update cycle_wait_time
    try:
        cycle_wait_time = float(timing_entry.get()) # Allow float for more precise timing
        if cycle_wait_time < 0: # Allow 0 for no wait, but not negative
            raise ValueError("Cycle timing must be a non-negative number.")
    except ValueError:
        print("Input Error: Please enter a valid non-negative number for cycle timing (in seconds).")
        return

    # Update click_wait_time
    try:
        click_wait_time = float(click_timing_entry.get()) # Allow float for more precise timing
        if click_wait_time < 0: # Allow 0 for no wait, but not negative
            raise ValueError("Click timing must be a non-negative number.")
    except ValueError:
        print("Input Error: Please enter a valid non-negative number for click timing (in seconds).")
        return

    print(f"Starting Mouse Actions with Cycle Wait: {cycle_wait_time}s, Click Wait: {click_wait_time}s")
    stop_flag = False # Reset stop flag
    mouse_thread = threading.Thread(target=mouse_actions_thread, daemon=True)
    mouse_thread.start()

    key_listener_thread = threading.Thread(target=check_keypress, daemon=True)
    key_listener_thread.start()

    print("Script Status: Mouse actions started. Press 'Stop Script' or 'q' to halt.")

def stop_script_internal():
    """Internal function to stop the script, callable from both GUI and key listener."""
    global stop_flag, mouse_thread, key_listener_thread
    if not stop_flag:
        stop_flag = True
        print("Stopping script initiated.")

def stop_script_gui():
    """Function called when 'Stop Script' button is pressed."""
    stop_script_internal()
    print("Script Status: Attempting to stop script. Please wait a moment.")

# --- GUI Management Functions ---

def clear_coordinate_entries():
    """Removes all dynamically created coordinate entry frames."""
    global coordinate_entry_frames, coordinate_entries
    for frame in coordinate_entry_frames:
        frame.destroy()
    coordinate_entry_frames.clear()
    coordinate_entries.clear()

def create_coordinate_entries(num_locations_str):
    """Dynamically creates coordinate entry fields based on the number specified."""
    clear_coordinate_entries() # Clear existing entries first

    try:
        num_locations = int(num_locations_str)
        if not (1 <= num_locations <= 10): # Set a reasonable limit
            print("Input Error: Number of locations must be between 1 and 10.")
            return
    except ValueError:
        print("Input Error: Please enter a valid number for locations.")
        return

    global coordinate_input_frame
    # Create coordinate_input_frame if it doesn't exist, or clear its children if it does
    if not coordinate_input_frame:
        coordinate_input_frame = tk.Frame(root, bd=2, relief="groove")
        coordinate_input_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        tk.Label(coordinate_input_frame, text="Enter Coordinates (x, y):", font=("Arial", 12, "bold")).pack(pady=5)
    else:
        # Clear existing widgets, but keep the frame and its title label
        for widget in coordinate_input_frame.winfo_children():
            # Only destroy widgets that are not the initial "Enter Coordinates (x, y):" label
            if not (isinstance(widget, tk.Label) and widget.cget("text") == "Enter Coordinates (x, y):"):
                widget.destroy()


    for i in range(num_locations):
        frame = tk.Frame(coordinate_input_frame)
        frame.pack(pady=2, fill=tk.X)
        tk.Label(frame, text=f"Location {i+1}:").pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=30)
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        coordinate_entry_frames.append(frame)
        coordinate_entries.append(entry)


# --- GUI Setup ---

def create_gui():
    """Creates the main Tkinter GUI window."""
    global root, mouse_pos_label, timing_entry, click_timing_entry, coordinate_input_frame

    root = tk.Tk()
    root.title("Mouse Automation Tool")
    root.geometry("450x750") # Adjusted window size for new entry

    # Mouse Position Display
    mouse_pos_label = tk.Label(root, text="Current Mouse Position: X=?, Y=?", font=("Arial", 12, "bold"))
    mouse_pos_label.pack(pady=10)
    update_mouse_position()

    # Number of Locations Input
    num_locations_frame = tk.Frame(root)
    num_locations_frame.pack(pady=10)
    tk.Label(num_locations_frame, text="Number of Locations (1-10):", font=("Arial", 10)).pack(side=tk.LEFT)
    num_locations_entry = tk.Entry(num_locations_frame, width=5)
    num_locations_entry.insert(0, "4")
    num_locations_entry.pack(side=tk.LEFT)
    tk.Button(num_locations_frame, text="Set", command=lambda: create_coordinate_entries(num_locations_entry.get())).pack(side=tk.LEFT, padx=5)

    # Frame to hold dynamic coordinate entries
    coordinate_input_frame = tk.Frame(root, bd=2, relief="groove")
    coordinate_input_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    tk.Label(coordinate_input_frame, text="Enter Coordinates (x, y):", font=("Arial", 12, "bold")).pack(pady=5)

    # Initially create default 4 entries
    create_coordinate_entries(num_locations_entry.get())

    # Timing Input (Cycle Wait Time)
    tk.Label(root, text="Wait Time Between Cycles (seconds):", font=("Arial", 12, "bold")).pack(pady=10)
    timing_entry = tk.Entry(root, width=30)
    timing_entry.insert(0, str(cycle_wait_time)) # Use the renamed global variable
    timing_entry.pack(pady=5)

    # NEW: Timing Input (Click Wait Time)
    tk.Label(root, text="Wait Time Between Clicks (seconds):", font=("Arial", 12, "bold")).pack(pady=10)
    click_timing_entry = tk.Entry(root, width=30)
    click_timing_entry.insert(0, str(click_wait_time)) # Use the new global variable
    click_timing_entry.pack(pady=5)

    # Buttons
    start_button = tk.Button(root, text="Start Script", command=start_script,
                             bg="green", fg="white", font=("Arial", 12, "bold"))
    start_button.pack(pady=10, ipadx=20, ipady=10)

    stop_button = tk.Button(root, text="Stop Script", command=stop_script_gui,
                             bg="red", fg="white", font=("Arial", 12, "bold"))
    stop_button.pack(pady=5, ipadx=20, ipady=10)

    # Instructions
    tk.Label(root, text="To stop, click 'Stop Script', press 'q' key, or\nmove mouse to a corner (Fail-Safe).",
             font=("Arial", 10)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()