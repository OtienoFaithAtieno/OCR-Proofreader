"""

Application menu bar.

The MenuBar owns all QAction objects used throughout the
application. Other UI components (ToolBar, MainWindow, etc.)
reuse these actions instead of creating duplicates.
"""

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMenuBar


class MenuBar(QMenuBar):
    """Application menu bar."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self._create_actions()
        self._create_menus()

    # ---------------------------------------------------------
    # Actions
    # ---------------------------------------------------------

    def _create_actions(self):
        """Create all application actions."""

        #
        # File
        #

        self.action_new = QAction("&New Project", self)
        self.action_new.setShortcut(QKeySequence.New)
        self.action_new.setStatusTip("Create a new project")

        self.action_open_pdf = QAction("Open &PDF...", self)
        self.action_open_pdf.setShortcut("Ctrl+Shift+O")
        self.action_open_pdf.setStatusTip("Open a PDF document")

        self.action_open_docx = QAction("Open &Word...", self)
        self.action_open_docx.setStatusTip("Open a Word document")

        self.action_save = QAction("&Save", self)
        self.action_save.setShortcut(QKeySequence.Save)
        self.action_save.setStatusTip("Save current document")

        self.action_save_as = QAction("Save &As...", self)
        self.action_save_as.setShortcut(QKeySequence.SaveAs)

        self.action_export = QAction("&Export...", self)
        self.action_export.setShortcut("Ctrl+E")
        self.action_export.setStatusTip("Export document")

        self.action_exit = QAction("E&xit", self)
        self.action_exit.setShortcut(QKeySequence.Quit)

        #
        # Edit
        #

        self.action_undo = QAction("&Undo", self)
        self.action_undo.setShortcut(QKeySequence.Undo)

        self.action_redo = QAction("&Redo", self)
        self.action_redo.setShortcut(QKeySequence.Redo)

        self.action_cut = QAction("Cu&t", self)
        self.action_cut.setShortcut(QKeySequence.Cut)

        self.action_copy = QAction("&Copy", self)
        self.action_copy.setShortcut(QKeySequence.Copy)

        self.action_paste = QAction("&Paste", self)
        self.action_paste.setShortcut(QKeySequence.Paste)

        self.action_find = QAction("&Find", self)
        self.action_find.setShortcut(QKeySequence.Find)

        #
        # View
        #

        self.action_zoom_in = QAction("Zoom &In", self)
        self.action_zoom_in.setShortcut(QKeySequence.ZoomIn)

        self.action_zoom_out = QAction("Zoom &Out", self)
        self.action_zoom_out.setShortcut(QKeySequence.ZoomOut)

        self.action_reset_zoom = QAction("&Reset Zoom", self)
        self.action_reset_zoom.setShortcut("Ctrl+0")

        self.action_toggle_theme = QAction("Toggle Dark Theme", self)
        self.action_toggle_theme.setCheckable(True)

        self.action_fullscreen = QAction("Full Screen", self)
        self.action_fullscreen.setShortcut("F11")

        self.action_detect_tables = QAction("Detect Tables", self)

        self.action_detect_images = QAction("Detect Images", self)

        #
        # Proofreading
        #

        self.action_clean_document = QAction(
            "Clean Formatting",
            self,
        )

        self.action_spell_check = QAction(
            "Spell Check",
            self,
        )

        self.action_grammar_check = QAction(
            "Grammar Check",
            self,
        )

        self.action_normalize_fonts = QAction(
            "Normalize Fonts",
            self,
        )

        #
        # Export
        #

        self.action_export_docx = QAction(
            "Export as DOCX",
            self,
        )

        self.action_export_pdf = QAction(
            "Export as PDF",
            self,
        )

        self.action_export_html = QAction(
            "Export as HTML",
            self,
        )

        self.action_export_markdown = QAction(
            "Export as Markdown",
            self,
        )

        #
        # Tools
        #

        self.action_preferences = QAction(
            "Preferences",
            self,
        )

        #
        # Help
        #

        self.action_documentation = QAction(
            "Documentation",
            self,
        )

        self.action_about = QAction(
            "About Proofreader",
            self,
        )

    # ---------------------------------------------------------
    # Menus
    # ---------------------------------------------------------

    def _create_menus(self):

        #
        # File
        #

        file_menu = self.addMenu("&File")

        file_menu.addAction(self.action_new)
        file_menu.addSeparator()

        file_menu.addAction(self.action_open_pdf)
        file_menu.addAction(self.action_open_docx)

        file_menu.addSeparator()

        file_menu.addAction(self.action_save)
        file_menu.addAction(self.action_save_as)

        file_menu.addSeparator()

        file_menu.addAction(self.action_export)

        file_menu.addSeparator()

        file_menu.addAction(self.action_exit)

        #
        # Edit
        #

        edit_menu = self.addMenu("&Edit")

        edit_menu.addAction(self.action_undo)
        edit_menu.addAction(self.action_redo)

        edit_menu.addSeparator()

        edit_menu.addAction(self.action_cut)
        edit_menu.addAction(self.action_copy)
        edit_menu.addAction(self.action_paste)

        edit_menu.addSeparator()

        edit_menu.addAction(self.action_find)

        #
        # View
        #

        view_menu = self.addMenu("&View")

        view_menu.addAction(self.action_zoom_in)
        view_menu.addAction(self.action_zoom_out)
        view_menu.addAction(self.action_reset_zoom)

        view_menu.addSeparator()

        view_menu.addAction(self.action_toggle_theme)
        view_menu.addAction(self.action_fullscreen)

        #
        # Proofreading
        #

        proof_menu = self.addMenu("&Proofreading")

        proof_menu.addAction(self.action_clean_document)
        proof_menu.addAction(self.action_spell_check)
        proof_menu.addAction(self.action_grammar_check)
        proof_menu.addAction(self.action_normalize_fonts)

        #
        # Export
        #

        export_menu = self.addMenu("&Export")

        export_menu.addAction(self.action_export_docx)
        export_menu.addAction(self.action_export_pdf)
        export_menu.addAction(self.action_export_html)
        export_menu.addAction(self.action_export_markdown)

        #
        # Tools
        #

        tools_menu = self.addMenu("&Tools")

        tools_menu.addAction(self.action_preferences)

        #
        # Help
        #

        help_menu = self.addMenu("&Help")

        help_menu.addAction(self.action_documentation)
        help_menu.addSeparator()
        help_menu.addAction(self.action_about)