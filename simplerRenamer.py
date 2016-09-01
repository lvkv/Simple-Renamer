# Simple Script
# Lukas Velikov
#
# Simple Script is a GUI app designed to make quick and simple mass file renames and relocations possible to clients
# without scripting experience. Built using Python's Tkinter package. Included imports for Python 2.x, but not tested.

try:
    from tkinter import *  # Python 3.x
except ImportError:
    from Tkinter import *  # Python 2.x
from tkinter import filedialog
from tkinter.ttk import *
# import sys #for shutil file moves
import os


class SimpleRenamer:

    TAB_NAMES = ["Rename Files", "Move Files"]

    # All tabs will contain frames of the same size
    FRAME_WIDTH = 400
    FRAME_HEIGHT = 250

    def __init__(self, master):
        master.title("Simple Rename")

        # Entry validation
        self.previous_bad_validation = False
        self.bad_chars = ['\\', '/', '¦', '*', '?', '"', '<', '>', '|']
        vcmd = (master.register(self.on_validate), '%S')

        # Initializing tabs and adding frames
        tabs = Notebook(master)
        rename_tab = Frame(width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT)

        rename_tab.grid_rowconfigure(0, weight=1)
        rename_tab.grid_rowconfigure(2, weight=1)
        rename_tab.grid_rowconfigure(3, weight=1)
        rename_tab.grid_rowconfigure(4, weight=1)
        rename_tab.grid_rowconfigure(5, weight=1)
        rename_tab.grid_rowconfigure(6, weight=1)
        rename_tab.grid_rowconfigure(7, weight=2)

        tabs.add(rename_tab, text=self.TAB_NAMES[0])
        move_tab = Frame(width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT)
        tabs.add(move_tab, text=self.TAB_NAMES[1])
        tabs.bind_all("<<NotebookTabChanged>>", self.cycle_frame_text)
        tabs.grid()

        # "Rename Files" Tab - Variables
        self.completed_items = [False, False, False]  # choose dir, replace this, >=1 checkbox
        self.dir_path = StringVar()
        self.replace_this = StringVar()
        self.with_this = StringVar()
        self.rename_files = BooleanVar()
        self.rename_files.set(True)
        self.rename_subfiles = BooleanVar()
        self.rename_dirs = BooleanVar()
        self.rename_subdirs = BooleanVar()

        # "Rename Files" Tab - Creating GUI elements
        button_dir = Button(rename_tab, text="Choose Directory")

        self.rename_frame = LabelFrame(rename_tab, text="Find and Replace")
        self.label_txt_warn = Label(self.rename_frame,
                                    text='''Remember, a file/directory name can't contain:  \ / ¦ * ? " < > |''')
        self.label_blank = Label(self.rename_frame, text=" ")
        label_1 = Label(self.rename_frame, text="  Replace this:  ")
        label_2 = Label(self.rename_frame, text="  With this:  ")
        self.entry_replace_this = Entry(self.rename_frame, width=50, validate="key", validatecommand=vcmd)
        self.entry_with_this = Entry(self.rename_frame, width=50, validate="key", validatecommand=vcmd)

        self.rename_options_frame = LabelFrame(rename_tab, text="Options")
        self.checkbox_files = Checkbutton(self.rename_options_frame,
                                          text="Rename files",
                                          onvalue=True,
                                          offvalue=False,
                                          variable=self.rename_files)
        self.checkbox_subfiles = Checkbutton(self.rename_options_frame,
                                             text="Rename subdirectory files",
                                             onvalue=True,
                                             offvalue=False,
                                             variable=self.rename_subfiles)
        self.checkbox_dirs = Checkbutton(self.rename_options_frame,
                                         text="Rename directories",
                                         onvalue=True,
                                         offvalue=False,
                                         variable=self.rename_dirs)
        self.checkbox_subdirs = Checkbutton(self.rename_options_frame,
                                            text="Rename subdirectories",
                                            onvalue=True,
                                            offvalue=False,
                                            variable=self.rename_subdirs)
        self.button_run_rename = Button(rename_tab, text="Run", state=DISABLED)

        # "Rename Files" Tab - Binding functions
        button_dir.bind('<Button-1>', self.choose_dir)
        self.button_run_rename.bind('<Button-1>', self.run_rename)
        self.entry_replace_this.bind('<KeyRelease>', self.update_replace_this)
        self.entry_with_this.bind('<KeyRelease>', self.update_with_this)
        self.checkbox_files.bind('<Button-1>', self.checkbox_complete)
        self.checkbox_subfiles.bind('<Button-1>', self.checkbox_complete)
        self.checkbox_subdirs.bind('<Button-1>', self.checkbox_complete)
        self.checkbox_subfiles.bind('<Button-1>', self.checkbox_complete)

        # "Rename Files" Tab - Gridding GUI elements
        button_dir.grid(columnspan=2)

        self.rename_frame.grid(columnspan=2)
        self.label_txt_warn.grid(columnspan=2, row=1, sticky=S)
        self.label_txt_warn.grid_remove()  # label_txtWarn is only visible when an illegal character is entered
        self.label_blank.grid(columnspan=2, row=1, sticky=S)
        label_1.grid(row=2, sticky=E)
        label_2.grid(row=3, sticky=E)

        self.entry_replace_this.grid(row=2, column=1)
        self.entry_with_this.grid(row=3, column=1)

        self.rename_options_frame.grid(columnspan=2)
        self.checkbox_files.grid(row=4, columnspan=2)
        self.checkbox_subfiles.grid(row=5, columnspan=2)
        self.checkbox_dirs.grid(row=6, columnspan=2)
        self.checkbox_subdirs.grid(row=7, columnspan=2)
        self.button_run_rename.grid(row=8, columnspan=2)

        # Text on bottom of window
        self.label = Label(master, text="")
        self.label.grid()

    def check_for_completion(self):
        # INPUT: Nothing
        # OUTPUT: If every element in self.completed_items is true, allows user to click "Run"
        #
        # Nothing much to say about this method

        for item in self.completed_items:
            if not item:
                self.button_run_rename.config(state=DISABLED)
                return
        self.button_run_rename.config(state='normal')

    def checkbox_complete(self, event):
        # INPUT: Window and left click event
        # OUTPUT: Marks a portion of the form complete if one or more boxes are checked
        #
        # No other elements use a check-if-this-form-element-is-complete method because that
        # functionality is already inside their respective bound functions

        if self.rename_files or self.rename_dirs or self.rename_subfiles or self.rename_subdirs:
            self.completed_items[2] = True
        else:
            self.completed_items[2] = False
        self.check_for_completion()

    def choose_dir(self, event):
        # INPUT: Window and left click event
        # OUTPUT: Changes value of self.dir_path to path of folder selected in dialog box
        #
        # Included if statement to prevent setting self.dir_path = "" when user cancels dialog

        temp_dir = filedialog.askdirectory()
        if temp_dir != "":
            self.dir_path.set(temp_dir)
            self.completed_items[0] = True
        else:
            self.completed_items[0] = False
        self.check_for_completion()

    def run_rename(self, event):
        # INPUT: <Button-1> left mouse click event
        # OUTPUT:
        #
        # First if statement prevents execution if user clicks on button in disabled state (why is that allowed?)
        # This is the functional part of the "Rename Files" tab. The part that actually does stuff.

        if str(self.button_run_rename['state']) == 'disabled':
            return
        if (not self.rename_subdirs.get()) and (not self.rename_subfiles.get()):  # Only doing root directory
            for f in os.scandir(self.dir_path.get()):
                file = self.dir_path.get() + "\\" + f.name
                if (self.rename_dirs.get() and os.path.isdir(file)) or (self.rename_files.get() and os.path.isfile(file)):
                    os.rename(file, (self.dir_path.get()+"\\"+(f.name.replace(self.replace_this.get(), self.with_this.get()))))
        else:  # Doing subdirectories     
            for tup in os.walk(self.dir_path):
                for lst in tup:
                    for file in lst:
                        print(file)

    def cycle_frame_text(self, event):
        # INPUT: Window and <<NotebookTabChanged>> event
        # OUTPUT: Changes text on bottom of tab frame to the new tab's respective description
        #
        # Opted for an elif structure instead of creating a dictionary. If more tabs are
        # added, we'll swap this out for a dictionary.

        tab_text = event.widget.tab(event.widget.index("current"), "text")
        if tab_text == self.TAB_NAMES[0]:  # "Rename Files"
            self.label.configure(text="Find and replace phrases in file names")
        elif tab_text == "Move Files":  # "Move Files"
            self.label.configure(text="Move select files to specified folders")

    def update_replace_this(self, event):
        self.check_rename_entries(event)
        self.replace_this.set(self.entry_replace_this.get())

    def update_with_this(self, event):
        self.check_rename_entries(event)
        self.with_this.set(self.entry_with_this.get())

    def check_rename_entries(self, event):
        # INPUT: <Key-Released> event
        # OUTPUT:
        #
        #

        if self.entry_replace_this.get() != '':
            self.completed_items[1] = True
        else:
            self.completed_items[1] = False
        self.check_for_completion()

    def flip_warnings(self, on_top):
        if on_top:
            self.label_blank.grid_remove()
            self.label_txt_warn.grid()
            self.previous_bad_validation = True
        else:
            self.label_txt_warn.grid_remove()
            self.label_blank.grid()
            self.previous_bad_validation = False


    def on_validate(self, s):
        # INPUT: String input to entry
        # OUTPUT: Returns true and sets self.previous_bad_validation = False if
        #
        # Also swaps warning label and blank

        for character in self.bad_chars:
            for substring in s:
                if substring == character:
                    self.flip_warnings(True)
                    return False
        if self.previous_bad_validation:
            self.flip_warnings(False)
        return True


root = Tk()
sr = SimpleRenamer(root)
root.mainloop()
