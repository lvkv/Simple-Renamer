from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import sys
import os

class SimpleRenamer:
    #To add a blank tab in the future, just add a new element to TAB_NAMES
    TAB_NAMES = ["Rename Files","Move Files"]
    
    #All tabs will contain frames of the same size
    FRAME_WIDTH = 400
    FRAME_HEIGHT = 300
    
    def __init__(self):
        root = Tk()
        root.title("Simple Renamer")
     
        #Initializing tabs and adding frames
        tabs = Notebook(root)
        for tab in self.TAB_NAMES:
            tabs.add(Frame(width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT), text=tab)
        tabs.bind_all("<<NotebookTabChanged>>", self.cycle_WindowText)
        tabs.pack()
        
        #Text on bottom of window
        self.label = Label(root, text="")
        self.label.pack()
        
        root.mainloop()
        
    def cycle_WindowText(self, event):
        #INPUT: Window and <<NotebookTabChanged>> event
        #OUTPUT: Changes text on bottom of window to the new tab's respective description
        #
        #Opted for an elif structure instead of creating a dictionary if more tabs are 
        #added, we'll swap this out for a dictionary.
        
        tab_text = event.widget.tab(event.widget.index("current"), "text")
        if (tab_text == "Rename Files"):
            self.label.configure(text="Find and replace words in file names")
        elif (tab_text == "Move Files"):
            self.label.configure(text="Move select files to specified folders")
        
                        
def main():
    window = SimpleRenamer()

main()
