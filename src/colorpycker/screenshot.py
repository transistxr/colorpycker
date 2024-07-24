import re
import random
from PySide6 import QtCore, QtDBus, QtGui
from typing import Optional
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlparse

from PySide6 import QtCore, QtDBus, QtGui


class FdskTopInterface(QtDBus.QDBusAbstractInterface):
    DBusResponse = QtCore.Signal(QtDBus.QDBusMessage)

    def __init__(
        self, path: str, connection: QtDBus.QDBusConnection, parent: QtCore.QObject
    ) -> None:
        super().__init__(
            "org.freedesktop.portal.Desktop",
            path,
            "org.freedesktop.portal.Request",
            connection,
            parent,
        )


class FdskTopScreenShot(QtCore.QObject):
    on_response = QtCore.Signal(QtDBus.QDBusMessage)
    on_result = QtCore.Signal(str)

    def __init__(self, parent: Optional[QtCore.QObject] = None, timeout_sec: int = 15):
        super().__init__(parent)
        self.timeout_timer = self._get_timeout_timer(timeout_sec)
        self.on_response.connect(self.got_signal)

    def grab_desktop(self) -> None:
        bus = QtDBus.QDBusConnection.sessionBus()

        base = bus.baseService()[1:].replace(".", "_")

        random_str = "".join(random.choice("aXYdBgFPi") for _ in range(8))
        token = f"colorpycker_{random_str}"
        object_path = f"/org/freedesktop/portal/desktop/request/{base}/{token}"

        request = FdskTopInterface(object_path, bus, self)
        request.DBusResponse.connect(self.on_response)
        interface = QtDBus.QDBusInterface(
            "org.freedesktop.portal.Desktop",
            "/org/freedesktop/portal/desktop",
            "org.freedesktop.portal.Screenshot",
            bus,
            self,
        )

        message = interface.call(
            "Screenshot", "", {"interactive": False, "handle_token": token}
        )

        print("Message call: %s", str(message))

    def _get_timeout_timer(self, timeout_sec: int) -> QtCore.QTimer:

        def _timeout_triggered() -> None:
            msg = f"No response from xdg-portal within {timeout_sec}s!"
            self.on_exception.emit(TimeoutError(msg))

        timeout_timer = QtCore.QTimer()
        timeout_timer.setSingleShot(True)
        timeout_timer.setInterval(timeout_sec * 1000)
        timeout_timer.timeout.connect(_timeout_triggered)
        return timeout_timer

    def got_signal(self, message: QtDBus.QDBusMessage) -> None:
        self.timeout_timer.stop()
        print("Message Signal: %s", str(message))
        reg_uri = r"""
                  \[Variant\(QString\)\:\ \"
                  (.*)                       
                  \"\]\}                     
                  """
        result = re.search(reg_uri, str(message), re.VERBOSE)
        print("reg_uri: %s", reg_uri)
        print("result val: %s", result)
        uri = result.group(1)
        self.on_result.emit(uri)
        self.close()


def capture():

    loop = QtCore.QEventLoop()
    result = []

    def _signal_triggered(uri: str) -> None:
        print(uri)
        result.append(uri)
        loop.exit()

    portal = FdskTopScreenShot(timeout_sec=10)
    portal.on_result.connect(_signal_triggered)

    QtCore.QTimer.singleShot(0, portal.grab_desktop)

    loop.exec()

    portal.on_result.disconnect(_signal_triggered)

    print(result[0])
    uri = result[0]
    parsed_uri = urlparse(uri)
    parsed_path = unquote(parsed_uri.path)

    image_path = Path(parsed_path)
    image = QtGui.QImage(image_path)

    image_path.unlink()
    return image
