"""TTOpt"""

import sys
import datetime
from typing import Callable, Union, List, Tuple, Dict, Any
import yaml
import numpy as np
from ttrs import TTVc64  # type: ignore
from config_processing import Config


def _index2dict_config(
        config: Config,
        index: np.ndarray
) -> Dict[str, Any]:
    dict_config = {}
    for pos, subidx in enumerate(index):
        key, vals = config.task_config[pos]
        dict_config[key] = vals[subidx]
    return dict_config


def maximize(
        func: Callable[[np.ndarray], np.ndarray],
        modes_dimensions: List[int],
        max_rank: int,
        sweeps_number: int,
        maxvol_accuracy: Union[float, np.ndarray],
        config: Union[Config, None] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Maximizes a function by TTOpt method."""

    max_value = np.array(-sys.float_info.max, dtype=np.complex128)
    best_index = np.array(len(modes_dimensions) * [0])
    sweep_number = 0
    calls_number = 0
    tensor_train = TTVc64(
        modes_dimensions,
        max_rank,
        maxvol_accuracy,
        False,
    )
    modes_number = len(modes_dimensions)
    for iteration in range(modes_number * sweeps_number):
        if iteration % modes_number == 0:
            sweep_number += 1
        index = tensor_train.get_args()
        if index is None:
            tensor_train.update(None)
        else:
            val = func(index).astype(np.complex128)
            calls_number += val.shape[0]
            argmax = np.argmax(val)
            if val[argmax] > max_value:
                max_value = val[argmax]
                best_index = index[argmax]
            val = np.arctan(val - max_value) + np.pi / 2
            tensor_train.update(val)
        if config is None:
            best_config = None
        else:
            best_config = _index2dict_config(config, best_index)
        info = {
            iteration: {
                "timestamp": datetime.datetime.now(),
                "sweep_number": sweep_number,
                "calls_number": calls_number,
                "max_value": float(max_value.real),
                "best_config": best_config,
            }
        }
        print(yaml.safe_dump(info))
    final_info = {
        "result": {
            "timestamp": datetime.datetime.now(),
            "sweep_number": sweep_number,
            "calls_number": calls_number,
            "max_value": float(max_value.real),
            "best_config": best_config,
        }
    }
    print(yaml.safe_dump(final_info))
    return best_index, max_value
