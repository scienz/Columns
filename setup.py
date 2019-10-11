from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = "C:\\python36\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\python36\\tcl\\tk8.6"

include_files= ['columns.png', 'name.png']
packages= ['pygame', 'game_logic']

setup(
    name= 'Columns by Cyan',
    description= 'Cyan\'s game',
    options= {'build_exe': {
        'packages': packages,
        'include_files': include_files}},
    executables = [Executable(
        "user_interface.py",
        base= "Win32GUI",
        icon= 'icon.ico',
        shortcutName= 'Columns by Cyan',
        shortcutDir= 'DesktopFolder')])
