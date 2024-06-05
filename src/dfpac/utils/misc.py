import os
import random
from pathlib import Path

import numpy as np
import yaml


def seed_everything(seed=1234):
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)


def shorten(bacteria: str) -> str:
    genus, species = bacteria.split(" ")
    return f"{genus[0]}. {species}"


def serialize_params(params: dict, filename: Path) -> None:
    serialized = {"classifier": params["classifier"].estimator.__class__.__name__}

    for key, val in params.items():
        if key == "classifier":
            continue

        if isinstance(val, np.float64):
            serialized[key] = float(val)

        elif isinstance(val, str) or isinstance(val, int):
            serialized[key] = val

        else:
            serialized[key] = val.__class__.__name__

    with open(filename, "w") as f:
        yaml.dump(serialized, f)
