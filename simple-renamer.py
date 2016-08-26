from tkinter import *
from tkinter import filedialog
import os

DIR_PATH = ""
RENAME_FILES = True
RENAME_DIRS = False
#RENAME_SUBFILES = False
#RENAME_SUBDIRS = False
replaceThis = ""
withThis = ""

def chooseDir():
        DIR_PATH = filedialog.askdirectory()

def toggle_RNfiles():
        RENAME_FILES

root = Tk()
root.wm_title("Simple Rename")
root.resizable(0,0)
    
button_dir = Button(root, text="Choose Directory", command=chooseDir)
label_txtWarn = Label(root, text='''Remember, a file/directory name can't contain:  \ / ¦ * ? " < > |''')
label_1 = Label(root, text="  Replace this:  ")
label_2 = Label(root, text="  With this:  ")
entry_1 = Entry(root, width=50)
entry_2 = Entry(root, width=50)
checkb_files = Checkbutton(root, text="Rename files")
checkb_dirs = Checkbutton(root, text="Rename directories")
#check_files = CheckButton(root, text="Rename subdirectory files")
#check_files = CheckButton(root, text="Rename subdirectory directories")
button_run = Button(root, text="Run", state=DISABLED)

button_dir.grid(columnspan=2)
label_txtWarn.grid(columnspan=2, sticky=S)
label_1.grid(row=2, sticky=E)
label_2.grid(row=3, sticky=E)
entry_1.grid(row=2, column=1)
entry_2.grid(row=3, column=1)
checkb_files.grid(columnspan=2)
checkb_dirs.grid(columnspan=2)
button_run.grid(columnspan=2)

root.mainloop()

for file in os.scandir(DIR_PATH):
        if((RENAME_FILES and os.path.isfile(file.name)) or (RENAME_DIRS and os.path.isdir(file.name))):
                os.rename(file.name, file.name.replace(replaceThis, withThis))
