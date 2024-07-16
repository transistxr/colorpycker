#!/usr/bin/env python3

import sys, random
from PySide6 import QtWidgets, QtCore, QtGui
from historywindow import HistoryWindow


class MainWidget(QtWidgets.QMainWindow):

    def openHistoryWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = HistoryWindow()
        self.ui.show()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.showFullScreen()
        self.setMouseTracking(True)


        self.point = None
        self.colourCode = "#abcdef"
        # self.colourCode = "rgb(255, 255, 255)"
        # self.colourCode = "cmyk(100%, 100%, 100%, 100%)"
        # self.colourCode = "hsl(100%, 100%, 100%)"        
        self.outerBox = QtCore.QRect()

        self.colorBox = QtCore.QRect()

        self.outerBox = QtCore.QRect(
            QtCore.QPoint(*random.sample(range(200), 2)), QtCore.QSize(150, 50)
        )
        self.colorBox = QtCore.QRect(
            QtCore.QPoint(*random.sample(range(200), 2)), QtCore.QSize(40, 40)
        )
        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.colourCode)

        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(1)
        self.label.setFont(font)
        # self.label.setStyleSheet("background-color: white;")

        # Update outerBox size based on text size
        text_width = self.label.fontMetrics().boundingRect(self.label.text()).width()
        self.outerBox.setSize(QtCore.QSize(text_width + 70, 50))  # Add padding
        self.update()

        self.resize(640, 480)


    def paintEvent(self, event):

        screen = QtWidgets.QApplication.primaryScreen()
        pixMapp = screen.grabWindow(0)
        colour = pixMapp.toImage().pixelColor(self.point).toCmyk()
        self.colourCode = colour.name()
        print(colour.name())
        self.label.setText(colour.name())

        super().paintEvent(event)
        print("Painting event")
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.black, 1, QtCore.Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(250, 250, 250), QtCore.Qt.SolidPattern))
        painter.drawRoundedRect(self.outerBox, 5, 5)



        colorBoxPainter = QtGui.QPainter(self)
        colorBoxPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        colorBoxPainter.setPen(QtGui.QPen(QtGui.Qt.GlobalColor.black, 1, QtCore.Qt.SolidLine))
        colorBoxPainter.setBrush(QtGui.QBrush(colour))
        colorBoxPainter.drawRoundedRect(self.colorBox, 5, 5)
    
        self.update()



    def mouseMoveEvent(self, event):

        self.outerBox.moveTopLeft(event.pos() + QtCore.QPoint(7, 7))
        self.point = event.pos()
        coords = self.outerBox.getCoords()
        print(coords)
        
        self.colorBox.moveTopLeft(QtCore.QPoint(coords[0]+5, coords[1]+5))
        colourBoxCoords = self.colorBox.getCoords()
        self.label.move(QtCore.QPoint(colourBoxCoords[0]+50, colourBoxCoords[1]+5))
        self.update()
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.close()
            self.openHistoryWindow()

def run():
    app = QtWidgets.QApplication([])
    appwindow = MainWidget()
    appwindow.showFullScreen()
    appwindow.show()
    sys.exit(app.exec())