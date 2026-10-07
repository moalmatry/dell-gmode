"""Dell G15 Fn+F9 Keyboard Event Listener Daemon."""
import os
import struct
import sys
import time
from .controller import GModeController

KBD_PATHS = [
    "/dev/input/by-path/platform-i8042-serio-0-event-kbd",
    "/dev/input/event2",
]


class GModeDaemon:
    def __init__(self, debounce_sec: float = 0.6):
        self.debounce_sec = debounce_sec
        self.last_trigger = 0.0

    @staticmethod
    def find_keyboard_fd() -> int | None:
        """Locates and opens the internal AT keyboard event device."""
        for path in KBD_PATHS:
            if os.path.exists(path):
                try:
                    return os.open(path, os.O_RDONLY)
                except OSError:
                    pass

        # Dynamic search if default paths not found
        import glob
        for dev in glob.glob("/dev/input/event*"):
            try:
                name_path = f"/sys/class/input/{os.path.basename(dev)}/device/name"
                if os.path.exists(name_path):
                    with open(name_path, "r") as f:
                        if "AT Translated Set 2 keyboard" in f.read():
                            return os.open(dev, os.O_RDONLY)
            except OSError:
                continue

        return None

    def run(self):
        """Runs the event loop monitoring for Fn+F9 keypresses."""
        fd = self.find_keyboard_fd()
        if fd is None:
            time.sleep(2)
            fd = self.find_keyboard_fd()

        if fd is None:
            sys.exit("Error: Could not open keyboard event device. Please run with root/sudo.")

        print("[✓] Dell G-Mode Daemon started. Listening for Fn+F9 events...")

        while True:
            try:
                data = os.read(fd, 24)
                if not data or len(data) < 24:
                    continue

                sec, usec, ev_type, ev_code, ev_value = struct.unpack("qqHHi", data[:24])

                # EV_MSC (type 4): MSC_SCAN (code 4), value 104 (0x68) -> Dell G15 Fn+F9
                # EV_KEY (type 1): KEY_PERFORMANCE (code 701), KEY_PROG1 (code 148)
                is_gmode_key = (
                    (ev_type == 4 and ev_value == 104) or
                    (ev_type == 1 and ev_code == 701 and ev_value == 1) or
                    (ev_type == 1 and ev_code == 148 and ev_value == 1)
                )

                now = time.time()
                if is_gmode_key and (now - self.last_trigger >= self.debounce_sec):
                    self.last_trigger = now
                    mode = GModeController.toggle(notify=True)
                    print(f"[⚡] Fn+F9 pressed: Toggled mode to {mode}")

            except OSError:
                time.sleep(1)
                fd = self.find_keyboard_fd()
