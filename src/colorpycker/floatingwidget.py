#!/usr/bin/env python3

import sys, random, os, re
from PySide6 import QtWidgets, QtCore, QtGui, QtDBus
from colorpycker import historywindow
from typing import Optional


class MainWidget(QtWidgets.QMainWindow):

    def openHistoryWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = historywindow.HistoryWindow()
        self.ui.setWindowTitle("Colorpycker")
        self.ui.move(self.point)

        eyedropper_svg = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "colorpycker.svg"
        )

        self.ui.setWindowIcon(QtGui.QIcon(eyedropper_svg))
        self.ui.show()

    def __init__(self):
        super().__init__()
        self.root_dir = os.path.abspath(os.path.dirname(__file__))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.stopChild = False
        self.point = None
        self.colorCode = "#abcdef"
        # self.colorCode = "rgb(255, 255, 255)"
        # self.colorCode = "cmyk(100%, 100%, 100%, 100%)"
        # self.colorCode = "hsl(100%, 100%, 100%)"
        self.outerBox = QtCore.QRect()

        self.colorBox = QtCore.QRect()

        self.outerBox = QtCore.QRect(
            QtCore.QPoint(*random.sample(range(200), 2)), QtCore.QSize(150, 50)
        )
        self.colorBox = QtCore.QRect(
            QtCore.QPoint(*random.sample(range(200), 2)), QtCore.QSize(40, 40)
        )
        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.colorCode)

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

        # screen = QtWidgets.QApplication.primaryScreen()
        # pixMapp = screen.grabWindow(0)
        # self.color = pixMapp.toImage().pixelColor(self.point)
        result = []

        def _signal_triggered(color0: int, color1: int, color2: int) -> None:
            print("Signal Triggered")
            result.append(color0)
            result.append(color1)
            result.append(color2)

        portal = PortalPickColorInterface()
        portal.on_result.connect(_signal_triggered)
        QtCore.QTimer.singleShot(0, portal.getColor)
        self.color = QtGui.QColor(result[0], result[1], result[2])
        self.colorCode = self.color.name()
        print(f"rgb({self.color.red()}, {self.color.green()}, {self.color.blue()})")
        print(self.color.name())
        self.label.setText(self.color.name())

        super().paintEvent(event)
        print("Painting event")
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.black, 1, QtCore.Qt.SolidLine))
        painter.setBrush(
            QtGui.QBrush(QtGui.QColor(250, 250, 250), QtCore.Qt.SolidPattern)
        )
        painter.drawRoundedRect(self.outerBox, 5, 5)

        colorBoxPainter = QtGui.QPainter(self)
        colorBoxPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        colorBoxPainter.setPen(
            QtGui.QPen(QtGui.Qt.GlobalColor.black, 1, QtCore.Qt.SolidLine)
        )
        colorBoxPainter.setBrush(QtGui.QBrush(self.color))
        colorBoxPainter.drawRoundedRect(self.colorBox, 5, 5)

        self.update()

    def mouseMoveEvent(self, event):

        self.outerBox.moveTopLeft(event.pos() + QtCore.QPoint(7, 7))
        self.point = event.pos()
        coords = self.outerBox.getCoords()
        print(coords)

        self.colorBox.moveTopLeft(QtCore.QPoint(coords[0] + 5, coords[1] + 5))
        colorBoxCoords = self.colorBox.getCoords()
        self.label.move(QtCore.QPoint(colorBoxCoords[0] + 50, colorBoxCoords[1] + 5))
        self.update()
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.colorCode)
        rgb_values = []
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if os.path.isfile(os.path.join(self.root_dir, ".colorpycker_history")):
                with open(
                    os.path.join(self.root_dir, ".colorpycker_history"), "r"
                ) as history:
                    for line in history:
                        rgb = line.strip()[1:-1].split(",")
                        r = int(rgb[0].strip())
                        g = int(rgb[1].strip())
                        b = int(rgb[2].strip())
                        rgb_values.append((r, g, b, 1.0))

            if len(rgb_values) >= 6:
                rgb_values = rgb_values[:5]

            color = (self.color.red(), self.color.green(), self.color.blue(), 1.0)
            rgb_values = [color] + rgb_values
            print(rgb_values)

            with open(
                os.path.join(self.root_dir, ".colorpycker_history"), "w"
            ) as history:
                for color in rgb_values:
                    print(str(color))
                    history.write("%s\n" % str(color))
            self.close()
            self.openHistoryWindow()


def run():
    app = QtWidgets.QApplication([])
    eyedropper_svg = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "colorpycker.svg"
    )
    appwindow = MainWidget()
    appwindow.setWindowIcon(QtGui.QIcon(eyedropper_svg))
    appwindow.showFullScreen()
    appwindow.show()
    sys.exit(app.exec())


class PortalRequestInterface(QtDBus.QDBusAbstractInterface):
    Response = QtCore.Signal(QtDBus.QDBusMessage)

    def __init__(
        self, path: str, connection: QtDBus.QDBusConnection, parent: QtCore.QObject
    ) -> None:
        super().__init__(
            "org.freedesktop.portal.Desktop",
            path,
            "org.freedesktop.portal.Request",  # type: ignore
            connection,
            parent,
        )


class PortalPickColorInterface(QtCore.QObject):
    on_response = QtCore.Signal(QtDBus.QDBusMessage)
    on_result = QtCore.Signal(int, int, int)

    def __init__(
        self,
        parent: Optional[QtCore.QObject] = None,
    ) -> None:
        super().__init__(parent)
        self.on_response.connect(self.got_signal)

    def getColor(self) -> None:
        bus = QtDBus.QDBusConnection.sessionBus()

        base = bus.baseService()[1:].replace(".", "_")

        object_path = f"/org/freedesktop/portal/desktop/request/{base}/my_token"

        request = PortalRequestInterface(object_path, bus, self)
        request.Response.connect(self.on_response)

        interface = QtDBus.QDBusInterface(
            "org.freedesktop.portal.Desktop",
            "/org/freedesktop/portal/desktop",
            "org.freedesktop.portal.Screenshot",
            bus,
            self,
        )

        message = interface.call("PickColor", "", {"handle_token": "my_token"})

    def got_signal(self, message: QtDBus.QDBusMessage) -> None:
        print("DBus signal message: %s", str(message))

        pattern = r"\(ddd\)\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)"

        match = re.search(pattern, str(message))
        print(match.group(1))
        print(match.group(2))
        print(match.group(3))

        self.on_result.emit(
            int(float(match.group(1)) * 255),
            int(float(match.group(2)) * 255),
            int(float(match.group(3)) * 255),
        )


if __name__ == "__main__":
    run()
