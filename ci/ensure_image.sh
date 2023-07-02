#!/usr/bin/env bash

ci_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

. ${ci_dir}/utils.sh

python="python${TT_PYTHON_SHORT}"
image_name="${ci_dir}/tt"

cat << EOF > "${image_name}.def"
Bootstrap: docker
From: rust:${TT_RUST_VERSION}-bullseye
Stage: build

%post
    DEBIAN_FRONTEND=noninteractive apt update && \
        DEBIAN_FRONTEND=noninteractive apt-get install make cmake wget build-essential gfortran \
        libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libopenblas-dev \
        libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev -y && \
        wget -c https://www.python.org/ftp/python/${TT_PYTHON_VERSION}/Python-${TT_PYTHON_VERSION}.tar.xz && \
        tar -Jxvf Python-${TT_PYTHON_VERSION}.tar.xz && \
        (cd ./Python-${TT_PYTHON_VERSION} && ./configure \
            --prefix=/opt/python/${TT_PYTHON_VERSION} \
            --enable-shared \
            --enable-optimizations \
            --enable-ipv6 \
            LDFLAGS=-Wl,-rpath=/opt/python/${TT_PYTHON_VERSION}/lib,--disable-new-dtags) && \
        (cd ./Python-${TT_PYTHON_VERSION} && make && make install) && \
    curl -O https://bootstrap.pypa.io/get-pip.py && \
        /opt/python/${TT_PYTHON_VERSION}/bin/python${TT_PYTHON_MAJOR} get-pip.py && \
        rm get-pip.py && \
        ln -s /opt/python/${TT_PYTHON_VERSION}/bin/${python} /usr/bin/${python}
    ${python} -m pip install --upgrade pip && \
        ${python} -m pip install -U pytest -U mypy pylint -U setuptools maturin \
        patchelf pyyaml types-PyYAML matplotlib && \
        mv /opt/python/${TT_PYTHON_VERSION}/bin/patchelf /usr/bin/patchelf
    git clone --recurse-submodules https://github.com/LuchnikovI/ttrs && \
        ${python} -m maturin build -i ${python} -m ./ttrs/Cargo.toml --release && \
        ${python} -m pip install ./ttrs/target/wheels/*.whl

Bootstrap: docker
From: debian:bullseye-slim
Stage: final

%files from build
    /opt/python/ /opt/python/
%post
    ln -s /opt/python/${TT_PYTHON_VERSION}/bin/${python} /usr/bin/python
EOF

singularity build -F "${image_name}.sif" "${image_name}.def"

if [[ $? -ne 0 ]]; then
    log ERROR "Unable to build an image"
    rm ${image_name}.def
    exit 1
else
    log INFO "Image has been built"
    rm ${image_name}.def
fi

."${ci_dir}/run_checks.sh"

if [[ $? -ne 0 ]]; then
    log ERROR "Checks have not been passed"
    exit 1
else
    log INFO "Checks have been passed, pushing an image to the registry..."
fi

singularity push "${ci_dir}/tt.sif" library://iluchnikov/ttcli/ttcli:latest

if [[ $? -ne 0 ]]; then
    log ERROR "Failed to push an image to the registry"
    exit 1
else
    log INFO "An image has been pushed to the registry"
fi
