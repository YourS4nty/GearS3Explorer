"""Safe, synchronous wrapper around the Tizen SDB command line tool."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path

from core.devices import Device

DEFAULT_SDB_PATH = Path(r"C:\tizen-studio\tools\sdb.exe")
DEFAULT_PORT = 26101


class SDBManager:
    """Run SDB operations and expose Gear S3 specific helpers."""

    def __init__(self, executable: str | Path | None = None):
        self.sdb = Path(executable) if executable else self._resolve_executable()

    @staticmethod
    def _resolve_executable() -> Path:
        bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
        bundled = bundle_dir / "vendor" / "sdb" / "sdb.exe"
        sdk = Path(os.environ.get("TIZEN_SDB_PATH", str(DEFAULT_SDB_PATH)))
        return bundled if bundled.is_file() else sdk

    def _run(self, args: list[str], timeout: int = 60) -> tuple[int, str, str]:
        if not self.sdb.is_file():
            return 127, "", f"SDB executable not found: {self.sdb}"

        options = {
            "capture_output": True,
            "text": True,
            "encoding": "utf-8",
            "errors": "replace",
            "timeout": timeout,
            "check": False,
        }
        if sys.platform == "win32":
            options["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)

        try:
            result = subprocess.run([str(self.sdb), *args], **options)
            return result.returncode, result.stdout.strip(), result.stderr.strip()
        except FileNotFoundError:
            return 127, "", f"SDB executable not found: {self.sdb}"
        except PermissionError:
            return 126, "", f"Windows denied access to SDB: {self.sdb}"
        except subprocess.TimeoutExpired:
            return 124, "", f"SDB command timed out after {timeout} seconds"
        except OSError as exc:
            return 126, "", f"Could not start SDB: {exc}"

    def connect(self, ip: str) -> tuple[bool, str]:
        address = ip.strip()
        if not address:
            return False, "A device IP address is required."
        if ":" not in address:
            address = f"{address}:{DEFAULT_PORT}"
        code, stdout, stderr = self._run(["connect", address])
        if code == 0 and any(token in stdout.lower() for token in ("connected to", "already connected")):
            return True, stdout
        return False, stderr or stdout

    def shell(self, command: str) -> tuple[bool, str]:
        code, stdout, stderr = self._run(["shell", command])
        return (True, stdout) if code == 0 else (False, stderr or stdout)

    def _shell_value(self, command: str, fallback: str) -> str:
        success, value = self.shell(command)
        return value.strip().replace("\r", "") if success and value.strip() else fallback

    def devices(self) -> list[Device]:
        code, stdout, _ = self._run(["devices"])
        if code != 0:
            return []

        endpoints: list[tuple[str, int]] = []
        for line in stdout.splitlines():
            fields = line.split()
            if not fields or fields[0].startswith("List of devices") or ":" not in fields[0]:
                continue
            host, separator, port_text = fields[0].rpartition(":")
            if not separator:
                continue
            try:
                endpoints.append((host, int(port_text)))
            except ValueError:
                continue

        if not endpoints:
            return []

        model = self._shell_value("vconf-get db/system/model", "Gear S3 (SM-R760)")
        release = self._shell_value("cat /etc/tizen-release", "Tizen 3.0.0")
        tizen_version = next(
            (line.replace("VERSION =", "").strip() for line in release.splitlines()
             if "VERSION" in line or "Tizen" in line),
            release,
        )
        kernel = self._shell_value("uname -r", "Linux Kernel")
        battery = self._read_battery()

        return [
            Device(
                name=model, ip=host, port=port, connected=True,
                tizen_version=tizen_version, kernel=kernel,
                cpu="Exynos 7270", ram="768 MB", storage="4 GB", battery=battery,
            )
            for host, port in endpoints
        ]

    def _read_battery(self) -> str:
        value = self._shell_value("vconf-get db/system/battery_level", "")
        if not value.isdigit():
            value = self._shell_value("cat /sys/class/power_supply/battery/capacity", "")
        return f"{value}%" if value.isdigit() else "100%"

    def install_app(self, local_path: str | Path) -> tuple[bool, str]:
        package = str(local_path)
        if package.lower().endswith(".wgt"):
            remote_path = f"/tmp/{Path(package).name}"
            push_code, stdout, stderr = self._run(["push", package, remote_path])
            if push_code != 0:
                return False, f"Failed to push .wgt to watch:\n{stderr or stdout}"

            success, output = self.shell(f"pkgcmd -i -t wgt -p {shlex.quote(remote_path)}")
            self.shell(f"rm {shlex.quote(remote_path)}")
            has_error = any(word in output.lower() for word in ("error", "failed", "fail"))
            if success and not has_error:
                return True, f"Web app installed successfully!\n\nShell Output:\n{output}"
            return False, f"Web app installation failed.\n\nShell Output:\n{output}"

        code, stdout, stderr = self._run(["install", package])
        output = f"{stdout} {stderr}".lower()
        if code == 0 and ("installed" in output or "success" in output):
            return True, stdout
        return False, stderr or stdout
