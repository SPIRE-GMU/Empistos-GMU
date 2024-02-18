#! /bin/bash

cd /optee

# Sync OP-TEE git repos and initialize if they don't already exist
if ! repo sync --no-clone-bundle; then
    repo init -u https://github.com/OP-TEE/manifest.git -m rpi3.xml
    patch -p1 -r - -Nti /patches/repo.patch
    repo sync --no-clone-bundle
else
    echo "OP-TEE repo already initialized"
fi

# Download toolchains if they don't already exist
if [ ! -d toolchains ]; then
    cd /optee/build
    make -j2 toolchains
else
    echo "Toolchains already downloaded"
fi

# Clone darknetz into optee_examples if it hasn't already been cloned
cd /optee/optee_examples
if [ ! -d darknetz ]; then
    git clone https://github.com/mofanv/darknetz.git
    rm -rf darknetz/.git
else
    echo "darknetz already cloned"
fi

# Clone darknetz datasets into root filesystem if they haven't already been cloned
cd /optee
if [ ! -d out-br ]; then
    mkdir -p out-br/target/root
    git clone https://github.com/mofanv/tz_datasets.git out-br/target/root
    rm -rf out-br/target/root/.git
else
    echo "tz_datasets already cloned"
fi

# Apply patches
patch -p1 -r - -Nti /patches/optee.patch
patch -p1 -r - -Nti /patches/darknetz.patch

# Perform build
cd /optee/build
if [ ! -z "$NPROC" ]; then
    make -j$NPROC
else
    make
fi
