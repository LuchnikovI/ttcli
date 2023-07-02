#!/usr/bin/env bash

ci_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

. ${ci_dir}/utils.sh

log INFO "Running typechecker..."

if . "${ci_dir}/../ttcli.sh" typecheck; then
    log INFO Type checking OK
else
    log ERROR Type checking failed
    exit 1
fi

log INFO "Running tests..."

if . "${ci_dir}/../ttcli.sh" test; then
    log INFO Testing OK
else
    log ERROR Testing failed
    exit 1
fi

log INFO "Running linter..."

if . "${ci_dir}/../ttcli.sh" lint; then
    log INFO Linting OK
else
    log ERROR Linting failed
    exit 1
fi

log INFO "Success"