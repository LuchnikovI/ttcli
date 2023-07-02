#!/usr/bin/python

"""Plotting app"""

import sys
import os
import argparse
from argparse import RawTextHelpFormatter
import yaml
import matplotlib.pyplot as plt

SRC_DIR = os.path.dirname(os.path.realpath(__file__))

def main():
    """Plotting main function."""

    parser = argparse.ArgumentParser(
        prog='Hypertuner',
        description=
"Makes a plot with some metrics obtained during hypertuning \
and saves it along with hypertuning logs file.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("--path", "-p", required=False, default=os.getcwd() + "/logs.yaml",
                        help=
"a path to a file with hypertuning logs (default to /current/working/dir/logs.yaml)"
    )
    args = parser.parse_args()
    filename = os.path.splitext(os.path.basename(args.path))[0]
    dirname = os.path.dirname(args.path)
    with open(args.path, "r", encoding='ascii') as file:
        logs = yaml.safe_load(file)
    calls_number = []
    max_value = []
    idx = 0
    while idx in logs:
        calls_number.append(logs[idx]["calls_number"])
        max_value.append(logs[idx]["max_value"])
        idx += 1
    iterations = list(range(len(calls_number)))
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Iteration')
    ax1.plot(iterations, calls_number, '-', color="red")
    ax1.tick_params(axis='y', labelcolor="red")
    ax1.set_ylabel("number of function calls", color="red")
    ax2 = ax1.twinx()
    while max_value[0] == -sys.float_info.max:
        max_value = max_value[1:]
        iterations = iterations[1:]
    ax2.set_ylabel('value', color="blue")
    ax2.plot(iterations, max_value, '-', color="blue")
    ax2.tick_params(axis='y', labelcolor="blue")
    fig.tight_layout()
    plt.savefig(dirname + "/" + filename + ".pdf")


if __name__ == '__main__':
    main()
