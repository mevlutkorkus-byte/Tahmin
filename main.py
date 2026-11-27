import sqlite3
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QListWidget, QMessageBox
from PySide6.QtCore import Qt

folder = Path.home() / "Library" / "Application Support" / "TahminAI"
folder.mkdir(parents=True, exist_ok=True)
db = sqlite3.connect(folder / "local.sqlite3")
db.execute("CREATE TABLE IF NOT EXISTS observations (id INTEGER PRIMARY KEY, alias TEXT NOT NULL, context TEXT NOT NULL, outcome TEXT NOT NULL)")
db.commit()

app = QApplication([])
window = QWidget()
window.setWindowTitle("Tahmin AI — Yerel prototip")
window.resize(760, 650)
layout = QVBoxLayout(window)
layout.addWidget(QLabel("Davranış gözlemleri ve geçmiş örüntüler"))
layout.addWidget(QLabel("Yalnızca izinli veriler kullanın. Gerçek isim yerine takma ad girin."))
alias = QLineEdit()
alias.setPlaceholderText("Kişi kodu")
context = QLineEdit()
context.setPlaceholderText("Durum etiketi (ör. tartışma sonrası)")
outcome = QTextEdit()
outcome.setPlaceholderText("Gerçekleşen, gözlemlenebilir davranış")
for widget in (alias, context, outcome):
    layout.addWidget(widget)
save = QPushButton("Gözlemi kaydet")
analyze = QPushButton("Benzer geçmiş durumları incele")
delete = QPushButton("Bu kişi kodunun kayıtlarını sil")
results = QListWidget()
for widget in (save, analyze, delete, results):
    layout.addWidget(widget)

def record():
    values = (alias.text().strip(), context.text().strip(), outcome.toPlainText().strip())
    if not all(values):
        QMessageBox.warning(window, "Eksik veri", "Üç alanı da doldurun.")
        return
    db.execute("INSERT INTO observations(alias, context, outcome) VALUES (?, ?, ?)", values)
    db.commit()
    outcome.clear()
    QMessageBox.information(window, "Kayıt", "Gözlem yerel olarak kaydedildi.")

def review():
    results.clear()
    rows = db.execute("SELECT outcome, COUNT(*) FROM observations WHERE alias=? AND context=? GROUP BY outcome ORDER BY COUNT(*) DESC", (alias.text().strip(), context.text().strip())).fetchall()
    if not rows:
        results.addItem("Benzer geçmiş kayıt yok. Tahmin için veri yetersiz.")
        return
    results.addItem("Geçmiş sıklıklar — gelecekteki davranış olasılığı değildir.")
    for behavior, count in rows:
        results.addItem(f"{behavior} — {count} kayıt")

def erase():
    key = alias.text().strip()
    if key and QMessageBox.question(window, "Sil", "Bu kişi koduna ait tüm gözlemler silinsin mi?") == QMessageBox.StandardButton.Yes:
        db.execute("DELETE FROM observations WHERE alias=?", (key,))
        db.commit()
        results.clear()

save.clicked.connect(record)
analyze.clicked.connect(review)
delete.clicked.connect(erase)
window.show()
app.exec()
db.close()
