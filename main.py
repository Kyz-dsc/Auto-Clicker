from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QDoubleSpinBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import sys
import time
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode

class ClickThread(QThread):
    def __init__(self, delay, click_type):
        super().__init__()
        self.mouse = Controller()
        self.delay = delay
        self.click_type = click_type
        self.running = True
    
    def run(self):
        while self.running:
            if self.click_type == "Gauche":
                self.mouse.click(Button.left)
            elif self.click_type == "Droit":
                self.mouse.click(Button.right)
            elif self.click_type == "Double":
                self.mouse.click(Button.left, 2)
            time.sleep(self.delay)
    
    def stop(self):
        self.running = False

class AutoClickerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.hotkey = 'f6'  # Déplacé avant initUI()
        self.initUI()
        self.click_thread = None
        self.listener = Listener(on_press=self.on_key_press)
        self.listener.start()
    
    def initUI(self):
        self.setWindowTitle("Auto Clicker Stylé")
        self.setGeometry(100, 100, 300, 250)
        layout = QVBoxLayout()
        self.delay_label = QLabel("Délai entre clics (secondes):")
        self.delay_input = QDoubleSpinBox()
        self.delay_input.setRange(0.01, 10.0)
        self.delay_input.setValue(0.1)
        self.click_label = QLabel("Type de clic:")
        self.click_type = QComboBox()
        self.click_type.addItems(["Gauche", "Droit", "Double"])
        self.hotkey_label = QLabel("Touche de démarrage/arrêt:")
        self.hotkey_input = QLineEdit()
        self.hotkey_input.setText(self.hotkey)
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_clicking)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_clicking)
        layout.addWidget(self.delay_label)
        layout.addWidget(self.delay_input)
        layout.addWidget(self.click_label)
        layout.addWidget(self.click_type)
        layout.addWidget(self.hotkey_label)
        layout.addWidget(self.hotkey_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)
    
    def start_clicking(self):
        if not self.click_thread or not self.click_thread.isRunning():
            self.click_thread = ClickThread(self.delay_input.value(), self.click_type.currentText())
            self.click_thread.start()
    
    def stop_clicking(self):
        if self.click_thread:
            self.click_thread.stop()
    
    def on_key_press(self, key):
        try:
            if hasattr(key, 'char') and key.char == self.hotkey_input.text():
                if self.click_thread and self.click_thread.isRunning():
                    self.stop_clicking()
                else:
                    self.start_clicking()
        except AttributeError:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClickerApp()
    window.show()
    sys.exit(app.exec())
