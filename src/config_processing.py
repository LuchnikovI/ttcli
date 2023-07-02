"""Utils for configs processing"""

import logging
from typing import (
    Any,
    Tuple,
    List,
    Callable,
)
from dataclasses import dataclass
from asyncio import (
    create_subprocess_exec,
    subprocess,
    Semaphore,
    gather,
)
import yaml
import numpy as np

logger = logging.getLogger(__name__)

# default values of TT parameters
MAX_RANK = 5
SWEEPS_NUMBER = 6
MAXVOL_THRESHOLD = 0.1

@dataclass
class Config:
    """Config class"""
    modes_number: int
    modes_dimensions: List[int]
    max_rank: int
    sweeps_number: int
    maxvol_threshold: float
    task_config: List[Tuple[str, List[Any]]]


def parse_config(yaml_str: str) -> Config:
    """Parses yaml string to a config."""

    raw_config = yaml.safe_load(yaml_str)
    try:
        task_config = raw_config.pop("task_config")
        task_config = [(str(key), val) for key, val in task_config.items()]
    except:
        logger.error(
"A task config is not specified or parsing failed: \
turning to the empty task config."
        )
        task_config = []
    modes_number = len(task_config)
    modes_dimensions = [len(val) for _, val in task_config]
    try:
        max_rank = int(raw_config.pop("max_rank"))
    except:
        logger.warning(
"A max_rank parameter is not specified: \
turning to the default value %i.", MAX_RANK
        )
        max_rank = MAX_RANK
    try:
        sweeps_number = int(raw_config.pop("sweeps_number"))
    except:
        logger.warning(
"A sweeps_number parameter is not specified: \
turning to the default value %i.", SWEEPS_NUMBER
        )
        sweeps_number = SWEEPS_NUMBER
    try:
        maxvol_threshold = float(raw_config.pop("maxvol_threshold"))
    except:
        logger.warning(
"A maxvol_threshold parameter is not specified: \
turning to the default value %f.", MAXVOL_THRESHOLD
        )
        maxvol_threshold = MAXVOL_THRESHOLD
    if len(raw_config) != 0:
        logger.warning(
"The following part of the config is not within the standard: \
%s, ignoring.", raw_config
        )
    config = Config(
        modes_number,
        modes_dimensions,
        max_rank,
        sweeps_number,
        maxvol_threshold,
        task_config,
    )
    return config


def index2config(
        config: Config,
        index: np.ndarray,
) -> str:
    """Transforms index to a task config given an index and a full config"""

    task_config = {}
    for pos, subidx in enumerate(index):
        key, vals = config.task_config[pos]
        task_config[key] = vals[subidx]
    return yaml.safe_dump(task_config)


async def run_task(
        task_path: str,
        task_config: str,
        semaphore: Semaphore,
) -> np.ndarray:
    """Runs a task given its path and a config. Returns a value calculated by a task."""

    await semaphore.acquire()
    task = await create_subprocess_exec(
        task_path,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    stdout, _ = await task.communicate(task_config.encode())
    try:
        value = np.array(float(stdout.decode()))
    except:
        logger.error(
"Unable to parse a process output (raw stdout %s) \
to a float number. Setting output to 0.", stdout
        )
        value = np.array(0)
    exit_code = await task.wait()
    if exit_code != 0:
        logger.error("One of the tasks retuned non-zero exit code %i.", exit_code)
    semaphore.release()
    return value


def get_black_box(
        config: Config,
        task_path: str,
        max_processes_number: int,
) -> Callable[[np.ndarray], np.ndarray]:
    """Returns a function that can be used as a black box function in
    TTCross based algorithms."""

    def black_box(indices: np.ndarray) -> np.ndarray:
        semaphore = Semaphore(max_processes_number)
        tasks = gather(*[
            run_task(task_path, index2config(config, index), semaphore)\
            for index in indices
        ])
        values = tasks.get_loop().run_until_complete(tasks)
        return np.array(values)
    return black_box
