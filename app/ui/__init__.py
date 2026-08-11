"""UI package for the Proofreader application."""

from .centralwidget import CentralWidget
from .docmanager import DockManager
from .mainwindow import MainWindow
from .menubar import MenuBar
from .statusbar import StatusBar
from .theme import ThemeManager
from .toolbar import ToolBar

__all__ = [
    "CentralWidget",
    "DockManager",
    "MainWindow",
    "MenuBar",
    "StatusBar",
    "ThemeManager",
    "ToolBar",
]