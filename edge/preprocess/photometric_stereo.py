"""Compute surface normals and albedo from a multi-angle frame set."""
from dataclasses import dataclass
import numpy as np

from edge.capture.controller import FrameSet


@dataclass
class SurfaceMap:
    normals: np.ndarray   # H x W x 3
    albedo: np.ndarray    # H x W


def compute_surface_map(frame_set: FrameSet) -> SurfaceMap:
    raise NotImplementedError
