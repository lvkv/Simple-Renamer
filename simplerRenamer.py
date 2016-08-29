from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
# import sys
import os


class SimpleRenamer:
    # To add a blank tab in the future, just add a new element to TAB_NAMES (and extra now)
    TAB_NAMES = ["Rename Files", "Move Files"]

    # All tabs will contain frames of the same size
    FRAME_WIDTH = 400
    FRAME_HEIGHT = 300

    def __init__(self, master):
        master.title("Simple Renamer")

        # Initializing tabs and adding frames
        tabs = Notebook(master)
        rename_tab = Frame(width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT)
        tabs.add(rename_tab, text=self.TAB_NAMES[0])
        move_tab = Frame(width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT)
        tabs.add(move_tab, text=self.TAB_NAMES[1])
        tabs.bind_all("<<NotebookTabChanged>>", self.cycle_frame_text)
        tabs.grid()

        # "Rename Files" Tab - Variables
        self.dir_path = StringVar()
        self.rename_files = BooleanVar()
        self.rename_dirs = BooleanVar()
        self.rename_subdirs = BooleanVar()
        self.rename_subfiles = BooleanVar()

        # "Rename Files" Tab - Creating GUI elements
        button_dir = Button(rename_tab, text="Choose Directory")
        label_txt_warn = Label(rename_tab, text='''Remember, a file/directory name can't contain:  \ / ¦ * ? " < > |''')
        label_1 = Label(rename_tab, text="  Replace this:  ")
        label_2 = Label(rename_tab, text="  With this:  ")
        entry_1 = Entry(rename_tab, width=50)
        entry_2 = Entry(rename_tab, width=50)
        checkbox_files = Checkbutton(rename_tab, text="Rename files")
        checkbox_dirs = Checkbutton(rename_tab, text="Rename directories")
        checkbox_subdirs = Checkbutton(rename_tab, text="Rename subdirectories")
        checkbox_subfiles = Checkbutton(rename_tab, text="Rename subdirectory files")
        button_run_rename = Button(rename_tab, text="Run", state=DISABLED)

        # "Rename Files" Tab - Binding functions
        button_dir.bind('<Button-1>', self.choose_dir)
        button_run_rename.bind('<Button-1>', self.run_rename)

        # "Rename Files" Tab - Gridding GUI elements
        button_dir.grid(columnspan=2)
        label_txt_warn.grid(columnspan=2, sticky=S)  # label_txtWarn is only shown when an illegal character is entered
        label_txt_warn.grid_remove()
        label_1.grid(row=2, sticky=E)
        label_2.grid(row=3, sticky=E)
        entry_1.grid(row=2, column=1)
        entry_2.grid(row=3, column=1)
        checkbox_files.grid(columnspan=2)
        checkbox_dirs.grid(columnspan=2)
        checkbox_subdirs.grid(columnspan=2)
        checkbox_subfiles.grid(columnspan=2)
        button_run_rename.grid(columnspan=2)

        # Text on bottom of window
        self.label = Label(master, text="")
        self.label.grid()

    def choose_dir(self, event):
        # INPUT: Window and left click event
        # OUTPUT: Changes value of self.dir_path to path of folder selected in dialog box
        #
        # Not much to say about this one

        self.dir_path = filedialog.askdirectory()

    def run_rename(self, event):
        # this is where the magic happens
        for file in os.walk():
            print(file)

    def cycle_frame_text(self, event):
        # INPUT: Window and <<NotebookTabChanged>> event
        # OUTPUT: Changes text on bottom of tab frame to the new tab's respective description
        #
        # Opted for an elif structure instead of creating a dictionary. If more tabs are
        # added, we'll swap this out for a dictionary.

        tab_text = event.widget.tab(event.widget.index("current"), "text")
        if tab_text == "Rename Files":
            self.label.configure(text="Find and replace words in file names")
        elif tab_text == "Move Files":
            self.label.configure(text="Move select files to specified folders")


root = Tk()
sr = SimpleRenamer(root)
root.mainloop()
