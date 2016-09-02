# Simple Script
# Lukas Velikov
#
# Simple Script is a GUI app designed to make quick and simple mass file renames and relocations possible to clients
# without scripting experience. Built using Python's Tkinter package.

from tkinter import *  # Python 3.x
from tkinter import filedialog
from tkinter.ttk import *
import sys  # for shutil file moves
import os


class SimpleScript:
    TAB_NAMES = ["Rename Files", "Move Files"]

    # All tabs will contain frames of the same size
    FRAME_WIDTH = 400
    FRAME_HEIGHT = 250

    successful_rename = "File/directory rename successful."
    successful_move = "File/directory relocation successful."
    error_renamed_exists = "Renamed file already exists: "

    def __init__(self, master):
        master.title("Simple Script")
        master.resizable(0, 0)

        # Entry validation
        self.previous_bad_validation = False
        self.bad_chars = ['\\', '/', '¦', '*', '?', '"', '<', '>', '|']
        vcmd = (master.register(self.on_validate), '%S')

        # Initializing tabs and adding frames
        tabs = Notebook(master)
        rename_tab = Frame(width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT)
        tabs.add(rename_tab, text=self.TAB_NAMES[0])
        move_tab = Frame(width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT)
        tabs.add(move_tab, text=self.TAB_NAMES[1])
        tabs.bind_all("<<NotebookTabChanged>>", self.cycle_frame_text)
        tabs.grid()

        # "Rename Files" Tab - Variables
        self.completed_items = [False, False, True]  # choose dir, replace this, >=1 checkbox (one is already checked)
        self.dir_path = StringVar()
        self.replace_this = StringVar()
        self.with_this = StringVar()
        self.rename_files = BooleanVar()
        self.rename_files.set(False)
        self.rename_subfiles = BooleanVar()
        self.rename_subfiles.set(False)
        self.rename_dirs = BooleanVar()
        self.rename_dirs.set(False)
        self.rename_subdirs = BooleanVar()
        self.rename_subdirs.set(False)

        # "Move Files" Tab - Variables
        self.completed_move_items = [False, False, True]  # choose source, destination, radio buttons
        self.dir_path_move = StringVar()
        self.dir_path_move_to = StringVar()
        self.pre_suf_cont = IntVar()
        self.starts_with = StringVar()
        self.ends_with = StringVar()
        self.contains = StringVar()
        self.move_files_here = StringVar()

        # "Rename Files" Tab - Creating GUI elements
        button_dir = Button(rename_tab, text="Choose Directory")
        self.rename_frame = LabelFrame(rename_tab, text="Find and Replace")
        self.label_txt_warn = Label(self.rename_frame,
                                    text='''File/directory names cannot contain:  \  /  ¦  *  ?  "  <  >  |''')
        self.label_txt_warn.config(foreground='red')
        self.label_blank = Label(self.rename_frame, text=" ")
        label_1 = Label(self.rename_frame, text="  Replace this:  ")
        label_2 = Label(self.rename_frame, text="  With this:  ")
        self.entry_replace_this = Entry(self.rename_frame, width=50, validate='key', validatecommand=vcmd)
        self.entry_with_this = Entry(self.rename_frame, width=50, validate='key', validatecommand=vcmd)
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

        # "Move Files" Tab - Creating GUI elements
        self.choose_move_dir_frame = LabelFrame(move_tab, text="From this directory...")
        self.button_dir_move = Button(self.choose_move_dir_frame, text='Choose Source Directory')
        self.button_dir_move_to = Button(move_tab, text='Choose Destination Directory')
        self.prefix_suffix_frame = LabelFrame(move_tab, text="Move files with names that...")
        self.radio_starts_with = Radiobutton(self.prefix_suffix_frame, text="Start with ", variable=self.pre_suf_cont,
                                             value=0)
        self.radio_ends_with = Radiobutton(self.prefix_suffix_frame, text="End with ", variable=self.pre_suf_cont,
                                           value=1)
        self.radio_contains = Radiobutton(self.prefix_suffix_frame, text="Contain ", variable=self.pre_suf_cont,
                                          value=2)
        self.label_move_blank = Label(self.prefix_suffix_frame, text="")
        self.label_txt_warn_move = Label(self.prefix_suffix_frame,
                                         text='''File/directory names cannot contain:  \  /  ¦  *  ?  "  <  >  |''')
        self.label_txt_warn_move.config(foreground='red')
        self.entry_pre_suf_cont = Entry(self.prefix_suffix_frame, width=62, validate='key', validatecommand=vcmd)

        # "Rename Files" Tab - Binding functions
        button_dir.bind('<Button-1>', self.choose_dir)
        self.button_run_rename.bind('<Button-1>', self.run_rename)
        self.entry_replace_this.bind('<KeyRelease>', self.update_replace_this)
        self.entry_with_this.bind('<KeyRelease>', self.update_with_this)
        self.checkbox_files.bind('<ButtonRelease-1>', self.set_rename_files)
        self.checkbox_subfiles.bind('<ButtonRelease-1>', self.set_rename_subfiles)
        self.checkbox_dirs.bind('<ButtonRelease-1>', self.set_rename_dirs)
        self.checkbox_subdirs.bind('<ButtonRelease-1>', self.set_rename_subdirs)

        # "Move Files" Tab - Binding functions
        self.button_dir_move.bind('<Button-1>', self.choose_dir_move)
        self.button_dir_move_to.bind('<Button-1>', self.choose_dir_move_destination)

        # "Rename Files" Tab - Gridding GUI elements
        button_dir.grid(columnspan=2, pady=(10, 2))
        self.rename_frame.grid(columnspan=2, padx=(5, 5))
        self.label_txt_warn.grid(columnspan=2, row=1, pady=(0, 5), sticky=S)
        self.label_txt_warn.grid_remove()  # label_txtWarn is only visible when an illegal character is entered
        self.label_blank.grid(columnspan=2, row=1, pady=(0, 5), sticky=S)
        label_1.grid(row=2, sticky=E, pady=(0, 10))
        label_2.grid(row=3, sticky=E, pady=(0, 20))
        self.entry_replace_this.grid(row=2, column=1, pady=(0, 10))
        self.entry_with_this.grid(row=3, column=1, pady=(0, 20))
        self.rename_options_frame.grid(row=4, column=0, padx=(5, 0), pady=(0, 5), sticky=W)
        self.checkbox_files.grid(row=4, column=0, sticky=W)
        self.checkbox_subfiles.grid(row=5, column=0, sticky=W)
        self.checkbox_dirs.grid(row=6, column=0, sticky=W)
        self.checkbox_subdirs.grid(row=7, column=0, sticky=W)
        self.button_run_rename.grid(column=1, row=4, sticky=W)

        # "Move Files" Tab - Gridding GUI elements
        self.choose_move_dir_frame.grid(row=0)
        self.button_dir_move.grid(column=0, row=0, pady=(10, 2))
        self.prefix_suffix_frame.grid(column=0, row=1, padx=(5, 5))
        self.radio_starts_with.grid(row=0, column=0)
        self.radio_ends_with.grid(row=0, column=1)
        self.radio_contains.grid(row=0, column=2)
        self.label_txt_warn_move.grid(row=1, columnspan=3)
        self.label_txt_warn_move.grid_remove()
        self.label_move_blank.grid(row=1, columnspan=3)
        self.entry_pre_suf_cont.grid(row=2, columnspan=3, padx=(5, 5), pady=(0, 20))
        self.button_dir_move_to.grid(column=0, row=2, pady=(10, 2))

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

    def check_for_move_complete(self):
        for item in self.completed_move_items:
            if not item:
                # disable that second run button
                return
                # enable that second run button

    def set_rename_files(self, event):
        self.rename_files.set(not self.rename_files.get())
        self.checkbox_complete(event)
        self.rename_files.set(not self.rename_files.get())

    def set_rename_subfiles(self, event):
        self.rename_subfiles.set(not self.rename_subfiles.get())
        self.checkbox_complete(event)
        self.rename_subfiles.set(not self.rename_subfiles.get())

    def set_rename_dirs(self, event):
        self.rename_dirs.set(not self.rename_dirs.get())
        self.checkbox_complete(event)
        self.rename_dirs.set(not self.rename_dirs.get())

    def set_rename_subdirs(self, event):
        self.rename_subdirs.set(not self.rename_subdirs.get())
        self.checkbox_complete(event)
        self.rename_subdirs.set(not self.rename_subdirs.get())

    def checkbox_complete(self, event):
        # INPUT: Window and left click event
        # OUTPUT: Marks a portion of the form complete if one or more boxes are checked
        #
        # No other elements use a check-if-this-form-element-is-complete method because that
        # functionality is already inside their respective bound functions

        if self.rename_files.get() or self.rename_dirs.get() or self.rename_subfiles.get() or self.rename_subdirs.get():
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

    def choose_dir_move(self, event):
        temp_dir = filedialog.askdirectory()
        if temp_dir != "":
            self.dir_path_move.set(temp_dir)
            self.completed_move_items[0] = True
        else:
            self.completed_move_items[0] = False
        self.check_for_move_complete()

    def choose_dir_move_destination(self, event):
        temp_dir = filedialog.askdirectory()
        if temp_dir != "":
            self.dir_path_move_to.set(temp_dir)
            self.completed_move_items[1] = True
        else:
            self.completed_move_items[1] = False
        self.check_for_move_complete()

    def run_rename(self, event):
        # INPUT: <Button-1> left mouse click event
        # OUTPUT:
        #
        # First if statement prevents execution if user clicks on button in disabled state (why is that allowed?)
        # This is the functional part of the "Rename Files" tab. The part that actually does stuff.

        if str(self.button_run_rename['state']) == 'disabled':
            return
        if (not self.rename_subdirs.get()) and (not self.rename_subfiles.get()):  # Only doing root directory
            error_messages = []
            error_count = 0
            for f in os.scandir(self.dir_path.get()):
                file = self.dir_path.get() + "\\" + f.name
                if (self.rename_dirs.get() and os.path.isdir(file)) or (
                    self.rename_files.get() and os.path.isfile(file)):
                    mod = self.dir_path.get() + "\\" + f.name.replace(self.replace_this.get(), self.with_this.get())
                    if os.path.exists(mod):
                        error_messages.append(self.error_renamed_exists+mod+'\n')
                        error_count += 1
                    else:
                        os.rename(file, mod)
            if error_count != 0:
                self.error_handle(error_messages)
            else:
                self.popup_window(self.successful_process)
        else:  # Doing subdirectories
            for path, dirs, files in os.walk(self.dir_path.get()):
                if self.rename_files and path == self.dir_path.get():
                    self.walk_rename(files, path)
                if self.rename_subfiles and path != self.dir_path.get():
                    self.walk_rename(files, path)
                if self.rename_dirs and path == self.dir_path.get():
                    self.walk_rename(dirs, path)
                if self.rename_subdirs and path != self.dir_path.get():
                    self.walk_rename(dirs, path)

    def run_move(self, event):
        do_stuff = "yes"

    def walk_rename(self, iterator, path):
        error_messages = []
        error_count = 0
        for item in iterator:
            full_path = path + "\\" + item
            modified_path = path + "\\" + item.replace(self.replace_this.get(), self.with_this.get())
            if os.path.exists(modified_path):
                error_messages.append(self.error_renamed_exists+modified_path+'\n')
                error_count += 1
            else:
                os.rename(full_path, modified_path)
        if error_count != 0:
            self.error_handle(error_messages)
        else:
            self.popup_window(self.successful_process)

    def error_handle(self, message_bank):
        error_message = "The following " + str(len(message_bank)) + 'error(s) have occurred:\n'
        for error in message_bank:
            error_message += error
        self.popup_window(error_message)

    def cycle_frame_text(self, event):
        # INPUT: Window and <<NotebookTabChanged>> event
        # OUTPUT: Changes text on bottom of tab frame to the new tab's respective description
        #
        # Opted for an elif structure instead of creating a dictionary. If more tabs are
        # added, we'll swap this out for a dictionary.

        tab_text = event.widget.tab(event.widget.index("current"), "text")
        if tab_text == self.TAB_NAMES[0]:  # "Rename Files"
            self.label.configure(text="Find and replace phrases in file/directory names")
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
            self.label_move_blank.grid_remove()
            self.label_blank.grid_remove()
            self.label_txt_warn_move.grid()
            self.label_txt_warn.grid()
            self.previous_bad_validation = True
        else:
            self.label_txt_warn_move.grid_remove()
            self.label_txt_warn.grid_remove()
            self.label_move_blank.grid()
            self.label_blank.grid()
            self.previous_bad_validation = False

    def popup_window(self, message):
        top_level = Toplevel()
        message_label = Label(top_level, text=message)
        message_label.grid(padx=(10, 10), pady=(10, 10))

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
sr = SimpleScript(root)
root.mainloop()
