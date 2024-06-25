#!/usr/bin/env python3
import sys
import subprocess
import time

def start_monitor_mode(interface):
    subprocess.run(['airmon-ng', 'check', 'kill'])
    subprocess.run(['airmon-ng', 'start', interface])

def stop_monitor_mode(interface):
    subprocess.run(['airmon-ng', 'stop', interface + 'mon'])
    subprocess.run(['service', 'NetworkManager', 'start'])

def rescan_wifi(interface, delay=4):
    stop_monitor_mode(interface)
    
    time.sleep(delay)
    subprocess.run(['nmcli', 'device', 'wifi', 'list'])
    start_monitor_mode(interface)

def print_help():
    print("""
Usage: wpt-mode [--start | -s | --exit | -e | --rescan | -r] <interface> [options]

Options:
  -h, --help          		Display this help message and exit
  -d, --delay <seconds>        	Set custom delay before rescan (default is 4 seconds)

Commands:
  --start, -s         Start monitor mode on specified interface
  --exit, -e          Exit monitor mode and restart NetworkManager
  --rescan, -r        Rescan WiFi networks after exiting monitor mode

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
    interface = sys.argv[2] if len(sys.argv) > 2 else 'wlan0'  # Default interface is wlan0
    
    if mode == '--start' or mode == '-s':
        start_monitor_mode(interface)
    elif mode == '--exit' or mode == '-e':
        stop_monitor_mode(interface)
    elif mode == '--rescan' or mode == '-r':
        delay = 4  # Default delay
        if len(sys.argv) > 3 and sys.argv[3] == '-d' or len(sys.argv) > 3 and sys.argv[3] == '--delay':
            try:
                delay = int(sys.argv[4])
            except (IndexError, ValueError):
                print_help()
        rescan_wifi(interface, delay)
    else:
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
