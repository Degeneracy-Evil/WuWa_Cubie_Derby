from enum import Enum


class DeviceType(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    DISRUPTION = "disruption"


DEVICE_MAP = {
    2: DeviceType.FORWARD,
    10: DeviceType.FORWARD,
    15: DeviceType.FORWARD,
    22: DeviceType.FORWARD,
    9: DeviceType.BACKWARD,
    27: DeviceType.BACKWARD,
    5: DeviceType.DISRUPTION,
    19: DeviceType.DISRUPTION,
}

TRACK_LENGTH = 32
START_POS = 0
FINISH_POS = 31


def get_device(pos: int) -> DeviceType | None:
    return DEVICE_MAP.get(pos)
