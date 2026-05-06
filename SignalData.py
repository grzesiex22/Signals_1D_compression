from dataclasses import dataclass
import numpy as np

@dataclass
class SignalData:
    t: np.ndarray
    y: np.ndarray