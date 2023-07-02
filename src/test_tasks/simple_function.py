#!/usr/bin/python

# pylint: skip-file

import sys
import yaml

def main():
    config = yaml.safe_load(sys.stdin)
    print(config["param1"] + config["param2"] + config["param3"])
    return 0


if __name__ == '__main__':
    main()
