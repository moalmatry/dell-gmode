"""Dell G15 G-Mode Hardware Controller.

Interfaces with Linux ACPI platform_profile and Alienware WMAX method to control
power limits, GPU/CPU performance states, and maximum fan boost.
"""
import glob
import os
import subprocess

PLATFORM_PROFILE = "/sys/firmware/acpi/platform_profile"
ACPI_CALL = "/proc/acpi/call"

# WMAX method paths: AMW3 (AMD Ryzen models like G15 5515), AMWW (Intel models like G15 5520)
WMAX_METHODS = ["\\_SB.AMW3.WMAX", "\\_SB.AMWW.WMAX"]


class GModeController:
    @staticmethod
    def send_notification(title: str, message: str, icon: str = "preferences-system-performance", urgency: str = "normal"):
        """Deliver native desktop notifications to all active graphical user sessions."""
        for user_run in glob.glob("/run/user/[0-9]*"):
            uid = os.path.basename(user_run)
            bus = f"unix:path={user_run}/bus"
            try:
                subprocess.run(
                    ["notify-send", "-i", icon, "-u", urgency, title, message],
                    env={"DBUS_SESSION_BUS_ADDRESS": bus, "PATH": "/usr/bin:/bin"},
                    user=int(uid),
                    check=False,
                )
            except Exception:
                pass

    @classmethod
    def get_mode(cls) -> str:
        """Returns current platform profile ('performance', 'balanced', 'power-saver')."""
        try:
            with open(PLATFORM_PROFILE, "r") as f:
                return f.read().strip()
        except OSError:
            # Fallback to powerprofilesctl if direct sysfs read fails
            try:
                res = subprocess.run(["powerprofilesctl", "get"], capture_output=True, text=True, check=True)
                return res.stdout.strip()
            except Exception:
                return "balanced"

    @classmethod
    def set_wmax_fan_boost(cls, enable: bool):
        """Sends Alienware WMAX ACPI call to enable/disable 100% G-Mode fan override."""
        if not os.path.exists(ACPI_CALL):
            subprocess.run(["modprobe", "acpi_call"], check=False)

        if os.path.exists(ACPI_CALL):
            val = 1 if enable else 0
            for method in WMAX_METHODS:
                cmd = f"{method} 0 0x25 {{0x1, {hex(val)}, 0x00, 0x00}}"
                try:
                    with open(ACPI_CALL, "w") as f:
                        f.write(cmd)
                    with open(ACPI_CALL, "r") as f:
                        resp = f.read().strip()
                    if resp and not resp.startswith("Error"):
                        break
                except OSError:
                    continue

    @classmethod
    def set_mode(cls, mode: str, notify: bool = True) -> str:
        """Sets the system performance mode ('performance' or 'balanced')."""
        is_perf = (mode.lower() in ("performance", "gmode", "g-mode"))
        target = "performance" if is_perf else "balanced"

        # 1. Update Linux platform_profile
        try:
            with open(PLATFORM_PROFILE, "w") as f:
                f.write(target)
        except OSError:
            subprocess.run(["powerprofilesctl", "set", target], check=False)

        # 2. Update WMAX G-Mode fan boost
        cls.set_wmax_fan_boost(is_perf)

        # 3. Notification
        if notify:
            if is_perf:
                cls.send_notification(
                    "Dell G-Mode",
                    "⚡ High Performance Mode Activated (Fans Maximum)",
                    "preferences-system-performance",
                    "critical",
                )
            else:
                cls.send_notification(
                    "Dell G-Mode",
                    "🍃 Balanced Mode Activated",
                    "preferences-system-power",
                    "normal",
                )

        return target

    @classmethod
    def toggle(cls, notify: bool = True) -> str:
        """Toggles between Balanced and Performance (G-Mode)."""
        current = cls.get_mode()
        if current == "performance":
            return cls.set_mode("balanced", notify=notify)
        else:
            return cls.set_mode("performance", notify=notify)
