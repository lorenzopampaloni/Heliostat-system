import sys
import serial
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor

# ---------------- SERIAL ----------------
ser = serial.Serial('COM7', 9600, timeout=0.1)

msg_id = 0

def send(cmd):
    global msg_id

    packet = f"#{msg_id}:{cmd};"
    ser.write(packet.encode())

    print(">>", packet)

    time.sleep(0.2)  # 🔥 QUESTA È LA CHIAVE

    resp = ser.read_all().decode(errors='ignore')
    print("<< RAW:", resp)

    if f"@{msg_id}:OK;" in resp:
        print("<< OK")
        msg_id += 1
        return True

    print("!! TIMEOUT")
    msg_id += 1
    return False


# ---------------- JOYSTICK ----------------
class Joystick(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        self.x = 0
        self.y = 0

    def mouseMoveEvent(self, e):
        cx = self.width()/2
        cy = self.height()/2

        dx = (e.x() - cx)/cx
        dy = (e.y() - cy)/cy

        self.x = max(-1, min(1, dx))
        self.y = max(-1, min(1, dy))
        self.update()

    def mouseReleaseEvent(self, e):
        self.x = 0
        self.y = 0
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setBrush(QColor(50,50,50))
        p.drawRect(0,0,self.width(),self.height())

        cx = self.width()/2
        cy = self.height()/2

        px = cx + self.x * cx
        py = cy + self.y * cy

        p.setBrush(QColor(200,0,0))
        p.drawEllipse(int(px-10), int(py-10), 20, 20)
        
    


# ---------------- UI ----------------
class Control(QWidget):
    
    def test(self):
        send("ENABLE")

        time.sleep(1)
        print("LATE READ:", ser.read_all().decode(errors='ignore'))
        
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motion Controller PRO")

        layout = QVBoxLayout()

        # ENABLE
        row = QHBoxLayout()
        row.addWidget(self.btn("ENABLE", lambda: send("ENABLE")))
        row.addWidget(self.btn("DISABLE", lambda: send("DISABLE")))
        layout.addLayout(row)

        # PARAMETRI
        param = QHBoxLayout()

        self.vx = QLineEdit("3000")
        self.vy = QLineEdit("3000")
        self.ax = QLineEdit("3000")
        self.ay = QLineEdit("3000")

        param.addWidget(QLabel("VX"))
        param.addWidget(self.vx)
        param.addWidget(QLabel("VY"))
        param.addWidget(self.vy)
        param.addWidget(QLabel("AX"))
        param.addWidget(self.ax)
        param.addWidget(QLabel("AY"))
        param.addWidget(self.ay)

        param.addWidget(self.btn("SET", self.set_params))
        layout.addLayout(param)

        # POSIZIONE
        pos = QHBoxLayout()

        self.px = QLineEdit("0")
        self.py = QLineEdit("0")

        pos.addWidget(QLabel("PX"))
        pos.addWidget(self.px)
        pos.addWidget(QLabel("PY"))
        pos.addWidget(self.py)
        pos.addWidget(self.btn("GO", self.go_pos))

        layout.addLayout(pos)

        # STEP
        step = QHBoxLayout()

        self.sx = QLineEdit("100")
        self.sy = QLineEdit("100")

        step.addWidget(QLabel("SX"))
        step.addWidget(self.sx)
        step.addWidget(QLabel("SY"))
        step.addWidget(self.sy)
        step.addWidget(self.btn("STEP", self.do_step))

        layout.addLayout(step)

        
        
        
        layout.addWidget(self.btn("TEST", self.test))
        
        
        
        # STOP
        layout.addWidget(self.btn("STOP", lambda: send("S")))

        # JOYSTICK
        self.joy = Joystick()
        layout.addWidget(self.joy)

        self.setLayout(layout)

        # TIMER joystick
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_joystick)
        self.timer.start(100)

    def btn(self, txt, func):
        b = QPushButton(txt)
        b.clicked.connect(func)
        return b

    def set_params(self):
        send(f"VX{self.vx.text()}")
        send(f"VY{self.vy.text()}")
        send(f"AX{self.ax.text()}")
        send(f"AY{self.ay.text()}")

    def go_pos(self):
        send(f"PX{self.px.text()}")
        send(f"PY{self.py.text()}")

    def do_step(self):
        send(f"SX{self.sx.text()}")
        send(f"SY{self.sy.text()}")

    def update_joystick(self):
        # deadzone
        if abs(self.joy.x) < 0.1:
            self.joy.x = 0
        if abs(self.joy.y) < 0.1:
            self.joy.y = 0

        scale = 500

        sx_val = int(self.joy.x * scale)
        sy_val = int(self.joy.y * scale)

        if sx_val != 0:
            send(f"SX{sx_val}")

        if sy_val != 0:
            send(f"SY{-sy_val}")


# ---------------- RUN ----------------
app = QApplication(sys.argv)
w = Control()
w.show()
sys.exit(app.exec_())
