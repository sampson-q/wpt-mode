#!/usr/bin/env python3
import sys
import subprocess
import time
import os

def run_command(cmd, check=False, capture=False):
    if os.geteuid() != 0 and cmd[0] != 'sudo':
        cmd = ['sudo'] + cmd
    try:
        if capture:
            return subprocess.run(cmd, check=check, text=True, capture_output=True)
        return subprocess.run(cmd, check=check)
    except Exception as e:
        print(f"[-] Error executing {' '.join(cmd)}: {e}")
        return None

def start_monitor_mode(interface):
    print("[*] Stopping interfering processes...")
    res = run_command(['systemctl', 'stop', 'NetworkManager'], capture=True)
    if res and res.returncode != 0:
        run_command(['service', 'NetworkManager', 'stop'])
    run_command(['pkill', '-9', 'wpa_supplicant'])

    print(f"[*] Bringing interface {interface} down...")
    run_command(['ip', 'link', 'set', interface, 'down'])

    print(f"[*] Setting {interface} to monitor mode...")
    res = run_command(['iw', 'dev', interface, 'set', 'type', 'monitor'], capture=True)
    if res and res.returncode != 0:
        run_command(['iwconfig', interface, 'mode', 'monitor'])

    print(f"[*] Bringing interface {interface} up...")
    run_command(['ip', 'link', 'set', interface, 'up'])

    print(f"[+] Monitor mode enabled on {interface}")

def stop_monitor_mode(interface):
    print(f"[*] Bringing interface {interface} down...")
    run_command(['ip', 'link', 'set', interface, 'down'])

    print(f"[*] Setting {interface} to managed mode...")
    res = run_command(['iw', 'dev', interface, 'set', 'type', 'managed'], capture=True)
    if res and res.returncode != 0:
        run_command(['iwconfig', interface, 'mode', 'managed'])

    print(f"[*] Bringing interface {interface} up...")
    run_command(['ip', 'link', 'set', interface, 'up'])

    print("[*] Restarting NetworkManager...")
    res = run_command(['systemctl', 'restart', 'NetworkManager'], capture=True)
    if res and res.returncode != 0:
        run_command(['service', 'NetworkManager', 'restart'])

    print(f"[+] Managed mode restored on {interface}")

def rescan_wifi(interface, delay=4):
    print("[*] Exiting monitor mode to perform rescan...")
    stop_monitor_mode(interface)

    print(f"[*] Waiting {delay} seconds for NetworkManager to initialize...")
    time.sleep(delay)

    print("[*] Scanning WiFi networks...")
    run_command(['nmcli', 'device', 'wifi', 'list'])

    print(f"[*] Re-enabling monitor mode on {interface}...")
    start_monitor_mode(interface)

def print_help():
    print("""
Usage: wpt-mode [--start | -s | --exit | -e | --rescan | -r] <interface> [options]

Options:
  -h, --help                    Display this help message and exit
  -d, --delay <seconds>         Set custom delay before rescan (default is 4 seconds)

Commands:
  --start, -s                   Start monitor mode on specified interface
  --exit, -e                    Exit monitor mode and restart NetworkManager
  --rescan, -r                  Rescan WiFi networks after exiting monitor mode

Examples:
  wpt-mode --start wlan0
  wpt-mode --exit wlan0
  wpt-mode --rescan wlan0 -d 6
""")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print_help()
        sys.exit(0)

    mode = sys.argv[1]
    interface = 'wlan0'
    delay = 4

    args = sys.argv[2:]
    idx = 0
    while idx < len(args):
        arg = args[idx]
        if arg in ['-d', '--delay']:
            if idx + 1 < len(args):
                try:
                    delay = int(args[idx + 1])
                    idx += 2
                    continue
                except ValueError:
                    print(f"Error: Invalid delay value '{args[idx + 1]}'")
                    print_help()
                    sys.exit(1)
            else:
                print("Error: Delay option requires a value")
                print_help()
                sys.exit(1)
        elif not arg.startswith('-'):
            interface = arg
            idx += 1
        else:
            print(f"Error: Unknown option '{arg}'")
            print_help()
            sys.exit(1)

    if mode in ['--start', '-s']:
        start_monitor_mode(interface)
    elif mode in ['--exit', '-e']:
        stop_monitor_mode(interface)
    elif mode in ['--rescan', '-r']:
        rescan_wifi(interface, delay)
    else:
        print(f"Error: Unknown command '{mode}'")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
