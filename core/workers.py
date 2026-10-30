"""Qt workers for SDB commands, network discovery and package installation."""

from __future__ import annotations

import socket
from concurrent.futures import ThreadPoolExecutor

from PySide6.QtCore import QThread, Signal

from core.sdb import DEFAULT_PORT, SDBManager

SCAN_TIMEOUT_SECONDS = 0.3
SCAN_WORKERS = 50


class SDBCommandWorker(QThread):
    """Run a shell command off the GUI thread."""

    finished = Signal(bool, str)

    def __init__(self, command: str, sdb_manager: SDBManager | None = None):
        super().__init__()
        self.command = command
        self.sdb = sdb_manager or SDBManager()

    def run(self) -> None:
        success, output = self.sdb.shell(self.command)
        self.finished.emit(success, output)


class NetworkScanWorker(QThread):
    """Discover devices accepting SDB on the local IPv4 /24 subnet."""

    progress = Signal(str)
    finished = Signal(list)

    def __init__(self, sdb_manager: SDBManager):
        super().__init__()
        self.sdb = sdb_manager
        self.port = DEFAULT_PORT

    @staticmethod
    def get_local_ip() -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
                connection.connect(("10.255.255.255", 1))
                return connection.getsockname()[0]
        except OSError:
            return "127.0.0.1"

    def check_ip_port(self, ip: str) -> str | None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
                connection.settimeout(SCAN_TIMEOUT_SECONDS)
                if connection.connect_ex((ip, self.port)) == 0:
                    return ip
        except OSError:
            pass
        return None

    def run(self) -> None:
        local_ip = self.get_local_ip()
        if local_ip == "127.0.0.1":
            self.finished.emit([])
            return

        subnet = ".".join(local_ip.split(".")[:3]) + "."
        self.progress.emit(f"Scanning subnet {subnet}0/24...")
        addresses = (f"{subnet}{host}" for host in range(1, 255))
        with ThreadPoolExecutor(max_workers=SCAN_WORKERS) as executor:
            found = [address for address in executor.map(self.check_ip_port, addresses) if address]
        self.finished.emit(found)


class SideloadWorker(QThread):
    """Install a Tizen package without blocking the GUI thread."""

    finished = Signal(bool, str)

    def __init__(self, tpk_path: str, sdb_manager: SDBManager | None = None):
        super().__init__()
        self.tpk_path = tpk_path
        self.sdb = sdb_manager or SDBManager()

    def run(self) -> None:
        success, message = self.sdb.install_app(self.tpk_path)
        self.finished.emit(success, message)
