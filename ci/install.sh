#!/usr/bin/env bash

if singularity --help &> /dev/null; then
    :
else
    echo "Singularity not found. Installing..."
    mkdir -p "${HOME}/apptainer"
    curl -s https://raw.githubusercontent.com/apptainer/apptainer/main/tools/install-unprivileged.sh | \
    bash -s - "${HOME}/apptainer"
    cat >> "${HOME}/.bashrc" < EOF
    export PATH="$HOME/apptainer/bin:$PATH"
    EOF
fi

mkdir -p "${HOME}/ttcli"
git clone https://github.com/LuchnikovI/ttcli "${HOME}/ttcli"
chmod +x "${HOME}/ttcli/src/entrypoint.sh"
chmod +x "${HOME}/ttcli/src/hypertune.py"
chmod +x "${HOME}/ttcli/ttcli.sh"
singularity pull "${HOME}/ttcli/ci" tt.sif library://iluchnikov/ttcli/ttcli:latest
cat >> "${HOME}/.bashrc" < EOF
    export PATH="$HOME/ttcli:$PATH"
EOF
log "ttcli has been installed"
