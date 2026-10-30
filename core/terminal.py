"""Synchronous terminal facade for commands sent through SDB."""

from __future__ import annotations

from core.sdb import SDBManager


class TerminalManager:
    def __init__(self, sdb_manager: SDBManager | None = None):
        self.sdb = sdb_manager or SDBManager()

    def execute(self, command: str) -> tuple[bool, str]:
        return self.sdb.shell(command)
