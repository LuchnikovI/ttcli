#!/usr/bin/python

# pylint: skip-file

import sys
import yaml
import numpy as np


def _encoder(index):
    if index is None:
        return None
    weights = 1 / (2 ** np.arange(0, 20))
    return np.array(np.tensordot(index, weights, axes=1))


def _function(arg):
    return np.cos(250 * (arg - 1.23456789)) / ((arg - 1.23456789) ** 2 + 0.0001)\
          + 500 * (arg - 1.23456789) ** 2


def main():
    config = yaml.safe_load(sys.stdin)
    params = np.array([
        int(config["x0"]), int(config["x1"]), int(config["x2"]), int(config["x3"]), int(config["x4"]),
        int(config["x5"]), int(config["x6"]), int(config["x7"]), int(config["x8"]), int(config["x9"]),
        int(config["x10"]), int(config["x11"]), int(config["x12"]), int(config["x13"]), int(config["x14"]),
        int(config["x15"]), int(config["x16"]), int(config["x17"]), int(config["x18"]), int(config["x19"]),
    ])
    print(float(_function(_encoder(params))))
    return 0


if __name__ == '__main__':
    main()
