"""Entry point for Gear S3 Explorer."""
import sys
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Gear S3 Explorer")
    try:
        window = MainWindow()
        window.show()
    except Exception as exc:
        traceback.print_exc()
        QMessageBox.critical(
            None,
            "Gear S3 Explorer - startup error",
            f"The application could not start:\n\n{type(exc).__name__}: {exc}\n\n"
            "Run main.py from a terminal to see the full traceback.",
        )
        return 1
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
