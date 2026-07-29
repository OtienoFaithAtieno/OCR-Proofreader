"""
dock_manager.py

Creates and manages all dock widgets used by the application.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QListWidget,
    QTextEdit,
)


class DockManager:
    """
    Responsible for creating and managing dock widgets.
    """

    def __init__(self, main_window):
        self.main_window = main_window

    def create_docks(self):

        self._create_navigation_dock()
        self._create_properties_dock()

    # ---------------------------------------------------------

    def _create_navigation_dock(self):

        self.navigation_dock = QDockWidget(
            "Navigation",
            self.main_window
        )

        self.navigation_dock.setAllowedAreas(
            Qt.LeftDockWidgetArea
        )

        navigation = QListWidget()

        navigation.addItems([
            "Recent Files",
            "Pages",
            "Bookmarks",
            "OCR Layers",
            "Annotations",
            "Processing Queue",
        ])

        self.navigation_dock.setWidget(navigation)

        self.main_window.addDockWidget(
            Qt.LeftDockWidgetArea,
            self.navigation_dock
        )

    # ---------------------------------------------------------

    def _create_properties_dock(self):

        self.properties_dock = QDockWidget(
            "Properties",
            self.main_window
        )

        self.properties_dock.setAllowedAreas(
            Qt.RightDockWidgetArea
        )

        properties = QTextEdit()

        properties.setReadOnly(True)

        properties.setPlaceholderText(
            "Document properties\n\n"
            "Fonts\n"
            "Margins\n"
            "Styles\n"
            "Metadata\n"
            "OCR Confidence\n"
        )

        self.properties_dock.setWidget(properties)

        self.main_window.addDockWidget(
            Qt.RightDockWidgetArea,
            self.properties_dock
        )