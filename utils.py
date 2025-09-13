"""
This module contains the Utils class. The Utils class is a grouping of small and usefull functions.
"""
from tkinter.ttk import *
from tkinter import *
from PIL import Image, ImageTk
import pathlib, os
import inspect
if os.name == 'nt':
    import winsound
from re import sub
import csv

class Utils():
    """
    A static class grouping small and usefull functions.
    """
    @staticmethod
    def center_window(window):
        """
        Center a tkinter window
        Args:
            window (Tk): The window object.
        """
        window.update_idletasks()

        width = window.winfo_width()
        frm_width = window.winfo_rootx() - window.winfo_x()
        win_width = width + 2 * frm_width

        height = window.winfo_height()
        titlebar_height = window.winfo_rooty() - window.winfo_y()
        win_height = height + titlebar_height + frm_width

        x = window.winfo_screenwidth() // 2 - win_width // 2
        y = window.winfo_screenheight() // 2 - win_height // 2

        window.geometry(f'{width}x{height}+{x}+{y}')
        window.deiconify()

    @staticmethod
    def set_up_window(window, title, geometry, is_centered):
        window.title(title)
        window.geometry(geometry)
        if is_centered:
            Utils.center_window(window)

    @staticmethod
    def destroy_widget_children(widget):
        for child in widget.winfo_children():
            child.destroy()

    @staticmethod
    def play_sound(relative_path):
        """
        Play the sound asynchronously, only if the os is windows.
        Args:
            relative_path (str): The relative path to the audio file.
        """
        if os.name == 'nt':
            winsound.PlaySound(relative_path, winsound.SND_ASYNC)

    @staticmethod
    def open_image(relative_path, master, width = None, height = None):
        """
        Open and return an image.
        Args:
            relative_path (str): The relative path to the image.
            master (Widget): The master widget.
            width (int): The image's width.
            height (int): The image's height.
        Returns:
            A PhotoImage.
        """
        caller_frame = inspect.stack()[1]
        caller_path = pathlib.Path(caller_frame.filename).resolve()
        full_path = os.path.join(caller_path.parent, relative_path)
        img = Image.open(full_path)
        if (width and height) :
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img, master=master)
    
    @staticmethod
    def read_csv(file_path, sep=","):
        with open(file_path, 'r') as file:
            csv_file = csv.reader(file, delimiter=sep)
            output = list(csv_file)
        return output

    