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
        master.title("Simple Rename")

        # Entry validation
        self.previous_bad_validation = False
        self.bad_chars = ['\\', '/', '¦', '*', '?', '"', '<', '>', '|']
        vcmd = (master.register(self.onValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        # Initializing tabs and adding frames
        tabs = Notebook(master)
        rename_tab = Frame(width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT)
        tabs.add(rename_tab, text=self.TAB_NAMES[0])
        move_tab = Frame(width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT)
        tabs.add(move_tab, text=self.TAB_NAMES[1])
        tabs.bind_all("<<NotebookTabChanged>>", self.cycle_frame_text)
        tabs.grid()

        # "Rename Files" Tab - Variables
        self.completed_items = [False, False, False, False]  # choose dir, replace this, with this, >=1 checkbox
        self.dir_path = StringVar()
        self.replace_this = StringVar()
        self.with_this = StringVar()
        self.rename_files = BooleanVar()
        self.rename_dirs = BooleanVar()
        self.rename_subdirs = BooleanVar()
        self.rename_subfiles = BooleanVar()

        # "Rename Files" Tab - Creating GUI elements
        button_dir = Button(rename_tab, text="Choose Directory")
        self.label_txt_warn = Label(rename_tab, text='''Remember, a file/directory name can't contain:  \ / ¦ * ? " < > |''')
        self.label_blank = Label(rename_tab, text=" ")
        label_1 = Label(rename_tab, text="  Replace this:  ")
        label_2 = Label(rename_tab, text="  With this:  ")
        entry_1 = Entry(rename_tab, width=50, validate="key", validatecommand=vcmd)
        entry_2 = Entry(rename_tab, width=50, validate="key", validatecommand=vcmd)
        checkbox_files = Checkbutton(rename_tab,
                                     text="Rename files",
                                     variable=self.rename_files,
                                     onvalue=True,
                                     offvalue=False)
        checkbox_subfiles = Checkbutton(rename_tab,
                                        text="Rename subdirectory files",
                                        variable=self.rename_subfiles,
                                        onvalue=True,
                                        offvalue=False)
        checkbox_dirs = Checkbutton(rename_tab,
                                    text="Rename directories",
                                    variable=self.rename_dirs,
                                    onvalue=True,
                                    offvalue=False)
        checkbox_subdirs = Checkbutton(rename_tab,
                                       text="Rename subdirectories",
                                       variable=self.rename_subdirs,
                                       onvalue=True,
                                       offvalue=False)
        self.button_run_rename = Button(rename_tab, text="Run", state=DISABLED)

        # "Rename Files" Tab - Binding functions
        button_dir.bind('<Button-1>', self.choose_dir)
        self.button_run_rename.bind('<Button-1>', self.run_rename)
        checkbox_files.bind('<Button-1>', self.checkbox_complete)
        checkbox_subfiles.bind('<Button-1>', self.checkbox_complete)
        checkbox_subdirs.bind('<Button-1>', self.checkbox_complete)
        checkbox_subfiles.bind('<Button-1>', self.checkbox_complete)

        # "Rename Files" Tab - Gridding GUI elements
        button_dir.grid(columnspan=2)
        self.label_txt_warn.grid(columnspan=2, sticky=S)
        self.label_txt_warn.grid_remove()  # label_txtWarn is only shown when an illegal character is entered
        self.label_blank.grid(columnspan=2, sticky=S)
        label_1.grid(row=2, sticky=E)
        label_2.grid(row=3, sticky=E)
        entry_1.grid(row=2, column=1)
        entry_2.grid(row=3, column=1)
        checkbox_files.grid(columnspan=2)
        checkbox_subfiles.grid(columnspan=2)
        checkbox_dirs.grid(columnspan=2)
        checkbox_subdirs.grid(columnspan=2)
        self.button_run_rename.grid(columnspan=2)

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
                return
        self.button_run_rename.config(state='normal')

    def checkbox_complete(self, event):
        # INPUT: Window and left click event
        # OUTPUT: Marks a portion of the form complete if one or more boxes are checked
        #
        # No other elements use a check-if-this-form-element-is-complete method because that
        # functionality is already inside their respective bound functions

        if self.rename_files or self.rename_dirs or self.rename_subfiles or self.rename_subdirs:
            self.completed_items[3] = True
        self.check_for_completion()

    def choose_dir(self, event):
        # INPUT: Window and left click event
        # OUTPUT: Changes value of self.dir_path to path of folder selected in dialog box
        #
        # Included if statement to prevent setting self.dir_path = "" when user cancels dialog

        temp_dir = filedialog.askdirectory()
        if temp_dir != "":
            self.dir_path = temp_dir
            self.completed_items[0] = True
        self.check_for_completion()

    def run_rename(self, event):
        # INPUT:
        # OUTPUT:
        #
        # First if statement prevents running if user clicks on disabled button (why is that allowed?)

        if str(self.button_run_rename['state']) == 'disabled':
            return
        for file in os.walk():
            print(file)

    def cycle_frame_text(self, event):
        # INPUT: Window and <<NotebookTabChanged>> event
        # OUTPUT: Changes text on bottom of tab frame to the new tab's respective description
        #
        # Opted for an elif structure instead of creating a dictionary. If more tabs are
        # added, we'll swap this out for a dictionary.

        tab_text = event.widget.tab(event.widget.index("current"), "text")
        if tab_text == self.TAB_NAMES[0]:  # "Rename Files"
            self.label.configure(text="Find and replace words in file names")
        elif tab_text == "Move Files":  # "Move Files"
            self.label.configure(text="Move select files to specified folders")

    def onValidate(self, d, i, P, s, S, v, V, W):
        for character in self.bad_chars:
            if S == character:
                self.label_blank.grid_remove()
                self.label_txt_warn.grid()
                self.previous_bad_validation = True
                return False
        if self.previous_bad_validation:
            self.label_txt_warn.grid_remove()
            self.label_blank.grid()
            self.previous_bad_validation = False
        return True

root = Tk()
sr = SimpleRenamer(root)
root.mainloop()
