# Importing necessary modules
import sys
import io
import time
from PySide2.QtWidgets import QMainWindow, QApplication, QTextEdit, QToolBar, QAction, QFileDialog, QComboBox
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QTextCursor, QPalette, QColor
from gtts import gTTS
import pyttsx3

# Defining the main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting window properties
        self.setWindowTitle("Der kleine Lern Helfer")
        self.setGeometry(100, 100, 800, 600)

        # Setting a dark color palette to the widgets
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

        # Creating a text edit widget and setting it as the central widget
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Initializing the toolbar
        self.init_toolbar()

        # Initializing the media player
        self.media_player = QMediaPlayer(self)
        self.media_player.setVolume(50)

        # Showing the main window
        self.show()

    # Method to initialize the toolbar
    def init_toolbar(self):
        # Creating a toolbar widget
        tool_bar = QToolBar("Toolbar")
        self.addToolBar(tool_bar)

        # Creating actions for the toolbar
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

        # Initializing the text-to-speech engine and the voice selection combo box
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.selected_voice = self.voices[0]
        self.engine.setProperty('voice', self.selected_voice.id)

        voice_combobox = QComboBox(self)
        for voice in self.voices:
            voice_combobox.addItem(voice.name)
        voice_combobox.currentIndexChanged.connect(self.set_voice)
        tool_bar.addWidget(voice_combobox)

    # Method to open a file and populate the text edit widget with its content
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt *.pdf)")

        if file_name:
            with open(file_name, "r", encoding="utf-8") as f:
                file_content = f.read()
                self.text_edit.setText(file_content)

    # Method to save the content of the text edit widget to a file
    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")

        if file_name:
            with open(file_name, "w", encoding="utf-8") as f:
                file_content = self.text_edit.toPlainText().encode("utf-8")
                f.write(file_content)

    # Method to clear the content of the text edit widget
    def clear_text(self):
        self.text_edit.clear()

    # Method to play the text entered in the text edit widget using text-to-speech
    def play_text(self):
        text = self.text_edit.toPlainText()

        if text:
            # Creating a text-to-speech object and generating an audio file from the entered text
            tts = gTTS(text, lang="de")
            tts_bytes = io.BytesIO()
            tts.write_to_fp(tts_bytes)
            tts_bytes.seek(0)

            # Saving the generated audio file
            temp_file = f"temp_{int(time.time())}.mp3"
            with open(temp_file, "wb") as f:
                f.write(tts_bytes.getvalue())

            # Setting the generated audio file as the media content and playing it
            media_content = QMediaContent(QUrl.fromLocalFile(temp_file))
            self.media_player.setMedia(media_content)
            self.media_player.play()

            # Setting the cursor position to the start of the text edit widget and saving the audio file as a .wav file
            cursor = self.text_edit.textCursor()
            cursor.setPosition(0)
            cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)

            self.engine.setProperty('rate', 150)
            self.engine.setProperty('voice', self.selected_voice.id)
            self.engine.save_to_file(text, temp_file[:-3] + "wav")

    # Method to set the selected voice from the voice selection combo box
    def set_voice(self, index):
        self.selected_voice = self.voices[index]
        self.engine.setProperty('voice', self.selected_voice.id)

# Main function to instantiate the main window and start the application event loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
