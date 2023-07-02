"""Tests for configs processing utils"""

import os
import numpy as np
import yaml
from config_processing import (
    parse_config,
    index2config,
    get_black_box,
)

SRC_DIR = os.path.dirname(os.path.realpath(__file__))

def test_config_correct():
    """Tests a correct config."""

    with open(SRC_DIR + "/test_configs/test_config_correct.yaml",
              "r", encoding='ascii') as file:
        config = parse_config(file.read())
    assert config.max_rank == 5
    assert config.sweeps_number == 6
    assert config.maxvol_threshold == 0.01
    assert config.task_config == [
        ("param1", ["a", "b", "c"]),
        ("param2", [0, 1, 2]),
        ("param3", ["arg1", "arg2"]),
    ]


def test_config_extra_field():
    """Tests a config with extra field"""

    with open(SRC_DIR + "/test_configs/test_config_extra_field.yaml",
              "r", encoding='ascii') as file:
        config = parse_config(file.read())
    assert config.max_rank == 5
    assert config.sweeps_number == 6
    assert config.maxvol_threshold == 0.01
    assert config.task_config == [
        ("param1", ["a", "b", "c"]),
        ("param2", [0, 1, 2]),
        ("param3", ["arg1", "arg2"]),
    ]


def test_config_missing_task_field():
    """Tests a config without task config"""

    with open(SRC_DIR + "/test_configs/test_config_missing_task_field.yaml",
              "r", encoding='ascii') as file:
        config = parse_config(file.read())
    assert config.max_rank == 5
    assert config.sweeps_number == 6
    assert config.maxvol_threshold == 0.01
    assert not config.task_config


def test_config_missing_some_field():
    """Tests a config with extra field"""

    with open(SRC_DIR + "/test_configs/test_config_missing_some_field.yaml",
              "r", encoding='ascii') as file:
        config = parse_config(file.read())
    assert config.max_rank == 5
    assert config.sweeps_number == 6
    assert config.maxvol_threshold == 0.1
    assert config.task_config == [
        ("param1", ["a", "b", "c"]),
        ("param2", [0, 1, 2]),
        ("param3", ["arg1", "arg2"]),
    ]


def test_index2config():
    """Tests index to config transformation."""

    with open(SRC_DIR + "/test_configs/test_config_correct.yaml",
              "r", encoding='ascii') as file:
        config = parse_config(file.read())
    assert yaml.safe_dump({"param1": "a", "param2": 2, "param3": "arg2"}) ==\
        index2config(config, np.array([0, 2, 1]))


def test_get_black_box():
    """Tests black box function."""

    with open(SRC_DIR + "/test_tasks/simple_config.yaml",
              "r", encoding='ascii') as file:
        config = parse_config(file.read())
    black_box = get_black_box(config, SRC_DIR + "/test_tasks/simple_function.py", 3)
    values = black_box(np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0, 2, 0],
        [2, 1, 0],
        [2, 1, 2],
        [2, 2, 2],
        [1, 1, 1],
        [1, 2, 0]
    ]))
    exact_values = np.array([111, 112, 131, 123, 323, 333, 222, 132], dtype=np.float64)
    assert np.isclose(values, exact_values).all()
