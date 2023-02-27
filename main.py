import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from text_summarizer import summarize_text

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('gui.ui', self)
        self.pushButton.clicked.connect(self.handleButton)   # Browse input file
        self.summarizeButton.clicked.connect(self.summarizeText) # Summarize text
        self.copyButton.clicked.connect(self.copyToClipboard)   # Copy to clipboard

    def handleButton(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open File', '.', 'Word Files (*.docx);;Text Files (*.txt)')
        self.lineEdit.setText(filePath)
        
    def summarizeText(self):
        file_path = self.lineEdit.text()
        if file_path:
            summary = summarize_text(file_path)
            self.outputText.setText(summary)
        else:
            self.outputText.setText('Please select a file to summarize.')
        
    def copyToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.outputText.toPlainText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
