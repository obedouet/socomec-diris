#
# Domoticz Plugin for Energy Utility / Socomec Diris metering
# Polls the Flask REST API (see README.md, default http://<host>:5002) and
# publishes total + per-phase electrical measurements to Domoticz.
#
# Note: the only REST API documented in this project is README.md (Diris).
# If your utility exposes a different weather-style endpoint set, adjust
# the POLL_ENDPOINTS / device specs below; the plugin skeleton stays the same.
#
"""
<plugin key="energy-utility" name="Energy Utility REST" author="obedouet" version="0.1" wikilink="https://github.com/obedouet/socomec-diris">
    <params>
        <param field="mAddress" label="API Host" width="200px" required="true" default="127.0.0.1"/>
        <param field="mPort" label="API Port" width="75px" required="true" default="5002"/>
        <param field="Mode1" label="Poll interval (s)" width="75px" required="true" default="20"/>
    </params>
</plugin>
"""

import Domoticz
import json
import threading
import time
import urllib.request
import urllib.error
from datetime import datetime

# ── REST endpoint map ────────────────────────────────────────────────────────
# path -> (unit divisor, signed?, kind)
#   kind is informational; device creation/specs are driven by UNITS/TYPE below.
POLL_ENDPOINTS = {
    "total/real":        ("W",  True),
    "total/apparent":    ("VA", False),
    "phase1/frequency":  ("Hz", False),   # cents of Hz  -> /100
    "phase1/voltage":    ("V",  False),
    "phase1/amps":       ("A",  False),   # mA           -> /1000
    "phase1/apparent":   ("VA", False),
    "phase1/reactive":   ("VAR", True),
    "phase1/real":       ("W",  True),
    "phase1/pf":         ("ratio", False),  # if >32768: 65535-value; assumed /100
    "phase2/voltage":    ("V",  False),
    "phase2/amps":       ("A",  False),
    "phase2/apparent":   ("VA", False),
    "phase2/reactive":   ("VAR", True),
    "phase2/real":       ("W",  True),
    "phase2/pf":         ("ratio", False),
    "phase3/voltage":    ("V",  False),
    "phase3/amps":       ("A",  False),
    "phase3/apparent":   ("VA", False),
    "phase3/reactive":   ("VAR", True),
    "phase3/real":       ("W",  True),
    "phase3/pf":         ("ratio", False),
    "neutral/amps":      ("A",  False),
}

# unit -> conversion function applied to the raw integer from the API
def _pf(raw):
    if raw > 32768:
        raw = 65535 - raw
    return round(raw / 100.0, 3)          # assumed /100 scale; adjust if firmware differs

CONVERT = {
    "W":      lambda v: float(v),
    "VA":     lambda v: float(v),
    "VAR":    lambda v: float(v),
    "V":      lambda v: float(v),
    "A":      lambda v: v / 1000.0,       # mA -> A
    "Hz":     lambda v: v / 100.0,        # cents of Hz -> Hz
    "ratio":  _pf,
}

# ── Device specs ─────────────────────────────────────────────────────────────
# (unit, name, Domoticz Type, Subtype, sValue-format note)
# Using Custom sensors (243 / 31) keeps the plugin loading cleanly; switch to
# Type 247 (P1) if you want native energy charts.
DEVICE_SPECS = [
    # unit      name                     unit-str    type  sub
    ("total/real",      "Total Real Power",    "kW", 243, 31),
    ("total/apparent",  "Total Apparent Power","kVA", 243, 31),
    ("phase1/frequency","Freq Phase 1",        "Hz", 243, 31),
    ("phase1/voltage",  "V Phase 1",           "V",  243,8),
    ("phase1/amps",     "I Phase 1",           "A",  243, 23),
    ("phase1/apparent", "VA Phase 1",          "kVA",243, 31),
    ("phase1/reactive", "VAr Phase 1",         "kVAr",243,31),
    ("phase1/real",     "kW Phase 1",          "kW", 243, 31),
    ("phase2/voltage",  "V Phase 2",           "V",  243, 8),
    ("phase2/amps",     "I Phase 2",           "A",  243, 23),
    ("phase2/apparent", "VA Phase 2",          "kVA",243, 31),
    ("phase2/reactive", "VAr Phase 2",         "kVAr",243,31),
    ("phase2/real",     "kW Phase 2",          "kW", 243, 31),
    ("phase3/voltage",  "V Phase 3",           "V",  243, 8),
    ("phase3/amps",     "I Phase 3",           "A",  243, 23),
    ("phase3/apparent", "VA Phase 3",          "kVA",243, 31),
    ("phase3/reactive", "VAr Phase 3",         "kVAr",243,31),
    ("phase3/real",     "kW Phase 3",          "kW", 243, 31),
    ("neutral/amps",    "I Neutral",           "A",  243, 23),
]

# unit -> converter
UNIT_OF = {s[0]: s[1] for s in DEVICE_SPECS}
def converter_for(endpoint, unit):
    if unit == "Hz":
        return CONVERT["Hz"]
    if unit == "A":
        return CONVERT["A"]
    if unit == "ratio":
        return CONVERT["ratio"]
    return CONVERT.get(unit, lambda v: float(v))

# ── Plugin Class ─────────────────────────────────────────────────────────────
class BasePlugin:
    def __init__(self):
        self.base_url = ""
        self.poll_interval = 20
        self.thread = None
        self.stop_event = threading.Event()
        self.data_lock = threading.Lock()
        return

    # ---- lifecycle ----
    def onStart(self):
        Domoticz.Log("Starting Energy Utility REST plugin")

        host = Parameters["mAddress"].strip()
        port = Parameters["mPort"].strip()
        try:
            self.poll_interval = int(Parameters["Mode1"])
        except Exception:
            self.poll_interval = 20
        self.base_url = "http://%s:%s/" % (host, port)
        Domoticz.Log("Polling API at %s every %ss" % (self.base_url, self.poll_interval))

        # create devices (unit number = index in DEVICE_SPECS, 1-based)
        for i, (endpoint, name, unit, dtype, dsub) in enumerate(DEVICE_SPECS, start=1):
            if i not in Devices:
                opts = {"Custom": "0;%s" % unit} if unit else None
                Domoticz.Device(
                    Name=name, Unit=i, Type=dtype, Subtype=dsub, Options=opts
                ).Create()

        # start the polling thread
        if self.thread is None or not self.thread.is_alive():
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.poll_loop)
            self.thread.daemon = True
            self.thread.start()
            Domoticz.Log("Polling thread started")

    def onConnect(self, Status, Description):
        Domoticz.Log("onConnect called with status: %s" % Status)

    def poll_loop(self):
        Domoticz.Log("Polling loop running")
        while not self.stop_event.is_set():
            try:
                self.poll_once()
                self.stop_event.wait(self.poll_interval)
            except Exception as e:
                if not self.stop_event.is_set():
                    Domoticz.Error("Error in polling loop: %s" % str(e))
                time.sleep(5)
        Domoticz.Log("Polling loop stopped")

    def poll_once(self):
        for i, (endpoint, name, unit, dtype, dsub) in enumerate(DEVICE_SPECS, start=1):
            try:
                raw = self.fetch(endpoint)
                if raw is None:
                    continue
                conv = converter_for(endpoint, unit)
                value = conv(raw)

                if unit in ("kW", "kVA"):
                    # power values: divide to kW/kVA for readability
                    value = value / 100.0
                elif unit == "kVAr":
                    # kVAr can be negative but raw value is only unsigned
                    if value > 32767:
                        value = (value - 65535)/100
                    else:
                        value = (65535 - value)/100
                elif unit == "V":
                    value = value / 100.0

                with self.data_lock:
                    if i in Devices:
                        Devices[i].Update(nValue=0, sValue=str(round(value, 3)))
            except Exception as e:
                Domoticz.Error("Error updating %s: %s" % (name, str(e)))

    def fetch(self, endpoint):
        url = self.base_url + endpoint
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8").strip()
            # API may return a bare number or a JSON dict
            try:
                data = json.loads(body)
            except ValueError:
                return int(float(body))
            if isinstance(data, dict):
                for key in ("value", "val", "data", "result"):
                    if key in data:
                        return int(data[key])
                return None
            return int(data)
        except urllib.error.URLError as e:
            Domoticz.Error("GET %s failed: %s" % (url, str(e)))
            return None
        except Exception as e:
            Domoticz.Error("GET %s failed: %s" % (url, str(e)))
            return None

    def onStop(self):
        Domoticz.Log("Stopping Energy Utility REST plugin")
        if self.thread is not None:
            self.stop_event.set()
            self.thread.join(timeout=5)
            Domoticz.Log("Polling thread stopped")

    def onHeartbeat(self):
        pass

# ── Plugin Instance ───────────────────────────────────────────────────────────
plugin = BasePlugin()

# ── Callbacks ────────────────────────────────────────────────────────────────
def onStart():
    plugin.onStart()

def onConnect(Status, Description):
    plugin.onConnect(Status, Description)

def onMessage(Data):
    pass

def onDisconnect():
    plugin.onStop()

def onHeartbeat():
    plugin.onHeartbeat()