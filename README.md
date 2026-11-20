# WiFi Pentesting Mode Tool (wpt-mode)

![wpt-mode logo](logo.svg)

This Python script simplifies switching between monitor mode and managed mode on a WiFi interface using granular Linux network controls (`ip`, `iw`, `nmcli`), removing reliance on the `aircrack-ng` suite.

## Features

- **Start Monitor Mode**: Activate monitor mode on a specified WiFi interface using granular controls (`ip link set <interface> down`, `iw dev <interface> set type monitor`, `ip link set <interface> up`).
- **Exit Monitor Mode**: Deactivate monitor mode (`ip link set <interface> down`, `iw dev <interface> set type managed`, `ip link set <interface> up`) and restart NetworkManager.
- **Rescan WiFi Networks**: Automatically exit monitor mode, scan for available WiFi networks via `nmcli`, and re-enable monitor mode.

## Requirements

- Python 3.x
- iproute2 (`ip`)
- iw (or wireless-tools)
- NetworkManager & nmcli

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/sampson-q/wpt-mode.git
   cd wpt-mode
   ```

2. **Setup Script:**

   Run the setup script (`setup.sh`) to verify dependencies and make `wpt-mode` executable from anywhere:

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Usage:**

   ```bash
   Usage: wpt-mode [--start | -s | --exit | -e | --rescan | -r] <interface> [options]

   Options:
     -h, --help                   Display this help message and exit
     -d, --delay <seconds>        Set custom delay before rescan (default is 4 seconds)

   Commands:
     --start, -s                  Start monitor mode on specified interface
     --exit, -e                   Exit monitor mode and restart NetworkManager
     --rescan, -r                 Rescan WiFi networks after exiting monitor mode
   ```

   Examples:
   ```bash
     wpt-mode --start wlan0
     wpt-mode --exit wlan0
     wpt-mode --rescan wlan0 -d 6
   ```

4. **Examples:**

   - Start monitor mode on interface `wlan0`:
     ```bash
     wpt-mode --start wlan0
     ```

   - Exit monitor mode on interface `wlan0` and restart NetworkManager:
     ```bash
     wpt-mode --exit wlan0
     ```

   - Rescan WiFi networks with a custom delay of 6 seconds after exiting monitor mode:
     ```bash
     wpt-mode --rescan wlan0 -d 6
     ```

## Case Study: Switching Between Monitor and Managed Modes

Using `wpt-mode` simplifies the process of switching between monitor mode and managed mode on a WiFi interface during penetration testing. Here's how the tool improves efficiency using granular network controls:

1. **Starting Monitor Mode**:
   - Stops interfering background processes (such as NetworkManager and `wpa_supplicant`).
   - Sets the interface down: `ip link set <interface> down`.
   - Sets interface mode to monitor: `iw dev <interface> set type monitor`.
   - Brings the interface back up: `ip link set <interface> up`.

2. **Exiting Monitor Mode**:
   - Sets the interface down: `ip link set <interface> down`.
   - Sets interface mode back to managed: `iw dev <interface> set type managed`.
   - Brings the interface back up: `ip link set <interface> up`.
   - Restarts NetworkManager (`systemctl restart NetworkManager`) to restore normal network connectivity.

3. **Rescanning WiFi Networks**:
   - Automatically switches back to managed mode, pauses for the interface to initialize, rescans WiFi networks using `nmcli device wifi list`, and re-enables monitor mode.

By automating these granular steps, `wpt-mode` provides clean mode switching without interface renaming or heavy third-party suite dependencies.
