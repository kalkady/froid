from bpyutils.model.base import BaseObject
from bpyutils.util.array import sequencify
from bpyutils.log import get_logger

from djitellopy import Tello as DJITelloPy

class TelloError(Exception):
    pass

class Tello(BaseObject):
    def __init__(self, *args, **kwargs):
        self._tello  = DJITelloPy(*args, **kwargs)
        self._logger = get_logger("tello")

        self._is_connected = False

    @property
    def connected(self):
        return self._is_connected

    def _get_state(self, type_):
        fn_name = "get_%s" % type_
        fn_attr = getattr(self._tello, fn_name, None)

        if not fn_attr:
            raise ValueError("No state %s found." % type_)

        return fn_attr()

    @property
    def battery(self):
        return self._get_state("battery")

    def connect(self, *args, **kwargs):
        def _connect():
            self._tello.connect(*args, **kwargs)
            self._is_connected = True

        self._exec_command(_connect,
            before_cmd_log = "Connecting...",
            after_cmd_log  = "Connected."
        )

    def _check_connected(self, raise_err = True):
        connected = self.connected

        if not connected:
            if raise_err:
                raise TelloError("Tello is not connected.")
        else:
            self._logger.info("Tello already connected.")
                
        return connected

    def _exec_command(self, cmd, before_cmd_log = None, after_cmd_log = None):
        if not before_cmd_log:
            before_cmd_log = "Executing command %s" % str(cmd)
        if not after_cmd_log:
            after_cmd_log  = "Command %s executed." % str(cmd)

        before_cmd_log = sequencify(before_cmd_log)
        after_cmd_log  = sequencify(after_cmd_log)

        for log in before_cmd_log:
            self._logger.info(log)
        
        cmd()

        for log in after_cmd_log:
            self._logger.success(log)

    def takeoff(self):
        self._exec_command(self._tello.takeoff,
            before_cmd_log = "Taking off...",
            after_cmd_log  = "Took off."
        )

    def land(self):
        self._exec_command(self._tello.land,
            before_cmd_log = "Landing...",
            after_cmd_log  = "Landed."
        )