"""
GUI utilities module for the Bela card game.

This module contains helper functions for creating and managing tkinter widgets
with consistent styling throughout the application.
"""

from tkinter import *
from PIL import Image, ImageTk


# Styling constants
PRIMARY_COLOR = "#20bebe"
FONT = ("Cascadia Code", 18)
BOLD_FONT = ("Cascadia Code", 18, "bold")
TITLE_FONT = ("Cascadia Code", 32, "bold")


def sleep(window, duration):
    """
    Pauses execution for a specified duration in the GUI thread.

    Args:
        window: The tkinter window to bind the sleep to
        duration: Time to sleep in milliseconds (currently hardcoded to 2500ms)
    """
    print("waiting...")
    if isinstance(duration, int):
        temp_var = IntVar()
        window.after(2500, lambda: temp_var.set(1))
        window.wait_variable(temp_var)
    print("waiting done")
    return


def create_game_label(window, text):
    """
    Creates a label with the game's standard font and color.

    Args:
        window: Parent tkinter window
        text: Text to display in the label

    Returns:
        tkinter.Label with styled appearance
    """
    return Label(window, text=text, font=FONT, fg=PRIMARY_COLOR, pady=15)


def create_title_label(window, text):
    """
    Creates a title label with the game's title font and color.

    Args:
        window: Parent tkinter window
        text: Text to display in the title

    Returns:
        tkinter.Label with styled title appearance
    """
    return Label(window, text=text, font=TITLE_FONT, fg=PRIMARY_COLOR)


def create_styled_button(window, text, command):
    """
    Creates a button with the game's standard styling.

    Args:
        window: Parent tkinter window
        text: Text to display on the button
        command: Function to call when button is clicked

    Returns:
        tkinter.Button with styled appearance
    """
    return Button(
        window,
        text=text,
        font=FONT,
        bg=PRIMARY_COLOR,
        fg="#fff",
        activebackground='#eee',
        activeforeground='#10aeae',
        command=command
    )


def create_styled_entry(window, width=10):
    """
    Creates an entry widget with the game's standard styling.

    Args:
        window: Parent tkinter window
        width: Width of the entry widget (default 10)

    Returns:
        tkinter.Entry with styled appearance
    """
    return Entry(window, width=width, font=FONT, fg=PRIMARY_COLOR)


def get_all_child_widgets(window):
    """
    Recursively gets all child widgets from a window.

    Args:
        window: The parent tkinter window

    Returns:
        List of all child widgets (including nested children)
    """
    widgets = window.winfo_children()

    for widget in widgets:
        if widget.winfo_children():
            widgets.extend(widget.winfo_children())

    return widgets


def destroy_widget(widget):
    """
    Safely destroys a widget if it's not a top-level window.

    Args:
        widget: The tkinter widget to destroy
    """
    try:
        if widget.winfo_class() != "Toplevel":
            widget.destroy()
    except Exception:
        pass  # Widget may already be destroyed


def clear_window(window):
    """
    Clears all child widgets from a window except the first two (typically canvas and background).

    Args:
        window: The tkinter window to clear
    """
    # Skip first two widgets (usually canvas and background) when clearing
    [destroy_widget(widget) for widget in get_all_child_widgets(window)[2:]]


def load_image(window, path, width=0, height=0):
    """
    Loads and optionally resizes an image for use in tkinter.

    Args:
        window: Parent tkinter window (not used directly but kept for compatibility)
        path: Path to the image file
        width: Target width for resizing (optional)
        height: Target height for resizing (optional)

    Returns:
        ImageTk.PhotoImage object ready for use in tkinter widgets
    """
    image = Image.open(path)
    if width and height:
        image = image.resize((width, height), Image.LANCZOS)
    image = ImageTk.PhotoImage(image)
    return image


def create_image_label(window, path, width=0, height=0):
    """
    Creates a label containing an image.

    Args:
        window: Parent tkinter window
        path: Path to the image file
        width: Target width for resizing (optional)
        height: Target height for resizing (optional)

    Returns:
        tkinter.Label containing the image
    """
    image = load_image(window, path, width, height)
    image_label = Label(image=image)
    image_label.image = image  # Keep a reference to prevent garbage collection
    return image_label


def create_image_button(window, path, width=0, height=0, command=lambda: None):
    """
    Creates a button with an image background.

    Args:
        window: Parent tkinter window
        path: Path to the image file
        width: Target width for resizing (optional)
        height: Target height for resizing (optional)
        command: Function to call when button is clicked

    Returns:
        tkinter.Button with image background
    """
    image = load_image(window, path, width, height)
    button = Button(
        window,
        image=image,
        font=FONT,
        bg=PRIMARY_COLOR,
        fg="#fff",
        activebackground='#eee',
        activeforeground='#10aeae',
        command=command
    )
    button.image = image  # Keep a reference to prevent garbage collection
    return button