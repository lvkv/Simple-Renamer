import shutil
import os

RENAME_FILES = True
RENAME_DIRECTORIES = False
CURRENT_DIR = str(os.path.dirname(os.path.realpath(__file__)))
REPEAT_DIR = CURRENT_DIR + "\\Repeat_Dashed_Files"

folders = ["112","114","121","124","214","612","614"]

for folder in folders:    
    os.makedirs(CURRENT_DIR + "\\" + folder)
	
for file in os.scandir():
    if '-' in file.name:
        if (RENAME_FILES and os.path.isfile(file.name)) or (RENAME_DIRECTORIES and os.path.isdir(file.name)):
            if os.path.exists(file.name.replace('-', '_')):
                if not os.path.exists(REPEAT_DIR):
                    os.makedirs(REPEAT_DIR)
                shutil.move(file.name, REPEAT_DIR)
            else:  
                os.rename(file.name,file.name.replace('-', '_'))
				
for file in os.scandir():
	f = file.name.split("\\")[len(file.name.split("\\"))-1]
    for folder in folders:
        if f[:3] == folder:
            shutil.move(file.name, CURRENT_DIR + "\\" + folder)