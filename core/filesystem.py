"""Remote filesystem helpers backed by SDB shell commands."""

from __future__ import annotations

import posixpath
import re
import shlex
from typing import TypedDict

from core.sdb import SDBManager

_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class FilesystemItem(TypedDict):
    name: str
    is_dir: bool
    size: int
    permissions: str
    owner: str
    date: str
    path: str


class FilesystemManager:
    def __init__(self, sdb_manager: SDBManager):
        self.sdb = sdb_manager
        self.current_path = "/"

    @staticmethod
    def normalize_path(path: str) -> str:
        """Normalize remote POSIX paths while keeping them rooted at '/'."""
        return posixpath.normpath("/" + (path or "").lstrip("/"))

    def list_directory(self, path: str) -> list[FilesystemItem]:
        """List directory entries using the stable dictionary schema used by the UI."""
        normalized = self.normalize_path(path)
        success, output = self.sdb.shell(f"ls -al {shlex.quote(normalized)}")
        if not success:
            return []

        items: list[FilesystemItem] = []
        for line in output.splitlines():
            line = line.strip()
            if not line or line.startswith("total"):
                continue
            columns = line.split(None, 5)
            if len(columns) != 6:
                continue
            permissions, _links, owner, group, size_text, remainder = columns
            date_and_name = remainder.split(None, 3)
            if len(date_and_name) < 3:
                continue
            date_columns = 2 if _ISO_DATE.match(date_and_name[0]) else 3
            if len(date_and_name) <= date_columns:
                continue
            date = " ".join(date_and_name[:date_columns])
            name = " ".join(date_and_name[date_columns:])
            if name in {".", ".."}:
                continue
            is_dir = permissions.startswith("d")
            items.append({
                "name": name,
                "is_dir": is_dir,
                "size": 0 if is_dir else int(size_text),
                "permissions": permissions,
                "owner": owner,
                "date": date,
                "path": posixpath.join(normalized, name),
            })

        items.sort(key=lambda item: (not item["is_dir"], item["name"].lower()))
        self.current_path = normalized
        return items

    def get_parent_directory(self, path: str) -> str:
        """Return the parent path; '/' remains the root."""
        normalized = self.normalize_path(path)
        return posixpath.dirname(normalized.rstrip("/")) or "/"
