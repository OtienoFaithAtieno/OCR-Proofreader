"""
UI package.

This package contains all graphical user interface components
for the Proofreader application.
"""

from .mainwindow import MainWindow
from .menubar import MenuBar
"""from .toolbar import ToolBar
from .statusbar import StatusBar
from .centralwidget import CentralWidget
from .docmanager import DockManager
from .theme import ThemeManager"""

__all__ = [
    "MainWindow",
    "MenuBar",
    "ToolBar",
    "StatusBar",
    "CentralWidget",
    "DockManager",
    "ThemeManager",
]