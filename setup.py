import sys
import os
from cx_Freeze import setup, Executable

# Replace 'your_script.py' with the name of your Python script
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

icon_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')

executables = [Executable('GPA Gui.py', base=base, icon=icon_file)]

setup(name='GPA Calculator',
      version='1.0',
      description='This program helps to calculate your GPA',
      executables=executables)

# import os
# from cx_Freeze import setup, Executable
#
# # Get the absolute path of the icon file
#
#
# # Specify the list of executables
# executables = [Executable('GPA Gui.py', base=None, icon=icon_file)]
#
# # Additional options for the setup
# build_options = {
#     'build_exe': {
#         'include_files': [icon_file],  # Include the icon file in the build directory
#         'optimize': 2,  # Optional: optimize the generated bytecode
#     },
# }
#
# # Setup configuration
# setup(
#     name='GPA Calculator',
#     version='1.0',
#     description='This program helps to calculate your GPA',
#     options=build_options,
#     executables=executables
# )
