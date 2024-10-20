from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QToolBar, QColorDialog, QFileDialog
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QAction
from PyQt6.QtCore import QSize, Qt
from PyQt6 import QtGui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(600,600)
        self.setWindowTitle("PapaWolf")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        

        self.previousPoint = None

        self.label = QLabel()

        self.canvas = QPixmap(QSize(600,600))
        self.canvas.fill(QColor("white"))

        self.pen = QPen()
        self.pen.setWidth(6)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        

        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)

        toolbar = QToolBar("ToolBar")
        

        saveAction = QAction("Save", self)
        saveAction.triggered.connect(self.saveToFile)
        toolbar.addAction(saveAction)

        colorAction = QAction("Colors", self)
        colorAction.triggered.connect(self.changeColor)
        toolbar.addAction(colorAction)

        

        self.addToolBar(toolbar)

    def saveToFile(self):
        dialog = QFileDialog()
        dialog.setNameFilter("*.png")
        dialog.setDefaultSuffix(".png")  
        clickedOk = dialog.exec()

        if clickedOk:
            self.canvas.save(dialog.selectedFiles()[0])

    def changeColor(self):
        dialog = QColorDialog()
        clickedOk = dialog.exec()
        
        if clickedOk:
            self.pen.setColor(dialog.currentColor())
        
    def mouseMoveEvent(self, event):
        position = event.pos()
        
        painter = QPainter(self.canvas)
        painter.setPen(self.pen)

        if self.previousPoint:
            painter.drawLine(self.previousPoint, position)
        
        
        self.previousPoint = position

        
        painter.end()
        self.label.setPixmap(self.canvas)

    def mouseReleaseEvent(self, event):
        self.previousPoint = None

app = QApplication([])
window = MainWindow()
window.show()
app.exec()