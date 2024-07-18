from PySide6 import QtWidgets, QtCore
import os


class HistoryWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        rgb_history = self.read_color_history()

        number_of_values = len(rgb_history)
        self.color = rgb_history[0] if number_of_values > 0 else (0, 0, 0, 1.0)
        self.color1 = rgb_history[1] if number_of_values > 1 else (0, 0, 0, 1.0)
        self.color2 = rgb_history[2] if number_of_values > 2 else (0, 0, 0, 1.0)
        self.color3 = rgb_history[3] if number_of_values > 3 else (0, 0, 0, 1.0)
        self.color4 = rgb_history[4] if number_of_values > 4 else (0, 0, 0, 1.0)
        self.color5 = rgb_history[5] if number_of_values > 5 else (0, 0, 0, 1.0)

        styleSheet1 = f"""
            QPushButton#coloredButton {{
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba{self.color}, stop: 1 rgba{self.color});
                border: 1px solid black;
                padding: 10px;
            }}

            QPushButton#coloredButton:checked {{
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba{self.color}, stop: 1 rgba{self.color});
                border: 2px solid black;
                padding: 10px;
            }}

            QPushButton#coloredButton1 {{
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba{self.color1}, stop: 1 rgba{self.color1});
                border: 1px solid black;
                padding: 10px;

            }}

            QPushButton#coloredButton1:checked {{
                background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba{self.color1}, stop: 1 rgba{self.color1});
                border: 2px solid black;
                padding: 10px;
            }}

            QPushButton#coloredButton2 {{
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba{self.color2}, stop: 1 rgba{self.color2});
                border: 1px solid black;
                padding: 10px;
            }}

            QPushButton#coloredButton2:checked {{
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba{self.color2}, stop: 1 rgba{self.color2});
                border: 2px solid black;
                padding: 10px;
            }}

            QPushButton#coloredButton3 {{
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba{self.color3}, stop: 1 rgba{self.color3});
                border: 1px solid black;
                padding: 10px;
            }}

            QPushButton#coloredButton3:checked {{
                background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba{self.color3}, stop: 1 rgba{self.color3});
                border: 2px solid black;
                padding: 10px;
            }}

            QPushButton#coloredButton4 {{
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba{self.color4}, stop: 1 rgba{self.color4});
                border: 1px solid black;
                padding: 10px;
            }}

            QPushButton#coloredButton4:checked {{
                background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba{self.color4}, stop: 1 rgba{self.color4});
                border: 2px solid black;
                padding: 10px;
            }}

            QPushButton#coloredButton5 {{
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba{self.color5}, stop: 1 rgba{self.color5});
                border: 1px solid black;
                padding: 10px;
            }}

            QPushButton#coloredButton5:checked {{
                background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba{self.color5}, stop: 1 rgba{self.color5});
                border: 2px solid black;
                padding: 10px;
            }}

            QLabel {{
                font-size: 12pt
            }}
        """

        print(styleSheet1)
        self.setStyleSheet(styleSheet1)

        self.coloredButton = QtWidgets.QPushButton()
        self.coloredButton.setObjectName("coloredButton")
        self.coloredButton.setCheckable(True)
        self.coloredButton.clicked.connect(self.button_clicked)

        self.coloredButton1 = QtWidgets.QPushButton()
        self.coloredButton1.setObjectName("coloredButton1")
        self.coloredButton1.setCheckable(True)
        self.coloredButton1.clicked.connect(self.button_clicked1)

        self.coloredButton2 = QtWidgets.QPushButton()
        self.coloredButton2.setObjectName("coloredButton2")
        self.coloredButton2.setCheckable(True)
        self.coloredButton2.clicked.connect(self.button_clicked2)

        self.coloredButton3 = QtWidgets.QPushButton()
        self.coloredButton3.setObjectName("coloredButton3")
        self.coloredButton3.setCheckable(True)
        self.coloredButton3.clicked.connect(self.button_clicked3)

        self.coloredButton4 = QtWidgets.QPushButton()
        self.coloredButton4.setObjectName("coloredButton4")
        self.coloredButton4.setCheckable(True)
        self.coloredButton4.clicked.connect(self.button_clicked4)

        self.coloredButton5 = QtWidgets.QPushButton()
        self.coloredButton5.setObjectName("coloredButton5")
        self.coloredButton5.setCheckable(True)
        self.coloredButton5.clicked.connect(self.button_clicked5)

        self.buttonGroup = QtWidgets.QButtonGroup()
        self.buttonGroup.setExclusive(True)
        self.buttonGroup.addButton(self.coloredButton)
        self.buttonGroup.addButton(self.coloredButton1)
        self.buttonGroup.addButton(self.coloredButton2)
        self.buttonGroup.addButton(self.coloredButton3)
        self.buttonGroup.addButton(self.coloredButton4)
        self.buttonGroup.addButton(self.coloredButton5)

        self.colorHistoryLayout = QtWidgets.QHBoxLayout()
        self.colorHistoryLayout.addWidget(self.coloredButton)
        self.colorHistoryLayout.addWidget(self.coloredButton1)
        self.colorHistoryLayout.addWidget(self.coloredButton2)
        self.colorHistoryLayout.addWidget(self.coloredButton3)
        self.colorHistoryLayout.addWidget(self.coloredButton4)
        self.colorHistoryLayout.addWidget(self.coloredButton5)

        self.colorDialog = QtWidgets.QVBoxLayout()
        self.colorDataLayout = QtWidgets.QVBoxLayout()

        hex_layout = QtWidgets.QHBoxLayout()
        HEX = QtWidgets.QLabel("HEX")
        self.hex_color = QtWidgets.QLabel(self.rgb_to_hex(self.color))
        self.hex_color.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        )
        hex_layout.addWidget(HEX)
        hex_layout.addWidget(self.hex_color)

        rgb_layout = QtWidgets.QHBoxLayout()
        RGB = QtWidgets.QLabel("RGB")
        r = self.color[0]
        g = self.color[1]
        b = self.color[2]
        self.rgb_color = QtWidgets.QLabel(f"rgb({r}, {g}, {b})")
        self.rgb_color.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        )
        rgb_layout.addWidget(RGB)
        rgb_layout.addWidget(self.rgb_color)

        hsl_layout = QtWidgets.QHBoxLayout()
        HSL = QtWidgets.QLabel("HSL")
        h, s, v = self.rgb_to_hsl(self.color)
        self.hsl_color = QtWidgets.QLabel(f"hsl({h}, {s}, {v})")
        self.hsl_color.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        )
        hsl_layout.addWidget(HSL)
        hsl_layout.addWidget(self.hsl_color)

        self.colorDataLayout.addLayout(hex_layout)
        self.colorDataLayout.addLayout(rgb_layout)
        self.colorDataLayout.addLayout(hsl_layout)

        self.colorDialog.addLayout(self.colorHistoryLayout)
        self.colorDialog.addLayout(self.colorDataLayout)
        widget = QtWidgets.QWidget()
        widget.setLayout(self.colorDialog)
        self.setCentralWidget(widget)

    def button_clicked(self):
        color = self.color
        self.hex_color.setText(self.rgb_to_hex(color))
        self.rgb_color.setText(f"rgb({color[0]}, {color[1]}, {color[2]})")
        h, s, l = self.rgb_to_hsl(color)
        self.hsl_color.setText(f"hsl({h}, {s}, {l})")

    def button_clicked1(self):
        color = self.color1
        self.hex_color.setText(self.rgb_to_hex(color))
        self.rgb_color.setText(f"rgb({color[0]}, {color[1]}, {color[2]})")
        h, s, l = self.rgb_to_hsl(color)
        self.hsl_color.setText(f"hsl({h}, {s}, {l})")

    def button_clicked2(self):
        color = self.color2
        self.hex_color.setText(self.rgb_to_hex(color))
        self.rgb_color.setText(f"rgb({color[0]}, {color[1]}, {color[2]})")
        h, s, l = self.rgb_to_hsl(color)
        self.hsl_color.setText(f"hsl({h}, {s}, {l})")

    def button_clicked3(self):
        color = self.color3
        self.hex_color.setText(self.rgb_to_hex(color))
        self.rgb_color.setText(f"rgb({color[0]}, {color[1]}, {color[2]})")
        h, s, l = self.rgb_to_hsl(color)
        self.hsl_color.setText(f"hsl({h}, {s}, {l})")

    def button_clicked4(self):
        color = self.color4
        self.hex_color.setText(self.rgb_to_hex(color))
        self.rgb_color.setText(f"rgb({color[0]}, {color[1]}, {color[2]})")
        h, s, l = self.rgb_to_hsl(color)
        self.hsl_color.setText(f"hsl({h}, {s}, {l})")

    def button_clicked5(self):
        color = self.color5
        self.hex_color.setText(self.rgb_to_hex(color))
        self.rgb_color.setText(f"rgb({color[0]}, {color[1]}, {color[2]})")
        h, s, l = self.rgb_to_hsl(color)
        self.hsl_color.setText(f"hsl({h}, {s}, {l})")

    def rgb_to_hex(self, rgb):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def rgb_to_hsl(self, rgb):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        r = float(r)
        g = float(g)
        b = float(b)
        high = max(r, g, b)
        low = min(r, g, b)
        h, s, l = ((high + low) / 2,) * 3

        if high == low:
            h = 0.0
            s = 0.0
        else:
            d = high - low
            s = d / (2 - high - low) if l > 0.5 else d / (high + low)
            h = {
                r: (g - b) / d + (6 if g < b else 0),
                g: (b - r) / d + 2,
                b: (r - g) / d + 4,
            }[high]
            h /= 6

        return round(h, 3), round(s, 3), round(l, 3)

    def read_color_history(self):
        rgb_values = []
        root_dir = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(root_dir, ".colorpycker_history"), "r") as file:
            for line in file:
                rgb = line.strip()[1:-1].split(",")

                r = int(rgb[0].strip())
                g = int(rgb[1].strip())
                b = int(rgb[2].strip())
                a = float(rgb[3].strip())
                rgb_values.append((r, g, b, a))

        print(rgb_values)

        return rgb_values
