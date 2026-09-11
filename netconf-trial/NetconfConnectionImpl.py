# netconf_connection.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Iterable
from ncclient import manager
from ncclient.operations import RPCError

@dataclass
class NetconfConnection:
    host: str = "127.0.0.1"
    port: int = 830
    username: str = "root"
    password: str = "root"
    timeout: int = 20
    hostkey_verify: bool = False
    allow_agent: bool = False
    look_for_keys: bool = False
    device_params: Optional[dict] = field(default_factory=lambda: {"name": "default"})

    _m: Optional[manager.Manager] = field(default=None, init=False, repr=False)
    _caps: Optional[Iterable[str]] = field(default=None, init=False, repr=False)

    # --- lifecycle -----------------------------------------------------------
    def connect(self) -> "NetconfConnection":
        if self._m and self._m.connected:
            return self
        self._m = manager.connect(
            host=self.host, port=self.port,
            username=self.username, password=self.password,
            hostkey_verify=self.hostkey_verify,
            allow_agent=self.allow_agent,
            look_for_keys=self.look_for_keys,
            device_params=self.device_params,
            timeout=self.timeout
        )
        self._caps = list(self._m.server_capabilities)
        return self

    def close(self) -> None:
        if self._m:
            try:
                self._m.close_session()
                print("Connection closed...")
            finally:
                self._m = None

    # context manager sugar:  with NetconfConnection(...) as nc: ...
    def __enter__(self) -> "NetconfConnection":
        return self.connect()

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # --- helpers -------------------------------------------------------------
    @property
    def is_connected(self) -> bool:
        return bool(self._m and self._m.connected)

    @property
    def capabilities(self) -> Iterable[str]:
        if not self.is_connected:
            self.connect()
        return self._caps or []

    def get_config(self, source: str = "running", filter_xml: Optional[str] = None):
        """Read configuration datastore (running|startup|candidate)."""
        if not self.is_connected:
            self.connect()
        if filter_xml:
            return self._m.get_config(source=source, filter=filter_xml)
        return self._m.get_config(source=source)

    def get(self, filter_xml: Optional[str] = None):
        """Read state data (operational) via <get>."""
        if not self.is_connected:
            self.connect()
        if filter_xml:
            return self._m.get(filter=filter_xml)
        return self._m.get()

    # --- write paths ---------------------------------------------------------
    def edit_running(self, config_xml: str, default_operation: str = "merge"):
        """Directly edit <running>. Use only if the device allows it."""
        if not self.is_connected:
            self.connect()
        return self._m.edit_config(target="running", config=config_xml,
                                   default_operation=default_operation)

    def edit_candidate_commit(self, config_xml: str,
                              default_operation: str = "merge",
                              confirmed: bool = False, confirm_timeout: int = 60):
        """
        Safe flow:
          lock(candidate) -> edit -> validate -> (confirmed-)commit -> unlock
        Rolls back automatically on RPCError.
        """
        if not self.is_connected:
            self.connect()
        try:
            self._m.lock(target="candidate")
            self._m.edit_config(target="candidate", config=config_xml,
                                default_operation=default_operation)
            # validate if supported
            if any("capability:validate" in c for c in self.capabilities):
                self._m.validate()
            if confirmed and any("confirmed-commit" in c for c in self.capabilities):
                return self._m.commit(confirmed=True, timeout=confirm_timeout)
            else:
                return self._m.commit()
        except RPCError as e:
            # discard on error to keep candidate clean
            try:
                self._m.discard_changes()
            except Exception:
                pass
            raise
        finally:
            try:
                self._m.unlock(target="candidate")
            except Exception:
                pass

    def discard_candidate(self):
        if not self.is_connected:
            self.connect()
        return self._m.discard_changes()