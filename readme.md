# Description

This is an experimental attempt to wrap ugly research code into a useful cli tool.
This cli is a hyperoptimizer meaning that it tunes hyperparameters of a black box.

# How to install

Run an instalation script `./ci/install`. You do not need to have the rest of the code, only this script. Note, that the cli is based on [Apptainer](https://apptainer.org/) and install it if necessary into the `$HOME` dir.

# How to uninstall

All the artefacts after installation are located in `$HOME/ttcli`, simply `rm` this dirrectory. You also need to exclude the corresponding record from `.bashrc` which brings the tool into `PATH`. You may also delete Apptainer and the corresponding `.bashrc` record if you no longer need it.

# How to use

Run `ttcli help` for the reference.
The most essential piece of documentation is given by `ttcli hypertune --help` and reads:

```
usage: Hypertuner [-h] [--path PATH] [--config CONFIG] [--num-parallel NUM_PARALLEL]

Hypertuner optimizes an arbitrary process by running it multiple times,
adaptively searching for the best set of parameters. Process must take
parameters as a `yaml` config via standard input and send the corresponding
score value to the standard output. Hypertuner tries to maximize this value
using so called TTOpt algorithm (see https://arxiv.org/abs/2205.00293).
A `yaml` config that process takes as an input has the following form:
    name_1: value_1
    name_2: value_2
         ...
    name_k: value_k
where `name_#` is an arbitrary string specifying a name of a parameter,
`value_#` is anything that is accepted by the process.
The Hypertuner itself also takes a `yaml` config as an input that has the
following form:
    max_rank: n
    sweeps_number: m
    maxvol_threshold: a
    task_config:
        name_1: [value_11, value_12, ...]
        name_2: [value_21, value_22, ...]
            ...
        name_k: [value_k1, value_k2, ...]
where
    `max_rank`: is the maximal TT rank allowed, typically a number around 10,
    `sweeps_number`: is the number of DMRG sweeps, typically a number less than 10,
    `maxvol_threshold`: is an accuracy of MaxVol algorithm, typically a value around 0.01,
    `task_config`: is the process config, where instead of a single value per name
        all allowed values are listed. The hypertuner searches the best set of parameters
        among these possible values.

options:
  -h, --help            show this help message and exit
  --path PATH, -p PATH  a path to an executable that runs a process being optimized (default to /current/working/dir/process)
  --config CONFIG, -c CONFIG
                        a path to a hypertuner `yaml` config (default to /current/working/dir/config.yaml)
  --num-parallel NUM_PARALLEL
                        maximal number of processes run parallel (default to 1)
```
Run this command in your system since some of the options are platform specific.

# Examples

You can find examples of configs and corresponding executables in `./src/exmples` directory. You can try to run `ttcli` with this examples. For instance,
```
ttcli hypertune \
    --config ./src/examples/1d_function_config.yaml \
    --path ./src/examples/1d_function.py
```
would run maximization of a simple one-dimensional function