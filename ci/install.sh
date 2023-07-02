#!/usr/bin/env bash

if singularity --help &> /dev/null; then
    :
else
    echo "Singularity not found. Installing..."
    mkdir -p "${HOME}/apptainer"
    curl -s https://raw.githubusercontent.com/apptainer/apptainer/main/tools/install-unprivileged.sh | \
    bash -s - "${HOME}/apptainer"
    export PATH="$HOME/apptainer/bin:$PATH"
fi

mkdir -p "${HOME}/ttcli"
git clone https://github.com/LuchnikovI/ttcli "${HOME}/ttcli"
if [[ $? -ne 0 ]]; then
    echo "Unable to clone a repo https://github.com/LuchnikovI/ttcli"
    exit 1
fi
chmod +x "${HOME}/ttcli/src/entrypoint.sh"
chmod +x "${HOME}/ttcli/src/hypertune.py"
chmod +x "${HOME}/ttcli/ttcli"
singularity remote use SylabsCloud && \
singularity pull --dir "${HOME}/ttcli/ci" tt.sif library://iluchnikov/ttcli/ttcli:latest
if [[ $? -ne 0 ]]; then
    echo "Unable to pull an repo image"
    exit 1
fi
export PATH="$HOME/ttcli:$PATH"
echo "export PATH=$PATH" >> "${HOME}/.bashrc"
echo "ttcli has been installed"
