# Dell G15 Fn+F9 G-Mode (Game Shift) for Linux ⚡

Native Linux background daemon and CLI utility for **Dell G15 (5515 / 5520)** laptops to bring the **Fn+F9 (G-Mode / Game Shift)** key to life.

Toggles between **Balanced Mode** and **High Performance G-Mode** (unlocked CPU/GPU power limits + 100% maximum fan cooling boost) with instant on-screen desktop notifications. Managed with **Poetry**.

---

## 🚀 Features

* **⌨️ Native Fn+F9 Hardware Trigger:** Listens directly to the internal keyboard controller for scancode `104` (`0x68`), working everywhere—including inside full-screen games.
* **🌀 Alienware WMAX Fan Boost:** Sends direct ACPI WMAX calls to the motherboard's Embedded Controller to override cooling curves and engage maximum fan speeds.
* **⚡ CPU & GPU Performance Scaling:** Switches the Linux kernel `alienware_wmi` `platform_profile` to `performance` to unlock maximum wattage and clock governors.
* **🔔 Native Desktop Notifications:** Dispatches on-screen alerts via user DBus (`notify-send`) confirming mode activation.
* **🪶 Ultra Lightweight:** Runs as a systemd background service using only **~2.5 MB of RAM** and **0% CPU** while idle.
* **💻 Command-Line Interface (`dell-gmode`):** Manual controls for scripting and keybinding.
* **📦 Poetry Packaging:** Clean, modern Python packaging with Poetry.

---

## 🔍 How It Works

On Dell G15 laptops, the **Fn+F9** hotkey is wired directly to the internal AT keyboard controller (`/dev/input/event2`) and emits raw scancode `104` (`0x68`). Standard Linux desktop environments don't recognize this key and do nothing.

`dell-gmode` runs a small event loop that catches this event, handles debouncing, and:
1. **Engages Performance Mode:**
   * Writes `performance` to `/sys/firmware/acpi/platform_profile` (CPU & GPU power scaling).
   * Calls ACPI WMAX method `\_SB.AMW3.WMAX 0 0x25 {0x1, 0x1, 0x00, 0x00}` to activate maximum fan cooling.
   * Shows: **"⚡ High Performance Mode Activated (Fans Maximum)"**
2. **Restores Balanced Mode:**
   * Writes `balanced` to `/sys/firmware/acpi/platform_profile`.
   * Calls ACPI WMAX method `\_SB.AMW3.WMAX 0 0x25 {0x1, 0x0, 0x00, 0x00}` to restore quiet acoustic curves.
   * Shows: **"🍃 Balanced Mode Activated"**

---

## 💻 Supported Hardware

* **Dell G15 5515** (AMD Ryzen Edition)
* **Dell G15 5520** (Intel Edition)
* Other Dell G-Series and Alienware laptops with the Game Shift (G-Mode) keyboard key and WMAX ACPI interface.

---

## 📦 Installation

### Prerequisites
* Python 3.10+
* Poetry (`pipx install poetry` or `sudo apt install python3-poetry`)
* `acpi_call-dkms` (for WMAX hardware fan control)

### Install via Installer Script

```bash
git clone https://github.com/moalmatry/dell-gmode.git
cd dell-gmode
chmod +x install.sh
./install.sh
```

The installer will:
1. Build the Poetry environment and install the package.
2. Link the `dell-gmode` executable to `/usr/local/bin/`.
3. Enable and start `dell-gmode.service` in systemd.
4. Ensure the `acpi_call` kernel module is loaded on boot.

---

## 🖥️ Usage

### Using the Hardware Key
Simply press **Fn+F9** anywhere on your laptop to toggle G-Mode!

### Using the CLI (`dell-gmode`)

```bash
# Toggle between Balanced and G-Mode
dell-gmode toggle

# Force High Performance G-Mode (Fans 100%)
dell-gmode performance

# Force Balanced Mode (Quiet Fans)
dell-gmode balanced

# Check current mode
dell-gmode status
```

---

## 🛠️ Service Management

Check service status:
```bash
systemctl status dell-gmode.service
```

Restart service:
```bash
sudo systemctl restart dell-gmode.service
```

---

## 🗑️ Uninstallation

```bash
cd dell-gmode
./uninstall.sh
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
