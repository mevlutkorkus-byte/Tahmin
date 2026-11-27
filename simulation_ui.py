import json
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QCheckBox, QLineEdit, QMessageBox
from PySide6.QtCore import QThread, Signal
from scientific_engine import simulate

class Job(QThread):
    result = Signal(str)
    def __init__(self, observations, scenario, choices):
        super().__init__()
        self.args = observations, scenario, choices
    def run(self):
        try:
            data = simulate(*self.args, consent=True)
            self.result.emit(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        except Exception as exc:
            self.result.emit("Simülasyon başarısız: " + type(exc).__name__ + ". Kurulum ve API ayarlarını kontrol edin.")

app = QApplication([])
window = QWidget()
window.setWindowTitle("Tahmin AI | GenAgents")
window.resize(850, 740)
layout = QVBoxLayout(window)
layout.addWidget(QLabel("Stanford GenAgents — davranış senaryosu"))
observations = QTextEdit()
observations.setPlaceholderText("İzinli ve kimliksiz gözlemler; her satır bir olay")
scenario = QLineEdit()
scenario.setPlaceholderText("Gelecekteki durum ve zaman aralığı")
choices = QTextEdit()
choices.setPlaceholderText("Olası davranışlar; her satır bir seçenek")
consent = QCheckBox("Girilen verilerin OpenAI API servisine gönderilmesini onaylıyorum.")
button = QPushButton("Bilimsel modeli çalıştır")
output = QTextEdit()
output.setReadOnly(True)
for widget in (observations, scenario, choices, consent, button, output):
    layout.addWidget(widget)
job = None
def start():
    global job
    if not consent.isChecked() or not os.environ.get("OPENAI_API_KEY"):
        QMessageBox.warning(window, "Ayar gerekli", "API anahtarı ve veri aktarım onayı gerekli.")
        return
    obs = [s.strip() for s in observations.toPlainText().splitlines() if s.strip()]
    opts = list(dict.fromkeys(s.strip() for s in choices.toPlainText().splitlines() if s.strip()))
    button.setEnabled(False)
    job = Job(obs, scenario.text(), opts)
    job.result.connect(output.setPlainText)
    job.finished.connect(lambda: button.setEnabled(True))
    job.start()
button.clicked.connect(start)
def close(event):
    if job is not None and job.isRunning():
        event.ignore()
    else:
        event.accept()
window.closeEvent = close
window.show()
app.exec()
