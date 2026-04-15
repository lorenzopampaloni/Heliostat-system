import sys
import serial
import time
import math
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor

# ---------------- CONFIG ----------------
PORT = 'COM7'
BAUD = 9600

LAT = 43.765
LON = 11.220

UPDATE_INTERVAL = 30  # secondi

T = (9.20, -0.50, -3.50)

STEPS_AZ = 16000 / (2*math.pi)
STEPS_EL = 11250 / (2*math.pi)

# ---------------- SERIAL ----------------
ser = serial.Serial(PORT, BAUD, timeout=0.1)
msg_id = 0

def wait_ack(expected_id, timeout=1.0):
    buffer = ""
    start = time.time()

    while time.time() - start < timeout:
        if ser.in_waiting:
            buffer += ser.read().decode(errors='ignore')

            while ";" in buffer:
                msg, buffer = buffer.split(";", 1)

                if msg.startswith("@"):
                    try:
                        id_str, status = msg[1:].split(":")
                        if int(id_str) == expected_id:
                            return status
                    except:
                        pass
    return "TIMEOUT"

def send(cmd):
    global msg_id

    packet = f"#{msg_id}:{cmd};"
    ser.reset_input_buffer()
    ser.write(packet.encode())
    print(">>", packet)

    time.sleep(0.05)  

    resp = wait_ack(msg_id, timeout=1.5)

    if resp == "OK":
        print("<< OK")
    else:
        print("!! ERROR:", resp)

    msg_id += 1
    return resp == "OK"

def move_to(px, py):
    send("ENABLE")
    time.sleep(1)
    send(f"PX{px}")
    send(f"PY{py}")
    time.sleep(1)
    send("DISABLE")

# ---------------- MATH ----------------
def normalize(v):
    norm = math.sqrt(sum(i*i for i in v))
    return tuple(i/norm for i in v)

T = normalize(T)

def get_sun_vector(lat, lon):
    now = datetime.utcnow()

    day = now.timetuple().tm_yday
    hour = now.hour + now.minute/60

    decl = 23.45 * math.sin(math.radians(360*(284+day)/365))
    h_angle = (hour - 12) * 15

    lat_r = math.radians(lat)
    decl_r = math.radians(decl)
    h_r = math.radians(h_angle)

    el = math.asin(
        math.sin(lat_r)*math.sin(decl_r) +
        math.cos(lat_r)*math.cos(decl_r)*math.cos(h_r)
    )

    az = math.atan2(
        -math.sin(h_r),
        math.tan(decl_r)*math.cos(lat_r) -
        math.sin(lat_r)*math.cos(h_r)
    )

    x = math.cos(el)*math.cos(az)
    y = math.sin(el)
    z = math.cos(el)*math.sin(az)

    return normalize((x,y,z))

def get_normal(S):
    return normalize((
        S[0] + T[0],
        S[1] + T[1],
        S[2] + T[2]
    ))

def normal_to_angles(N):
    az = math.atan2(N[2], N[0])
    el = math.asin(N[1])
    return az, el

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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solar Tracker")

        self.tracking = False
        self.step0 = (0,0)
        self.az0 = 0
        self.el0 = 0
        self.last_update = time.time()
        self.correction_count = 0
        self.countdown = UPDATE_INTERVAL

        layout = QVBoxLayout()

        # BOTTONI
        row = QHBoxLayout()
        row.addWidget(self.btn("ENABLE", lambda: send("ENABLE")))
        row.addWidget(self.btn("DISABLE", lambda: send("DISABLE")))
        layout.addLayout(row)

        layout.addWidget(self.btn("START TRACKING", self.start_tracking))
        layout.addWidget(self.btn("STOP TRACKING", self.stop_tracking))

        layout.addWidget(self.btn("STOP", lambda: send("S")))
        
        self.lbl_countdown = QLabel("Next update: 0s")
        self.lbl_counter = QLabel("Corrections: 0")

        layout.addWidget(self.lbl_countdown)
        layout.addWidget(self.lbl_counter)

        # JOYSTICK
        self.joy = Joystick()
        layout.addWidget(self.joy)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loop)
        self.timer.start(100)
        
    def update_status(self):
        if self.tracking:
            remaining = UPDATE_INTERVAL - (time.time() - self.last_update)
            remaining = max(0, int(remaining))
            self.lbl_countdown.setText(f"Next update: {remaining}s")
        else:
            self.lbl_countdown.setText("Tracking OFF")

        self.lbl_counter.setText(f"Corrections: {self.correction_count}")

    def btn(self, txt, func):
        b = QPushButton(txt)
        b.clicked.connect(func)
        return b

    # ---------------- TRACKING ----------------
    def start_tracking(self):
        print("START TRACKING")

        send("R")

        S = get_sun_vector(LAT, LON)
        N = get_normal(S)

        self.az0, self.el0 = normal_to_angles(N)
        self.step0 = (0,0)

        self.tracking = True

    def stop_tracking(self):
        print("STOP TRACKING")
        self.tracking = False

    # ---------------- LOOP ----------------
    def update_loop(self):
        self.update_status()
        # TRACKING MODE
        if self.tracking:
            if time.time() - self.last_update < UPDATE_INTERVAL:
                return

            self.last_update = time.time()

            S = get_sun_vector(LAT, LON)
            N = get_normal(S)

            az, el = normal_to_angles(N)

            daz = az - self.az0
            delv = el - self.el0

            step_x = int(self.step0[0] + daz * STEPS_AZ)
            step_y = int(self.step0[1] + delv * STEPS_EL)

            print("TARGET:", step_x, step_y)

            move_to(step_x, step_y)
            self.correction_count += 1
            return

        # MANUAL MODE (joystick)
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
