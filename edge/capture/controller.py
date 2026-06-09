"""Drives the LED ring + shutter sequence and returns a multi-angle frame set."""
from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class FrameSet:
    """One patch capture: N frames under N known lighting directions."""
    frames: List[np.ndarray]
    light_directions: List[tuple]
    metadata: dict


class CaptureController:
    def capture_patch(self) -> FrameSet:
        raise NotImplementedError
