#!/usr/bin/python

"""Hypertune app."""

import os
import datetime
import argparse
from argparse import RawTextHelpFormatter
import yaml
import numpy as np
from config_processing import parse_config, get_black_box
from tt_opt import maximize

SRC_DIR = os.path.dirname(os.path.realpath(__file__))

def main():
    """Hypertune main function."""

    with open(SRC_DIR + "/hypertune_description.txt",
            "r", encoding='utf-8') as file:
        description = file.read()
    parser = argparse.ArgumentParser(
        prog='Hypertuner',
        description=description,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("--path", "-p", default=os.getcwd() + "/process",
                        help=
"a path to an executable that runs a process being optimized \
(default to /current/working/dir/process)"
    )
    parser.add_argument("--config", "-c", default=os.getcwd() + "/config.yaml",
                        help=
"a path to a hypertuner `yaml` config (default to /current/working/dir/config.yaml)"
    )
    parser.add_argument("--num-parallel", type=int, default=os.cpu_count(),
                        help=
f"maximal number of processes run parallel (default to {os.cpu_count()})"
    )
    args = parser.parse_args()
    task_info = {
        "task_info": {
            "timestamp": datetime.datetime.now(),
            "process_path": args.path,
            "config_path": args.config,
            "parallel_processes_number": args.num_parallel,
        }
    }
    print(yaml.safe_dump(task_info))
    with open(args.config, "r", encoding='ascii') as file:
        config = parse_config(file.read())
    func = get_black_box(config, args.path, args.num_parallel)
    _, _ = maximize(
        func,
        np.array(config.modes_dimensions),
        config.max_rank,
        config.sweeps_number,
        config.maxvol_threshold,
        config,
    )


if __name__ == '__main__':
    main()
