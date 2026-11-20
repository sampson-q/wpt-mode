# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com), versioning follows [Semantic Versioning](https://semver.org).

## [Unreleased]
### Changed
- Refactored monitor mode switching to use granular Linux commands (`ip link`, `iw`, `nmcli`) instead of relying on the `aircrack-ng` suite.
- Interface names are now preserved directly without appending a `mon` suffix.
- Updated `setup.sh` to check for granular networking dependencies (`ip`, `iw`, `nmcli`).
- Updated documentation and case study in `README.md` reflecting granular network controls.

### Added
- Automatic fallback to `iwconfig` if `iw` is not supported.
- Clear status and error messages during mode switching operations.
- Flexible command-line argument parsing supporting options before or after the interface.

## [1.0.0] - original release
*Tagged retroactively; the project was not versioned at the time.*
### Added
- `--start` / `-s`: kill interfering processes (`airmon-ng check kill`) and enable monitor mode
- `--exit` / `-e`: disable monitor mode and restart NetworkManager
- `--rescan` / `-r`: rescan WiFi networks via `nmcli` after exiting monitor mode
- `-d` / `--delay`: custom delay before rescan (default 4 seconds)
- `setup.sh` to install dependencies and make `wpt-mode` available system-wide
