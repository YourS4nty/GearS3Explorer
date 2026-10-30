"""Device-oriented facade for SDB and basic system diagnostics."""

from __future__ import annotations

from core.devices import Device
from core.sdb import SDBManager


class DeviceManager:
    """Group device discovery and diagnostics behind one injectable service."""

    def __init__(self, sdb_manager: SDBManager | None = None):
        self.sdb = sdb_manager or SDBManager()

    def list_devices(self) -> list[Device]:
        return self.sdb.devices()

    def connect(self, address: str) -> tuple[bool, str]:
        return self.sdb.connect(address)

    def system_info(self) -> dict[str, str]:
        """Return optional kernel, memory and storage snapshots from the watch."""
        commands = {
            "kernel": "uname -r",
            "memory": "cat /proc/meminfo",
            "storage": "df -h",
        }
        info: dict[str, str] = {}
        for key, command in commands.items():
            success, value = self.sdb.shell(command)
            info[key] = value if success else ""
        return info
