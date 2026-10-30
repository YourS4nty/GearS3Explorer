<div align="center">

# Gear S3 Explorer

**A modern Windows desktop toolkit for managing Samsung Gear S3 devices through Tizen SDB.**

[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-0078D6?logo=windows&logoColor=white)](#requirements)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![UI](https://img.shields.io/badge/UI-PySide6-41CD52?logo=qt&logoColor=white)](https://www.qt.io/qt-for-python)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-community%20project-informational)](#project-status)

*Connect · Inspect · Browse · Transfer · Sideload*

</div>

---

## Overview

Gear S3 Explorer is an independent desktop application built with **Python** and **PySide6**. It provides a unified interface for connecting to compatible Samsung Gear S3 watches over a local network using the **Tizen Smart Development Bridge (SDB)**.

The project aims to make common device-management workflows easier to access from Windows: device inspection, remote file operations, SDB shell access, and package installation.

> **Disclaimer:** This is an independent community project. It is not affiliated with, endorsed by, or supported by Samsung or the Tizen project.

## Features

- **Device connection** — connect to a Gear S3 through its local IP address and SDB.
- **Device information** — inspect available model, firmware, kernel, and battery details.
- **File manager** — browse remote directories and transfer files.
- **SDB terminal** — execute shell commands on an authorized device.
- **Package sideloading** — install compatible Tizen `.tpk` and `.wgt` packages.
- **Desktop experience** — focused dark interface built with PySide6.

Feature availability depends on the watch model, firmware, network, and device permissions.

## Requirements

- Windows 10/11 (64-bit)
- Python 3.12
- Samsung Gear S3 with compatible Tizen SDB support
- PC and watch connected to the same local network
- SDB debugging enabled and the computer authorized on the watch

## Quick start

### Windows launcher

1. Download and extract the project.
2. Install Python 3.12.
3. Run `run_from_source.bat`.

The launcher creates a virtual environment, installs the requirements, and starts the application.

### Manual installation

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

If PowerShell blocks activation, invoke the virtual environment's Python directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

## Connect your watch

1. Connect the PC and watch to the same Wi-Fi network.
2. Enable debugging on the watch and authorize the PC when prompted.
3. Open **Devices** in Gear S3 Explorer.
4. Enter the watch's local IP address and connect.
5. Use the device, file manager, terminal, or sideloading pages.

If discovery fails, connect by IP manually. Windows Firewall and router client isolation can block local connections.

## SDB configuration

The application checks for the bundled executable at `vendor/sdb/sdb.exe`. To use a separate Tizen Studio installation, set `TIZEN_SDB_PATH` before launch:

```powershell
$env:TIZEN_SDB_PATH = "C:\tizen-studio\tools\sdb.exe"
python main.py
```

## Project structure

```text
GearS3Explorer/
├── core/                 # SDB, device, filesystem and worker logic
├── ui/                   # PySide6 main window and application pages
├── vendor/sdb/           # Third-party SDB runtime files (if redistributed)
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
└── run_from_source.bat   # Windows setup and launch helper
```

## Development

Install dependencies as shown above, then run:

```powershell
python -m compileall -q core ui main.py
python main.py
```

Keep device communication logic in `core/` and UI-specific behavior in `ui/`. Use background workers for long-running operations so the Qt event loop remains responsive.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

## Security and responsible use

Use this software only with devices you own or are explicitly authorized to administer. SDB shell commands can modify or delete device data; review commands carefully and keep backups.

For security concerns, see [SECURITY.md](SECURITY.md).

## Licensing and third-party components

Original project code and documentation are provided under the **MIT License**; see [LICENSE](LICENSE).

Third-party executables and libraries are **not** relicensed by this repository. Their original copyright and license terms remain applicable. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and verify redistribution rights before publishing vendor binaries.

## Project status

Gear S3 Explorer is a community project. Compatibility has not been verified across every Gear S3 model or Tizen firmware. Tested device and firmware reports are welcome through GitHub Issues.

---

<div align="center">

**Built for the Gear S3 community.**

If you find this project useful, consider giving it a ⭐ and contributing improvements.

</div>
