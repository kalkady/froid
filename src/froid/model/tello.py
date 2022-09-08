from bpyutils.model.base import BaseObject
from bpyutils.util.array import sequencify
from bpyutils.log import get_logger
from bpyutils._compat import iteritems

from djitellopy import Tello as DJITelloPy

class TelloError(Exception):
    pass

class Tello(BaseObject):
    _STATE_PROPS = {
        "roll": None,
        "yaw": None,
        "battery": None,
        "height": None,
        "flight_time": None,
        "barometer": None,
    }

    def __init__(self, *args, **kwargs):
        docker = kwargs.pop("docker", False)
        DJITelloPy.DOCKER = docker

        self._tello  = DJITelloPy(*args, **kwargs)
        self._logger = get_logger("tello")

        self._state  = { }

    @property
    def connected(self):
        return self._state.get("connected")

    @property
    def frame(self):
        frame_read = self._exec_command(self._tello.get_frame_read,
            before_cmd_log = "Fetching frame read...",
            after_cmd_log  = "Frame read fetched."
        )
        frame = frame_read.frame

        return frame

    def _set_tello_state_fns(self):
        for attr, conf in iteritems(Tello._STATE_PROPS):
            if not conf:
                conf = { "type": int }
            else:
                if "type" not in conf:
                    conf["type"] = int
            
            setattr(self, attr, lambda c=conf, a=attr:
                conf["type"](self._get_state(a)))

    def _get_state(self, attr):
        self._check_connected()

        fn_name = "get_%s" % attr
        fn_attr = getattr(self._tello, fn_name, None)

        if not fn_attr:
            raise ValueError("No state %s found." % attr)

        return fn_attr()

    def _set_state(self, state, value):
        self._state[state] = value

    def connect(self, *args, **kwargs):
        stream_on = kwargs.pop("stream_on", False)

        def _connect():
            self._tello.connect(*args, **kwargs)
            self._set_state("connected", True)

        self._exec_command(_connect,
            before_cmd_log = "Connecting...",
            after_cmd_log  = "Connected."
        )

        self._set_tello_state_fns()

        if stream_on:
            self._exec_command(self._tello.streamon,
                before_cmd_log = "Turning camera on...",
                after_cmd_log  = "Camera ready."
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
        
        result = cmd()

        for log in after_cmd_log:
            self._logger.success(log)

        return result

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