import sys, json, re
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: white;")

        self.button = QtWidgets.QPushButton("convert to sBoooky 👻")
        self.text = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)

        self.fileButton = QtWidgets.QPushButton("Select file 🔪", )
        self.destinationButton = QtWidgets.QPushButton("Select destination 🪦")

        self.file = QtWidgets.QLabel('', alignment=QtCore.Qt.AlignCenter) #QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Python scripts (*.py)")[0]
        self.destination = QtWidgets.QLabel('', alignment=QtCore.Qt.AlignCenter)#QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")

        self.message = QtWidgets.QLabel('', alignment = QtCore.Qt.AlignCenter)

        self.attr = QtWidgets.QLabel("Games icons created by Freepik - Flaticon", alignment = QtCore.Qt.AlignCenter)

        self.movie = QtGui.QMovie("./Assets/screee.gif", )

        self.fileButton.setStyleSheet("background-color: #f5f5f5; border: 1px solid #e0e0e0; border-radius: 5px; padding: 5px;")
        self.destinationButton.setStyleSheet("background-color: #f5f5f5; border: 1px solid #e0e0e0; border-radius: 5px; padding: 5px;")
        self.button.setStyleSheet("background-color: #f5f5f5; border: 1px solid #e0e0e0; border-radius: 5px; padding: 5px;")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.text.setMovie(self.movie)
        #self.layout.addItem(self.movie)
        self.movie.start()
        self.layout.addWidget(self.fileButton)
        self.layout.addWidget(self.file)
        self.layout.addWidget(self.destinationButton)
        self.layout.addWidget(self.destination)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.message)

        self.layout.addWidget(self.attr)

        self.fileButton.clicked.connect(self.selectFile)
        self.destinationButton.clicked.connect(self.selectDestination)
        self.button.clicked.connect(self.magic)

    def selectFile(self):
        self.file.setText(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Python scripts (*.py)")[0])
    
    def selectDestination(self):
        self.destination.setText(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))

    @QtCore.Slot()
    def magic(self):
        try:
            corpus = open(self.file.text(), "r").read()
            splits = re.split('\n\n|\n#+ ', corpus)

            out = []
            for token in splits:
                if token.lstrip()[0] == '#':
                    out.append(token.lstrip())
                elif token[0].isspace() and token.lstrip()[0] != '#':
                    out[-1] += '\n' + token
                else:
                    out.append(token)

            dictNotebook = {
                "cells": [],
                "metadata": {},
                "nbformat": 6,
                "nbformat_minor": 4
                }

            
            cells = []
            for code in out:
                if code[0] == '#':
                    cell = {
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": code
                    }
                else:
                    cell = {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "outputs": [],
                        "source": code
                    }
                cells.append(cell)      
            
            dictNotebook["cells"] = cells

            jason = json.dumps(dictNotebook)

            fileName = self.file.text().split('/')[-1].split('.')[0]

            with open(self.destination.text() + f'/{fileName}.ipynb', 'w') as f:
                f.write(jason)

            self.message.setText("Success!. Your lazy ass can find your file in the destination folder. You can close this window now.  ")
        
        except:
            self.message.setText("There was an error. Goodluck figuring it out.")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    app.setApplicationName("screeepy script file transmogrifier")
    app.setApplicationDisplayName('screeepy')

    app.setWindowIcon(QtGui.QIcon('./Assets/icon.png'))

    widget = MyWidget()
    widget.resize(500, 200)
    widget.show()

    sys.exit(app.exec())