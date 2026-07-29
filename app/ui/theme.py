"""
theme.py

Handles application themes.
"""

from PySide6.QtWidgets import QApplication


class ThemeManager:

    def __init__(self):

        self.dark_mode = True

    # ---------------------------------------------------------

    def apply(self, window):

        if self.dark_mode:
            QApplication.instance().setStyleSheet(
                self.dark_stylesheet()
            )
        else:
            QApplication.instance().setStyleSheet(
                self.light_stylesheet()
            )

    # ---------------------------------------------------------

    def toggle(self, window):

        self.dark_mode = not self.dark_mode

        self.apply(window)

    # ---------------------------------------------------------

    @staticmethod
    def dark_stylesheet():

        return """

        QWidget{

            background:#2b2b2b;

            color:white;

            font-size:10pt;

        }

        QMenuBar{

            background:#353535;

        }

        QMenu{

            background:#353535;

        }

        QToolBar{

            background:#3d3d3d;

        }

        QTextEdit{

            background:#252526;

            border:1px solid #444;

        }

        QListWidget{

            background:#252526;

            border:1px solid #444;

        }

        QDockWidget{

            font-weight:bold;

        }

        """

    # ---------------------------------------------------------

    @staticmethod
    def light_stylesheet():

        return """

        QWidget{

            background:white;

            color:black;

            font-size:10pt;

        }

        QTextEdit{

            border:1px solid gray;

        }

        QListWidget{

            border:1px solid gray;

        }

        """