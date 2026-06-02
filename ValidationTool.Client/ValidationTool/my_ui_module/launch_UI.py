from PySide6 import QtWidgets

from my_ui_module.validator_UI import ValidatorWindow


_window = None


def close_existing():
    global _window

    if _window:
        try:
            _window.close()
            _window.deleteLater()
        except:
            pass
        _window = None


def show():
    global _window

    close_existing()

    _window = ValidatorWindow()
    _window.show()

    return _window