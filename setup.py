import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': ['numpy.core._methods', 'numpy.lib.format', 'matplotlib.backends.backend_qt5agg', 'appdirs',
                     'packaging.version', 'packaging.specifiers', 'packaging.requirements',
                     'ui.generated', 'algorithm'],
        'excludes': ['gtk', 'PyQt4', 'wx', 'tkinter', 'setuptools', 'IPython', 'pytz']
    }
}

executables = [
    Executable('app.py', base=base)
]

setup(name='Data Structure',
      version='3.0',
      description='Edit, search and encode documents.',
      options=options,
      executables=executables
      )
