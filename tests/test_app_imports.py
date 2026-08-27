import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QMainWindow

from app.ui.mainwindow import MainWindow


def test_main_window_can_be_created():
    app = QApplication.instance() or QApplication([])
    window = MainWindow()

    assert isinstance(window, QMainWindow)
    assert window.windowTitle() == "Proofreader"
    assert window.central.document_panel.editor.isReadOnly() is False

    window.close()
    app.quit()
