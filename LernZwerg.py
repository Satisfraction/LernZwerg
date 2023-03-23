# Ein kleines Tool zum helfen beim Auswendig Lernen von Texten für Schulkinder ;)

import io
import sys
import time
from gtts import gTTS
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QTextCursor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QAction, QToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Der kleine Lern Helfer")
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        self.init_toolbar()

        self.media_player = QMediaPlayer(self)
        self.media_player.setVolume(50)

        self.show()

    def init_toolbar(self):
        tool_bar = QToolBar("Toolbar")
        self.addToolBar(Qt.LeftToolBarArea, tool_bar)

        open_file_action = QAction("Datei Öffnen", self)
        open_file_action.triggered.connect(self.open_file)
        tool_bar.addAction(open_file_action)

        save_file_action = QAction("Datei Speichern", self)
        save_file_action.triggered.connect(self.save_file)
        tool_bar.addAction(save_file_action)

        clear_text_action = QAction("Text Löschen", self)
        clear_text_action.triggered.connect(self.clear_text)
        tool_bar.addAction(clear_text_action)

        play_text_action = QAction("Play", self)
        play_text_action.triggered.connect(self.play_text)
        tool_bar.addAction(play_text_action)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt *.pdf)")

        if file_name:
            with open(file_name, "r", encoding="utf-8") as f:
                file_content = f.read().decode("utf-8")
                self.text_edit.setText(file_content)

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")

        if file_name:
            with open(file_name, "w", encoding="utf-8") as f:
                file_content = self.text_edit.toPlainText().encode("utf-8")
                f.write(file_content)

    def clear_text(self):
        self.text_edit.clear()
    
    def play_text(self):
        text = self.text_edit.toPlainText()

        if text:
            tts = gTTS(text, lang="de")
            tts_bytes = io.BytesIO()
            tts.write_to_fp(tts_bytes)
            tts_bytes.seek(0)

            temp_file = f"temp_{int(time.time())}.mp3"
            with open(temp_file, "wb") as f:
                f.write(tts_bytes.getvalue())

            media_content = QMediaContent(QUrl.fromLocalFile(temp_file))
            self.media_player.setMedia(media_content)

            self.media_player.play()

            cursor = self.text_edit.textCursor()
            cursor.setPosition(0)
            cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
