"""Load and run the model bundle (anomaly + segmentation + fissure/crack discriminator)."""
from dataclasses import dataclass, field
from typing import List
import numpy as np


@dataclass
class DetectedDefect:
    defect_type: str
    confidence: float
    mask: np.ndarray


@dataclass
class InferenceResult:
    anomaly_map: np.ndarray
    defects: List[DetectedDefect] = field(default_factory=list)


class InferenceEngine:
    def __init__(self, bundle_path: str) -> None:
        raise NotImplementedError

    def run(self, normals: np.ndarray, albedo: np.ndarray) -> InferenceResult:
        raise NotImplementedError
