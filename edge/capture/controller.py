"""Drives the stereo camera + LiDAR unit and returns a registered RGB-D capture.

The handheld is a thin capture device: it grabs synchronized stereo RGB frames and a
LiDAR depth map / point cloud, registers them, and streams the bundle to the paired
mobile app. The mobile app relays it to the cloud, where inference and grading run.
No defect inference happens on-device.
"""
from dataclasses import dataclass, field
from typing import Optional
import numpy as np


@dataclass
class RGBDCapture:
    """One slab-patch capture from the stereo + LiDAR unit."""

    rgb: np.ndarray                              # H x W x 3, rectified colour image
    depth: np.ndarray                            # H x W, metric depth (m), registered to rgb
    point_cloud: Optional[np.ndarray] = None     # N x 3 LiDAR cloud (optional, for 3D surface relief)
    metadata: dict = field(default_factory=dict)  # device id, timestamp, calibration ref


class CaptureController:
    """Triggers a capture and returns a registered RGB-D frame.

    Implementations own stereo rectification and LiDAR->RGB registration (extrinsic
    calibration), plus exposure/focus validation. They do not run any model.
    """

    def capture_patch(self) -> RGBDCapture:
        raise NotImplementedError
