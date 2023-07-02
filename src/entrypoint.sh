#!/usr/bin/env bash

script_dir="$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null

help() {
cat << EOF
Usage: ttcli COMMAND

COMMANDs:
  test:      runs tests and exits with 0 code in case of success;
  typecheck: runs static code analysis and exits with 0 code in case of success;
  lint:      runs linter and exits with 0 code;
  help:      shows this message;
  hypertune: runs TTOpt based hypertuner, a utility that optimizes hyperparameters
             of an arbitrary process. (run ttcli hypertune --help for more information);
  plot:      plots different metrics obtained during hypertuning.
             (run ttcli plot --help for more information);
EOF
}

case $1 in

    help)
        help
    ;;
    test)
        python -m pytest "${script_dir}"
    ;;
    typecheck)
        python -m mypy --exclude "/examples/" "${script_dir}"
    ;;
    lint)
        python -m pylint --fail-under=9 "${script_dir}"
    ;;
    hypertune)
        shift
        "${script_dir}/hypertune.py" "$@"
    ;;
    plot)
        shift
        "${script_dir}/plot.py" "$@"
    ;;
    *)
        echo "Unknown option: '$1'"
        help
        exit 1
    ;;

esac