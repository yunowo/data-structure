import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': ['numpy.core._methods', 'numpy.lib.format', 'matplotlib.backends.backend_qt5agg', 'ui.generated'],
        'excludes': ['gtk', 'PyQt4', 'wx', 'tkinter', 'setuptools', 'IPython', 'pytz', 'PIL']
    }
}

executables = [
    Executable('app.py', base=base)
]

setup(name='Data Structure',
      version='0.1',
      description='Edit and search',
      options=options,
      executables=executables
      )
