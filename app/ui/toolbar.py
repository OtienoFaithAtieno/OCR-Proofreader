"""
Toolbar for the Proofreader application.
"""
"""
tool_bar.py

Application toolbar.

This toolbar reuses QAction objects owned by the MenuBar.
"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QToolBar


class ToolBar(QToolBar):
    """Main application toolbar."""

    def __init__(self, main_window):
        super().__init__("Main Toolbar", main_window)

        self.main_window = main_window

        self.setObjectName("MainToolbar")

        self.setMovable(False)
        self.setFloatable(False)

        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.setIconSize(QSize(24, 24))

        self._build_toolbar()

    # ---------------------------------------------------------

    def _build_toolbar(self):

        menu = self.main_window.menu

        self.action_open = menu.action_open_pdf
        self.action_save = menu.action_save

        #
        # File
        #

        self.addAction(menu.action_new)
        self.addAction(menu.action_open_pdf)
        self.addAction(menu.action_save)

        self.addSeparator()

        #
        # Proofreading
        #

        self.addAction(menu.action_clean_document)
        self.addAction(menu.action_spell_check)
        self.addAction(menu.action_grammar_check)

        self.addSeparator()

        #
        # Export
        #

        self.addAction(menu.action_export_docx)
        self.addAction(menu.action_export_pdf)

        self.addSeparator()

        #
        # View
        #

        self.addAction(menu.action_toggle_theme)