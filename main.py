from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QColorDialog
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QImage
from PyQt6.QtCore import QSize, Qt, QPoint
from PyQt6 import QtGui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PapaWolf")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.setFixedSize(1520, 600)
        self.setStyleSheet('''
        QSlider::handle:vertical {
                           background-color: black;
                           border-radius: 5px;};
        ''')

        self.label = QLabel()
        self.canvas = QPixmap(QSize(900, 580))
        self.canvas.fill(QColor("white"))
        self.label.setPixmap(self.canvas)

        self.pen = QPen()
        self.pen.setWidth(6)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.current_tool = 'pen'
        self.previousPoint = None

        self.createToolPanel()

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.toolPanel) 
        mainLayout.addWidget(self.label) 

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        self.color_dialog = QColorDialog(self)
        self.color_dialog.setOption(QColorDialog.ColorDialogOption.NoButtons)
        self.color_dialog.currentColorChanged.connect(self.changeColor)
        mainLayout.addWidget(self.color_dialog)

    def createToolPanel(self):
        self.toolPanel = QWidget()
        toolLayout = QVBoxLayout()
        self.toolPanel.setLayout(toolLayout)

        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.saveToFile)
        toolLayout.addWidget(saveButton)

        penButton = QPushButton("Pen")
        penButton.clicked.connect(self.selectPen)
        toolLayout.addWidget(penButton)

        fillButton = QPushButton("Fill")
        fillButton.clicked.connect(self.selectFill)
        toolLayout.addWidget(fillButton)

        eraserButton = QPushButton("Eraser")
        eraserButton.clicked.connect(self.selectEraser)
        toolLayout.addWidget(eraserButton)

        label = QLabel(self)
        label.setText("Size")
        toolLayout.addWidget(label)

        self.brushSizeSlider = QSlider(Qt.Orientation.Vertical)
        self.brushSizeSlider.setRange(1, 50)
        self.brushSizeSlider.setValue(6)
        self.brushSizeSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.brushSizeSlider.setTickInterval(5)
        self.brushSizeSlider.valueChanged.connect(self.changeBrushSize)
        toolLayout.addWidget(self.brushSizeSlider)

        self.toolPanel.setFixedWidth(100)

    def selectPen(self):
        self.current_tool = 'pen'
        self.pen.setColor(QColor("black"))

    def selectFill(self):
        self.current_tool = 'fill'

    def selectEraser(self):
        self.current_tool = 'eraser'
        self.pen.setColor(QColor("white"))

    def saveToFile(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        if filePath:
            self.canvas.save(filePath)

    def changeBrushSize(self):
        self.pen.setWidth(self.brushSizeSlider.value())

    def changeColor(self, color):
        self.pen.setColor(color)

    def mousePressEvent(self, event):
        position = event.position().toPoint() - self.label.pos()

        if 0 <= position.x() < self.label.width() and 0 <= position.y() < self.label.height():
            if self.current_tool == 'fill':
                self.fill(position)
            elif self.current_tool == 'pen' or self.current_tool == 'eraser':
                self.previousPoint = position

    def mouseMoveEvent(self, event):
        if self.current_tool == 'pen' or self.current_tool == 'eraser':
            position = event.position().toPoint() - self.label.pos()

            if 0 <= position.x() < self.label.width() and 0 <= position.y() < self.label.height():
                painter = QPainter(self.canvas)
                painter.setPen(self.pen)

                if self.previousPoint:
                    painter.drawLine(self.previousPoint, position)
                else:
                    painter.drawPoint(position)

                self.previousPoint = position
                painter.end()
                self.label.setPixmap(self.canvas)

    def mouseReleaseEvent(self, event):
        self.previousPoint = None

    def fill(self, position):

     image = self.canvas.toImage()
     width, height = image.width(), image.height()

     target_color = image.pixelColor(position)
     fill_color = self.pen.color()

     if target_color == fill_color:
        return

     stack = [position]

     while stack:
        current_point = stack.pop()
        x, y = current_point.x(), current_point.y()

        if image.pixelColor(x, y) != target_color:
            continue

        left = x
        while left > 0 and image.pixelColor(left - 1, y) == target_color:
            left -= 1

        right = x
        while right < width - 1 and image.pixelColor(right + 1, y) == target_color:
            right += 1

        for i in range(left, right + 1):
            image.setPixelColor(i, y, fill_color)

            if y > 0 and image.pixelColor(i, y - 1) == target_color:
                stack.append(QPoint(i, y - 1))
            if y < height - 1 and image.pixelColor(i, y + 1) == target_color:
                stack.append(QPoint(i, y + 1))

     self.canvas = QPixmap.fromImage(image)
     self.label.setPixmap(self.canvas)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
