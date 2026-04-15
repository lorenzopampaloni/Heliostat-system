#include <AccelStepper.h>

// --- PIN ---
#define X_STEP 4
#define X_DIR  5
#define Y_STEP 6
#define Y_DIR  7

#define EN_X 8
#define EN_Y 9

AccelStepper sx(AccelStepper::DRIVER, X_STEP, X_DIR);
AccelStepper sy(AccelStepper::DRIVER, Y_STEP, Y_DIR);

bool enabled = false;

// ---------------- SERIAL BUFFER ----------------
String buffer = "";

// ---------------- SETUP ----------------
void setup() {
  Serial.begin(115200);   // DEBUG USB
  Serial1.begin(9600);    // HC-12

  pinMode(EN_X, OUTPUT);
  pinMode(EN_Y, OUTPUT);

  disableDrivers();

  sx.setMaxSpeed(1000);
  sx.setAcceleration(500);

  sy.setMaxSpeed(1000);
  sy.setAcceleration(500);

  sx.setPinsInverted(false, false, true);
  sy.setPinsInverted(false, false, true);

  Serial.println("READY");
}

// ---------------- LOOP ----------------
void loop() {
  readSerial();

  if (!enabled) return;

  sx.run();
  sy.run();
}

// ---------------- SERIAL PARSER ----------------
void readSerial() {
  while (Serial1.available()) {
    char c = Serial1.read();

    if (c == ';') {
      processPacket(buffer);
      buffer = "";
    } else {
      buffer += c;
    }
  }
}

// ---------------- PROCESS PACKET ----------------
void processPacket(String pkt) {
  pkt.trim();

  Serial.print("RX: ");
  Serial.println(pkt);  // DEBUG su USB

  if (pkt.length() == 0) return;
  if (pkt[0] != '#') return;

  int sep = pkt.indexOf(':');
  if (sep == -1) return;

  String id = pkt.substring(1, sep);
  String cmd = pkt.substring(sep + 1);

  bool ok = executeCommand(cmd);

  sendAck(id, ok);
}

// ---------------- EXECUTE COMMAND ----------------
bool executeCommand(String s) {
  s.trim();

  if (s == "ENABLE") { enableDrivers(); return true; }
  if (s == "DISABLE") { disableDrivers(); return true; }

  if (s == "S") {
    sx.stop();
    sy.stop();
    return true;
  }

  if (s == "R") {
    sx.setCurrentPosition(0);
    sy.setCurrentPosition(0);
    return true;
  }

  if (s.startsWith("VX")) {
    sx.setMaxSpeed(s.substring(2).toFloat());
    return true;
  }

  if (s.startsWith("VY")) {
    sy.setMaxSpeed(s.substring(2).toFloat());
    return true;
  }

  if (s.startsWith("AX")) {
    sx.setAcceleration(s.substring(2).toFloat());
    return true;
  }

  if (s.startsWith("AY")) {
    sy.setAcceleration(s.substring(2).toFloat());
    return true;
  }

  if (s.startsWith("PX")) {
    sx.moveTo(s.substring(2).toInt());
    return true;
  }

  if (s.startsWith("PY")) {
    sy.moveTo(s.substring(2).toInt());
    return true;
  }

  if (s.startsWith("SX")) {
    sx.move(s.substring(2).toInt());
    return true;
  }

  if (s.startsWith("SY")) {
    sy.move(s.substring(2).toInt());
    return true;
  }

  return false;
}

// ---------------- ACK ----------------
void sendAck(String id, bool ok) {
  Serial1.print("@");
  Serial1.print(id);

  if (ok) Serial1.println(":OK;");
  else Serial1.println(":ERR;");
}

// ---------------- DRIVER CONTROL ----------------
void enableDrivers() {
  digitalWrite(EN_X, HIGH);
  digitalWrite(EN_Y, HIGH);
  enabled = true;
  Serial.println("ENABLED"); // debug
}

void disableDrivers() {
  digitalWrite(EN_X, LOW);
  digitalWrite(EN_Y, LOW);
  enabled = false;
  Serial.println("DISABLED"); // debug
}
