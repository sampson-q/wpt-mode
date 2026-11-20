# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com), versioning follows [Semantic Versioning](https://semver.org).

## [Unreleased]
### Changed
- Rewrite in progress (v2.0.0)

## [1.0.0] - original release
*Tagged retroactively; the project was not versioned at the time.*
### Added
- `--start` / `-s`: kill interfering processes (`airmon-ng check kill`) and enable monitor mode
- `--exit` / `-e`: disable monitor mode and restart NetworkManager
- `--rescan` / `-r`: rescan WiFi networks via `nmcli` after exiting monitor mode
- `-d` / `--delay`: custom delay before rescan (default 4 seconds)
- `setup.sh` to install dependencies and make `wpt-mode` available system-wide
